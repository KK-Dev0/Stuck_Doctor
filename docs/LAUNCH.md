# Launch kit

Everything here is copy, paste and fill in. Anything in [square brackets] is something only you know. Don't leave brackets in what you post.

---

## 1. The one-liner

Pick one and use it everywhere (README top, DEV post, LinkedIn, demo video):

- "I built this for the 5th week someone says 'I'll go next week.'"
- "Stuck Doctor doesn't treat you. It gets you through the door."

---

## 2. 60-second demo video (shot list)

Record your phone screen with the screen recorder built into Android or iPhone, in portrait.

| Seconds | What's on screen | What you say |
|---|---|---|
| 0-5 | The home page | "Everyone knows someone who keeps saying they'll see a doctor next week. Stuck Doctor helps them actually go." |
| 5-20 | Tap "Ear ache, 2 weeks" chip, result appears | "One tap. It figures out why you're stuck, gives one two-minute first step, and writes the WhatsApp message to the clinic." |
| 20-30 | Switch language to Hindi, tap Read aloud | "Works in English, Hindi and Bengali, and reads everything out loud." |
| 30-42 | Report tab, upload a blurred sample report, show the low/high chips and confidence note | "Photograph a report. Every number is checked against the range printed on it, by code, not by the AI, and read twice." |
| 42-50 | Type "chest pain" and show the emergency screen | "If someone describes an emergency, it skips the AI and shows 108 and 112 immediately." |
| 50-60 | Journey checklist, then the home page with the one-liner | "[Your one-liner]. It's open source, built with Gemma. Link below." |

**README GIF:** trim the first 5 to 20 seconds, convert at 12 fps and 480px wide, and keep it under 8 MB. Free tools: ScreenToGif (Windows), Gifski (Mac), or ezgif.com in the browser. Save it as `docs/demo.gif`.

---

## 3. README additions

Paste these into README.md.

```markdown
![Stuck Doctor demo](docs/demo.gif)

> I built this for the 5th week someone says "I'll go next week."

## Privacy
- Photos are sent to Google's Gemini API so the AI can read them. The back end deletes the file as soon as the answer is ready and never stores it. Google's own terms for the Gemini API apply to what is sent.
- Text you type is sent to the same AI to write your answer. Stuck Doctor does not store it.
- Your medicine list and journey are saved only in your own browser.
- No accounts, no ads, no analytics.

## Safety
- Emergency words in English, Hindi, Hinglish and Bengali skip the AI and show 108 / 112 (and Tele-MANAS 14416 for mental health).
- Lab values are compared with the range printed on the report by Python code, not by the AI.
- Reports are read twice, and the result shows a confidence note.
- Stuck Doctor never diagnoses, never suggests medicines or doses, and refuses to read X-ray, MRI or CT images.

## Testing
See [docs/TESTING.md](docs/TESTING.md). Report decoder: [X of Y values right on Z photos]. User test: [N testers, M took their first step].

## Works offline
After the first visit, the page, the SOS button and the offline care card open without internet. The AI itself needs internet.
```

---

## 4. DEV post (draft)

**Title ideas**
- I built an app for the 5th week of "I'll go to the doctor next week"
- Stuck Doctor: using Gemma to get people to the doctor, not to replace one

**Body**

> Everyone knows someone who keeps saying "I'll go next week." Maybe it's you. I built Stuck Doctor for that fifth week.
>
> It's not a symptom checker. It doesn't diagnose. It works on the part that actually stops people: starting.
>
> **What it does**
> - You say why you're putting it off (scared, hate calling, "it's probably nothing", cost, awkward, don't know which doctor).
> - It gives one two-minute first step, a ready WhatsApp message to the clinic, questions to ask, and what to carry.
> - If money is tight, it points to government hospitals, eSanjeevani and Jan Aushadhi stores.
> - It can rehearse the booking phone call with an AI receptionist.
> - Family mode helps you convince a parent or grandparent to go.
> - You can speak instead of typing, in English, Hindi or Bengali, and everything can be read aloud.
> - It decodes report photos and turns prescriptions into reminders.
>
> **How it's built**
> - Front end: plain HTML, CSS and JavaScript on GitHub Pages.
> - Back end: a Gradio API on Render, calling Gemma 4 through the Gemini API. Four endpoints: `prescribe`, `read_document`, `visit_summary`, `rehearse`.
> - Gemma returns structured JSON. Each task has its own temperature, and incomplete answers are retried automatically.
>
> **Where I didn't trust the AI**
> - Lab values are compared with the range printed on the report by Python, never by the model.
> - Reports are read twice, and the screen shows a confidence note based on whether the second reading matched.
> - Emergency words in four languages are matched by code and skip the model entirely. If someone writes "chest pain", they see 108 and 112, not a friendly paragraph.
> - It refuses to read scans (X-ray, MRI, CT).
> - Uploaded photos are deleted from the server as soon as the answer is ready.
>
> **What I learned from testing**
> - [One honest lesson from your 5 testers.]
> - [One honest lesson from the report test: for example, which photos failed and what you changed.]
> - [Your real number: "N testers, M took their first step."]
>
> **Try it:** [site link] · **Code:** https://github.com/KK-Dev0/Stuck_Doctor
>
> Stuck Doctor is not medical advice. It exists to get you to someone who can give it.

---

## 5. LinkedIn post (draft)

> For the fifth week in a row, someone I know said "I'll go to the doctor next week."
>
> So I built Stuck Doctor. It doesn't diagnose anyone. It helps people take the first step: why they're stuck, one two-minute action, the WhatsApp message to the clinic, free-care options, and a practice phone call with an AI receptionist.
>
> It works in English, Hindi and Bengali, reads answers aloud, decodes report photos (numbers checked by code, not by the AI), and sends emergency words straight to 108 and 112.
>
> Built with Gemma, Gradio, Render and GitHub Pages. [Your honest result from testing.]
>
> Try it: [link] · Code: https://github.com/KK-Dev0/Stuck_Doctor
>
> #Hacktoberfest #Gemma #OpenSource #HealthTech #India
