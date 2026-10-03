# ==================== Stuck Doctor · back end (Render) ====================
# Runs Gemma 4 through Google's Gemini API, so nothing needs to stay open in Colab.
# Needs one environment variable on Render: GEMINI_API_KEY (from aistudio.google.com).
import os, json, datetime, re, mimetypes
from urllib.parse import quote
from zoneinfo import ZoneInfo
import gradio as gr
from google import genai
from google.genai import types

MODEL = os.environ.get("GEMMA_MODEL", "gemma-4-26b-a4b-it")   # or "gemma-4-31b-it"
IST = ZoneInfo("Asia/Kolkata")
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))

def llm(system, messages, kind):
    """Send a conversation to Gemma. messages: [{'role': 'user'|'assistant', 'content': str, 'images': [paths]}]"""
    contents = []
    for m in messages:
        parts = []
        for p in m.get("images") or []:
            with open(p, "rb") as f:
                parts.append(types.Part.from_bytes(data=f.read(), mime_type=mimetypes.guess_type(p)[0] or "image/jpeg"))
        parts.append(types.Part.from_text(text=str(m.get("content", ""))))
        contents.append(types.Content(role="model" if m.get("role") == "assistant" else "user", parts=parts))
    cfg = types.GenerateContentConfig(system_instruction=system, temperature=SETTINGS[kind]["temperature"])
    r = client.models.generate_content(model=MODEL, contents=contents, config=cfg)
    return (r.text or "").strip()

def parse_json(text):
    t = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    a, b = t.find("{"), t.rfind("}")
    if a == -1 or b == -1:
        raise json.JSONDecodeError("no JSON found", t, 0)
    return json.loads(t[a:b + 1])

def ensure_ollama():   # kept so the rest of the code is unchanged; nothing to start here
    return

# ---------- model settings per task ----------
SETTINGS = {
    "prescribe": {"temperature": 0.6, "num_ctx": 8192},
    "document":  {"temperature": 0.1, "num_ctx": 16384},
    "verify":    {"temperature": 0.0, "num_ctx": 16384},
    "visit":     {"temperature": 0.3, "num_ctx": 8192},
    "rehearse":  {"temperature": 0.8, "num_ctx": 8192},
}
REQUIRED = {
    "prescribe": ["diagnosis", "first_move", "message", "questions"],
    "document":  ["doc_type", "summary"],
    "visit":     ["summary"],
}
TIMES = ["In 1 hour", "Tonight (7 PM)", "Tomorrow morning (10 AM)", "This Saturday (11 AM)"]

def ask_json(system, user_msg, kind):
    """Ask Gemma for JSON. If the answer is broken or missing keys, tell it and retry once."""
    system = system + "\nReply with ONE valid JSON object only. No markdown, no extra text."
    for attempt in range(2):
        try:
            d = parse_json(llm(system, [user_msg], kind))
        except json.JSONDecodeError:
            continue
        missing = [k for k in REQUIRED.get(kind, []) if not d.get(k)]
        if not missing:
            return d
        user_msg = {**user_msg, 'content': user_msg['content'] +
                    f"\n\nYour last answer was missing: {', '.join(missing)}. Reply again with every key filled in."}
    raise json.JSONDecodeError("incomplete answer", "", 0)

def lang_rule(language):
    simple = " Use short, simple sentences that someone with little schooling can understand. Keep the JSON keys in English exactly as written."
    if not language or str(language).lower().startswith("auto"):
        return "Write every text value in the same language and script the user wrote in (for example Hindi, Bengali, Hinglish or English). If you cannot tell, use simple English." + simple
    if language == "Hinglish":
        return "Write every text value in Hinglish (Hindi words written in English letters)." + simple
    if language in ("Hindi", "Bengali"):
        return f"Write every text value in {language}, in its own script." + simple
    return f"Write every text value in simple {language}." + simple

def now_ist():
    return datetime.datetime.now(IST)

def cal_link(title, details, start, minutes=15, recur_days=None):
    end = start + datetime.timedelta(minutes=minutes)
    fmt = "%Y%m%dT%H%M%S"
    url = ("https://calendar.google.com/calendar/render?action=TEMPLATE"
           f"&text={quote(title)}&details={quote(details)}"
           f"&dates={start.strftime(fmt)}/{end.strftime(fmt)}&ctz=Asia/Kolkata")
    if recur_days:
        url += "&recur=" + quote(f"RRULE:FREQ=DAILY;COUNT={recur_days}")
    return url

def pick_time(when):
    now = now_ist()
    if when == "In 1 hour":
        return now + datetime.timedelta(hours=1)
    if when == "Tonight (7 PM)":
        t = now.replace(hour=19, minute=0, second=0, microsecond=0)
        return t if t > now else t + datetime.timedelta(days=1)
    if when == "Tomorrow morning (10 AM)":
        return (now + datetime.timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)
    days = (5 - now.weekday()) % 7 or 7
    return (now + datetime.timedelta(days=days)).replace(hour=11, minute=0, second=0, microsecond=0)

# ---------- number checking (done by Python, not the AI) ----------
def parse_num(s):
    m = re.search(r"-?\d+(?:\.\d+)?", str(s).replace(",", ""))
    return float(m.group()) if m else None

def range_bounds(r):
    r = str(r or "").replace(",", "")
    nums = re.findall(r"\d+(?:\.\d+)?", r)
    if len(nums) == 1 and re.search(r"<|less than|up ?to|below", r, re.I):
        return None, float(nums[0])
    if len(nums) == 1 and re.search(r">|more than|above", r, re.I):
        return float(nums[0]), None
    if len(nums) >= 2:
        return float(nums[0]), float(nums[1])
    return None, None

def status_of(v):
    val = parse_num(v.get("value"))
    lo, hi = range_bounds(v.get("range"))
    if val is None or (lo is None and hi is None):
        return "unknown"
    if lo is not None and val < lo:
        return "low"
    if hi is not None and val > hi:
        return "high"
    return "normal"

# ==================== 1. I'M STUCK ====================
def prescribe_prompt(language, helping, relation, budget):
    rel = relation.strip() if relation and relation.strip() else "family member"
    if helping:
        who = (f"The user is HELPING their {rel}, who keeps putting off the doctor. "
               f"'first_move' is something the USER can do in 2 minutes to help their {rel}. "
               f"'message' is a gentle, loving WhatsApp message the user can send to their {rel} to encourage them to go (no guilt, no scaring). "
               f"'buddy_message' is a short message to the {rel} offering to go with them. "
               f"'doctor_note' describes the {rel}'s problem in the third person, using ONLY what the user said. "
               f"'diagnosis' names the kind of stuck the {rel} seems to be in.")
    else:
        who = ("The user is the person putting it off. "
               "'message' is a short WhatsApp message to a clinic asking to book an appointment. "
               "'buddy_message' is a short, warm message asking a friend to come along. "
               "'doctor_note' is 2-3 first-person sentences the user can show the doctor, describing ONLY what they told you.")
    money = {
        "Free / government only": ("The user can only afford free care. Point them to government options: the government hospital OPD, "
                                   "the Primary Health Centre (PHC), the free eSanjeevani online doctor consultation from the Government of India, "
                                   "and Jan Aushadhi stores for cheaper generic medicines. Use \"government hospital\" as doctor_type unless a specialist is clearly needed. "
                                   "Give 2 cost_tips."),
        "Low cost": ("The user is on a tight budget. Mention low-cost options where they fit: government hospital OPD, eSanjeevani free online consultation, "
                     "and Jan Aushadhi generic medicine stores. Give 2 cost_tips."),
    }.get(budget, "No budget limit was given. cost_tips should be an empty list.")
    return f"""You are Stuck Doctor, a calm, kind helper for people in India who keep putting off going to the doctor.
You do NOT diagnose or give medical advice. You only help them take the next step toward care.
{who}
{money}
{lang_rule(language)}
Reply ONLY with JSON using exactly these keys:
"urgent": true if anything sounds urgent or serious (chest pain, trouble breathing, heavy bleeding, fainting, sudden severe pain, signs of stroke), otherwise false
"diagnosis": one kind sentence naming the type of stuck
"first_move": one specific action that can be done in 2 minutes
"doctor_type": the kind of doctor to search for, in 1-3 ENGLISH words (use "general physician" if unsure)
"message": see above
"questions": a list of 3 short questions to ask the doctor during the visit
"while_you_wait": a list of 2 gentle, general comfort tips with no medicines, doses, home remedies or putting anything in the body
"see_sooner_if": a list of 2-3 warning signs that mean get care urgently
"doctor_note": see above
"buddy_message": see above
"bring_list": a list of 3-5 practical things to carry to the visit (photo ID, old reports, list of current medicines, anything specific)
"cost_tips": see above
"suggested_when": copy EXACTLY one of these English options: {TIMES}. Pick the soonest realistic time. Prefer today unless it is late at night. Never suggest waiting because of fear, since delay makes it worse. Always "In 1 hour" if urgent.
"why_this_time": one short sentence explaining why that time is good
"push": one encouraging line
Do not mention insurance unless the user does."""

def prescribe(task, reason, when, language, details, for_whom, relation, budget):
    ensure_ollama()
    task = (task or "").strip() or "seeing a doctor"
    helping = str(for_whom or "").lower().startswith("someone")
    who_line = f"I'm asking for my {relation or 'family member'}." if helping else "I'm asking for myself."
    try:
        d = ask_json(prescribe_prompt(language, helping, relation, budget), {'role': 'user', 'content':
            f"{who_line}\nWhat is being put off: {task}\nWhy stuck: {reason}\nBudget: {budget}\nAnything else: {details}"}, "prescribe")
    except json.JSONDecodeError:
        return {"error": "Stuck Doctor got confused. Please try again."}
    except Exception:
        return {"error": "The AI is busy right now. Please try again in a minute."}

    guided = when not in TIMES
    chosen = when
    if guided:
        chosen = "In 1 hour" if d.get("urgent") else d.get("suggested_when")
        if chosen not in TIMES:
            chosen = "Tomorrow morning (10 AM)"
    doctor = d.get("doctor_type") or "doctor"
    search = "government hospital" if budget == "Free / government only" else doctor
    title = (f"Stuck Doctor: help my {relation or 'family member'} see a doctor" if helping
             else f"Stuck Doctor: book a doctor for {task}")
    d.update({
        "task": task, "chosen": chosen, "guided": guided, "helping": helping,
        "relation": relation or "family member", "budget": budget, "search_label": search,
        "date": now_ist().strftime("%d %b %Y"),
        "links": {
            "whatsapp": "https://wa.me/?text=" + quote(d.get("message", "")),
            "buddy": "https://wa.me/?text=" + quote(d.get("buddy_message", "")) if d.get("buddy_message") else "",
            "maps": "https://www.google.com/maps/search/?api=1&query=" + quote(search + " near me"),
            "calendar": cal_link(title, d.get("first_move", ""), pick_time(chosen)),
        },
    })
    return d

# ==================== 2. EXPLAIN MY REPORT / PRESCRIPTION ====================
def doc_prompt(language):
    return f"""You read photos of medical documents (blood tests, reports, prescriptions, clinic cards, bills, scan images) for people in India.
Your job is to help people understand the WORDS and NUMBERS on their documents and get to their doctor.
Rules:
- Never diagnose, never say what the person has, and never say whether they are fine or not.
- If the image is a medical scan itself (X-ray, MRI, CT, ultrasound picture) rather than a written document, do NOT describe any findings. Set is_scan to true, say only what kind of scan it seems to be and which body part, and leave explained, values and medicines empty.
- For values, copy every numeric test result EXACTLY as printed with its unit and the printed reference range ("" if none). Do not judge them.
- For prescriptions, copy each medicine and its instructions EXACTLY as written. Convert the timing into 24-hour reminder times using these common Indian conventions:
  1-0-1 = ["08:00","21:00"], 1-1-1 = ["08:00","14:00","21:00"], 1-0-0 = ["08:00"], 0-0-1 = ["21:00"], 0-1-0 = ["14:00"],
  OD = ["08:00"], BD = ["08:00","20:00"], TDS = ["08:00","14:00","20:00"], QID = ["08:00","12:00","16:00","20:00"], HS = ["22:00"], SOS = [] (only when needed).
  Only use times when the instruction clearly says so. Otherwise use [].
- Test names, values, units and medicine names stay exactly as printed. {lang_rule(language)}
Reply ONLY with JSON using exactly these keys:
"doc_type": what kind of document this is, in a few words
"is_prescription": true if it lists medicines to take, otherwise false
"is_scan": true if this is a scan image rather than a written document, otherwise false
"summary": 2-3 plain sentences describing what is written (tests done, dates, instructions as written)
"explained": a list of objects like {{"term": "...", "meaning": "..."}} explaining up to 6 medical terms in plain words
"values": a list of objects like {{"test": "...", "value": "...", "unit": "...", "range": "..."}} for every numeric result
"medicines": a list of objects like {{"name": "...", "as_written": "...", "times": ["08:00"], "days": 5, "with_food": "after food"}} (days null if not written, with_food "" if not written)
"clinic_name": clinic or hospital name if visible, else ""
"doctor_name": doctor's name if visible, else ""
"phone": phone number if visible, else ""
"follow_up": any follow-up date or instruction written on it, else ""
"questions": a list of 3 questions to ask the doctor or pharmacist about this document
"message": a short WhatsApp message to the clinic to book a follow-up or ask about this document
If the image is not a medical document or cannot be read, set doc_type to "unreadable" and explain why in summary."""

VERIFY_PROMPT = """You are double-checking a first reading of a medical document photo. Look at the image again, very carefully, line by line.
Compare every test name, value, unit, range, medicine name, instruction and time in the first reading against what is actually printed.
Fix anything that was misread, add anything that was missed, and remove anything that is not on the document.
Reply ONLY with JSON using exactly these keys:
"values": the corrected full list, same format as the first reading
"medicines": the corrected full list, same format as the first reading
"changes": a list of short English sentences describing each fix (an empty list if everything matched)"""

def med_reminders(med):
    days = parse_num(med.get("days"))
    days = int(days) if days and 0 < days <= 90 else None
    med["days"] = days
    links = []
    for t in med.get("times") or []:
        m = re.match(r"^\s*(\d{1,2}):(\d{2})\s*$", str(t))
        if not m or int(m.group(1)) > 23 or int(m.group(2)) > 59:
            continue
        now = now_ist()
        start = now.replace(hour=int(m.group(1)), minute=int(m.group(2)), second=0, microsecond=0)
        if start <= now:
            start += datetime.timedelta(days=1)
        details = (f"As written on your prescription: {med.get('as_written', '')}. {med.get('with_food', '')}\n"
                   "Read by AI. Check against your prescription and confirm with your pharmacist or doctor.")
        links.append({"time": f"{int(m.group(1)):02d}:{m.group(2)}",
                      "url": cal_link(f"💊 {med.get('name', 'Medicine')}", details, start, minutes=5, recur_days=days)})
    med["reminders"] = links
    return med

def read_document(image_path, language, double_check):
    ensure_ollama()
    if not image_path:
        return {"error": "Please upload a photo of the document."}
    try:
        d = ask_json(doc_prompt(language), {'role': 'user', 'content': "Read this document carefully.", 'images': [image_path]}, "document")
    except json.JSONDecodeError:
        return {"error": "I couldn't make sense of that photo. Try a clearer, well-lit one."}
    except Exception:
        return {"error": "The AI is busy right now. Please try again in a minute."}

    values = [v for v in (d.get("values") or []) if isinstance(v, dict)] if not d.get("is_scan") else []
    meds = [m for m in (d.get("medicines") or []) if isinstance(m, dict)] if not d.get("is_scan") else []
    d["verified"], d["changes"] = False, []

    # second pass: double-check the numbers and medicines against the photo
    if str(double_check or "yes").lower().startswith("y") and (values or meds):
        try:
            v = ask_json(VERIFY_PROMPT, {'role': 'user', 'images': [image_path], 'content':
                         "First reading:\n" + json.dumps({"values": values, "medicines": meds}, ensure_ascii=False)}, "verify")
            if isinstance(v.get("values"), list):
                values = [x for x in v["values"] if isinstance(x, dict)]
            if isinstance(v.get("medicines"), list):
                meds = [x for x in v["medicines"] if isinstance(x, dict)]
            d["changes"] = [str(c) for c in (v.get("changes") or [])][:6]
            d["verified"] = True
        except Exception:
            pass

    for v in values:
        v["status"] = status_of(v)
    d["values"] = values
    d["medicines"] = [med_reminders(m) for m in meds if m.get("name")]

    digits = re.sub(r"\D", "", d.get("phone") or "")
    if len(digits) == 10:
        digits = "91" + digits
    msg = quote(d.get("message", ""))
    clinic = d.get("clinic_name") or ""
    d["links"] = {
        "whatsapp": f"https://wa.me/{digits}?text={msg}" if len(digits) >= 11 else f"https://wa.me/?text={msg}",
        "call": f"tel:+{digits}" if len(digits) >= 11 else "",
        "maps": "https://www.google.com/maps/search/?api=1&query=" + quote(clinic) if clinic else "",
    }
    return d

# ==================== 3. AFTER MY VISIT ====================
def visit_summary(notes, language):
    ensure_ollama()
    notes = (notes or "").strip()
    if not notes:
        return {"error": "Write or say what the doctor told you first."}
    today = now_ist().strftime("%Y-%m-%d (%A)")
    prompt = f"""You turn messy notes from a doctor visit into a clear, simple summary.
Use ONLY what is in the notes. Never add medical advice, diagnoses, or medicines that are not in the notes.
{lang_rule(language)}
Today is {today}.
Reply ONLY with JSON using exactly these keys:
"summary": 2-3 simple sentences of what the doctor said
"todo": a list of clear action items from the notes (tests to get, things to buy, things to avoid, exactly as the doctor said)
"medicines": a list of objects like {{"name": "...", "as_said": "..."}} for medicines mentioned, copied as said
"follow_up_date": the follow-up date as YYYY-MM-DD if a date or a number of days/weeks is mentioned, else ""
"follow_up_text": the follow-up instruction as said, else ""
"questions_left": a list of 1-3 things that sound unclear and are worth asking the doctor or pharmacist
"family_message": a short, calm WhatsApp message to update family about the visit"""
    try:
        d = ask_json(prompt, {'role': 'user', 'content': notes}, "visit")
    except json.JSONDecodeError:
        return {"error": "Stuck Doctor got confused. Please try again."}
    except Exception:
        return {"error": "The AI is busy right now. Please try again in a minute."}
    d["links"] = {"family": "https://wa.me/?text=" + quote(d.get("family_message", "")) if d.get("family_message") else ""}
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", str(d.get("follow_up_date") or ""))
    if m:
        try:
            start = datetime.datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), 10, 0, tzinfo=IST)
            d["links"]["calendar"] = cal_link("🩺 Doctor follow-up", d.get("follow_up_text") or d.get("summary", ""), start, minutes=30)
            d["follow_up_pretty"] = start.strftime("%a, %d %b %Y")
        except ValueError:
            pass
    return d

# ==================== 4. REHEARSE THE CALL ====================
def rehearse(history_json, task, language):
    ensure_ollama()
    try:
        history = json.loads(history_json or "[]")
    except json.JSONDecodeError:
        history = []
    speak = ("Reply in the same language and script the caller uses." if not language or str(language).lower().startswith("auto")
             else f"Speak in {language}.")
    system = f"""You are Meera, a friendly but busy receptionist at City Care Clinic, a small neighbourhood clinic in India, on a phone call.
The caller is PRACTISING booking an appointment because phone calls make them nervous. Stay in character the whole time.
{speak} Keep every reply to 1-2 short sentences, like a real receptionist on the phone.
Ask the usual things one at a time: their name, briefly what the visit is for, and a preferred day and time. Offer a realistic slot and mention the consultation fee is paid at the clinic.
Never give medical advice. If they mention anything that sounds like an emergency, tell them kindly to call 108 or go to a hospital now.
Once the appointment is confirmed, give the confirmation, then on a new line write "✅ Practice complete!" and one short, kind tip on how they did.
The caller wants to book for: {task or 'a doctor visit'}"""
    msgs = [{'role': 'user', 'content': "(The phone rings and you pick up.)"}]
    for m in history[-20:]:
        if isinstance(m, dict) and m.get("role") in ("user", "assistant"):
            msgs.append({'role': m["role"], 'content': str(m.get("content", ""))[:500]})
    try:
        return {"reply": llm(system, msgs, "rehearse")}
    except Exception:
        return {"reply": "Sorry, the line is busy. Please try again in a moment."}

# ==================== API for the website ====================
with gr.Blocks(title="Stuck Doctor API") as api:
    gr.Markdown("## 🩺 Stuck Doctor back end is running\nThis is the always-on back end for the Stuck Doctor website.")
    with gr.Tab("Prescribe"):
        ins = [gr.Textbox(label=x) for x in ["task", "reason", "when", "language", "details", "for_whom", "relation", "budget"]]
        out = gr.JSON()
        gr.Button("Test").click(prescribe, ins, out, api_name="prescribe")
    with gr.Tab("Read document"):
        img = gr.Image(type="filepath", label="document")
        l2 = gr.Textbox(label="language", value="Auto")
        dc = gr.Textbox(label="double_check", value="yes")
        out2 = gr.JSON()
        gr.Button("Test").click(read_document, [img, l2, dc], out2, api_name="read_document")
    with gr.Tab("Visit summary"):
        n = gr.Textbox(label="notes", lines=4)
        l4 = gr.Textbox(label="language", value="Auto")
        out4 = gr.JSON()
        gr.Button("Test").click(visit_summary, [n, l4], out4, api_name="visit_summary")
    with gr.Tab("Rehearse"):
        h = gr.Textbox(label="history (JSON)", value="[]")
        t3 = gr.Textbox(label="task")
        l3 = gr.Textbox(label="language", value="Auto")
        out3 = gr.JSON()
        gr.Button("Test").click(rehearse, [h, t3, l3], out3, api_name="rehearse")

api.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
