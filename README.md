<div align="center">

# 🩺 Stuck Doctor

### The hardest part of seeing a doctor is *starting*. Stuck Doctor helps you start.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20App-0f6b63?style=for-the-badge)](https://kk-dev0.github.io/Stuck_Doctor/)
[![Gemma 4](https://img.shields.io/badge/AI-Gemma%204-e0643a?style=for-the-badge)](https://ai.google.dev/gemma)
[![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest-2026-1c2a28?style=for-the-badge)](https://hacktoberfest.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

**[👉 Try it live](https://kk-dev0.github.io/Stuck_Doctor/)**

*Built in one day at Hacktoberfest × HackTropica, Asansol · 3 October 2026*

</div>

---

## 💡 The problem

Millions of people put off going to the doctor, not because they don't care, but because they're **stuck**:
scared of bad news, hate phone calls, worried about cost, unsure which doctor to see, or too embarrassed to say it out loud.

Most health apps tell you *what* to do. **Stuck Doctor asks *why* you're stuck**, then gives you one tiny step that fits, and helps you actually take it.

> I built this for the 5th week someone says "I'll go next week."

> ⚠️ **Not medical advice.** Stuck Doctor never diagnoses, suggests medicines, or reads scans. It only helps people get to a real doctor.

---

## ✨ Features

| | Feature | What it does |
|---|---|---|
| 🩺 | **Stuck diagnosis** | Names *why* you're avoiding the doctor and gives one 2-minute first move |
| ⚡ | **One-tap examples** | Tap "Ear ache, 2 weeks" on the home page and get a full plan without typing anything |
| 💬 | **One-tap actions** | Ready-to-send WhatsApp booking message, the right doctor on Google Maps, and a calendar reminder |
| 🎭 | **Rehearse the call** | Practise booking with *Meera*, an AI clinic receptionist, until the real call feels easy |
| 👨‍👩‍👧 | **Help someone you love** | Gentle messages to convince a parent or grandparent to go, plus an offer to go with them |
| 🧭 | **Your journey** | Tick off three steps: first move, book, go. Come back later and it asks how it went, so the app follows up instead of ending after one answer |
| 🧪 | **Report decoder** | Every blood-test value checked against the printed range, marked **Low / Normal / High**, double-checked against your photo, with a visible confidence note |
| 💊 | **My medicines** | Snap a prescription or add medicines and supplements by hand, then add every reminder to your phone in one tap |
| 📝 | **After-the-visit notes** | Say what the doctor told you, and get a summary, to-do list, follow-up reminder and family update |
| 🗒️ | **Show-the-doctor card** | Too shy to say it? A full-screen note in your own words |
| 💰 | **Free-care finder** | Points to government hospitals, eSanjeevani (free online doctor), Jan Aushadhi and Ayushman Bharat |
| 🚨 | **Emergency routing** | Words like "chest pain" or "can't breathe" (English, Hinglish, Hindi, Bengali) skip the AI and show 108 / 112 straight away. Words about self-harm show Tele-MANAS 14416 |
| 🚑 | **SOS button** | Always one tap away: 108 ambulance, 112 emergency, 104 helpline, Tele-MANAS 14416, share live location, nearest hospital |
| 📤 | **Share** | Send Stuck Doctor to someone who keeps putting it off, with the phone's share menu or WhatsApp |

### ♿ Built for everyone
- 🗣️ **English, Hindi, Hinglish, Bengali**, or **Auto** (replies in the language you write in)
- 🎙️ **Voice input** and 🔊 **read-aloud** for people who can't read well
- 🔠 **Bigger text** and ◐ **high contrast** buttons, plus short, simple sentences
- ⌨️ Skip link, screen-reader labels, visible keyboard focus, and reduced-motion support
- 🌙 **Light and dark themes**, and works on any phone
- 📴 **Works offline:** after the first visit, the page, the SOS button and an offline care card open without internet (the AI itself needs internet)
- ⏳ **Wakes the AI for you:** if the free server has been asleep, the page says so, retries by itself, and shows a sample while you wait

---

## 🧠 How it works

```
Website ──► Render back end (Gradio API) ──► Gemma 4 (Gemini API)
   ▲                  │
   └── prescription,  ◄── Python checks emergency words and numbers,
       buttons,           builds WhatsApp, Maps and Calendar links
       reminders
```

1. **Front end:** a custom HTML/CSS/JS website on **GitHub Pages**, with a small service worker (`sw.js`) for offline use
2. **Back end:** a **Gradio** API on **Render**, with four endpoints: `prescribe`, `read_document`, `visit_summary`, `rehearse`
3. **AI:** **Gemma 4** (open-weight) replies in structured JSON, with per-task temperature and automatic retry if an answer is incomplete
4. **Code, not guesses:**
   - Lab values are compared to reference ranges **by Python**, not by the AI.
   - Reports get a second "double-check" pass, and the result shows a confidence note based on whether the two readings matched.
   - Emergency words are matched by code in the browser and again on the back end. They never depend on what the model says.
5. **Always on:** a GitHub Actions job pings the Render back end every 10 minutes so the free server rarely sleeps

---

## 🛠️ Tech stack

`Gemma 4` · `Gemini API` · `Ollama` (prototyping) · `Gradio` · `Python` · `HTML / CSS / JavaScript` · `Web Speech API` · `Service Worker` · `GitHub Pages` · `GitHub Actions` · `Render` · `Google Colab`

---

## 🚀 Run it yourself

**Website:** open `index.html`, or visit the [live demo](https://kk-dev0.github.io/Stuck_Doctor/).

**Back end:**
```bash
cd backend
pip install -r requirements.txt
export GEMINI_API_KEY=your_key_here   # free key from aistudio.google.com
python app.py
```
Then set `DEFAULT_BACKEND` in `index.html` to your back-end URL.

**Keep a free Render server awake (optional):** the workflow in `.github/workflows/keep-alive.yml` pings it every 10 minutes. Change the URL inside it if your Render address is different.

---

## 🛡️ Safety

| ✅ Stuck Doctor **will** | ❌ Stuck Doctor **won't** |
|---|---|
| Help you understand why you're avoiding care | Diagnose what's wrong with you |
| Give one tiny, doable first step | Suggest medicines, doses or home remedies |
| Explain report terms and flag out-of-range values | Read X-ray, MRI or CT images |
| Turn your doctor's instructions into reminders | Book appointments for you |
| Flag warning signs that mean "go sooner" | Replace a real doctor or pharmacist |
| Skip the AI and show 108 / 112 if you describe an emergency | Plan a routine visit for someone who describes an emergency |

---

## 🔒 Privacy

- **Photos** are sent to Google's Gemini API so the AI can read them. The back end deletes the file as soon as the answer is ready and never stores it. Google's own terms for the Gemini API apply to what is sent.
- **Text you type** goes to the same AI to write your answer. Stuck Doctor does not store it.
- **Your medicine list and journey** are saved only in your own browser, on your own device.
- **No accounts, no ads, no analytics.**

---

## 🗺️ What's next
- More Indian languages (Tamil, Telugu, Marathi)
- Nearby clinic timings and fees
- Shared family accounts for caregivers

---

## 📄 License & credits

Code under the **MIT License**. Gemma is subject to Google's Gemma terms of use.
AI assistance (Claude) was used in building this project.

<div align="center">

**Made with 🩺 at Hacktoberfest 2026**

</div>
