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

> ⚠️ **Not medical advice.** Stuck Doctor never diagnoses, suggests medicines, or reads scans. It only helps people get to a real doctor.

---

## ✨ Features

| | Feature | What it does |
|---|---|---|
| 🩺 | **Stuck diagnosis** | Names *why* you're avoiding the doctor and gives one 2-minute first move |
| 💬 | **One-tap actions** | Ready-to-send WhatsApp booking message, the right doctor on Google Maps, and a calendar reminder |
| 🎭 | **Rehearse the call** | Practise booking with *Meera*, an AI clinic receptionist, until the real call feels easy |
| 👨‍👩‍👧 | **Help someone you love** | Gentle messages to convince a parent or grandparent to go, plus an offer to go with them |
| 🧪 | **Report decoder** | Every blood-test value checked against the printed range, marked **Low / Normal / High**, and double-checked against your photo |
| 💊 | **My medicines** | Snap a prescription or add medicines and supplements by hand, then add every reminder to your phone in one tap |
| 📝 | **After-the-visit notes** | Say what the doctor told you, and get a summary, to-do list, follow-up reminder and family update |
| 🗒️ | **Show-the-doctor card** | Too shy to say it? A full-screen note in your own words |
| 💰 | **Free-care finder** | Points to government hospitals, eSanjeevani (free online doctor), Jan Aushadhi and Ayushman Bharat |
| 🚑 | **SOS button** | Always one tap away: 108 ambulance, 112 emergency, 104 helpline, share live location, nearest hospital |

### ♿ Built for everyone
- 🗣️ **English, Hindi, Hinglish, Bengali**, or **Auto** (replies in the language you write in)
- 🎙️ **Voice input** and 🔊 **read-aloud** for people who can't read well
- 🔠 **Bigger text** button, plus short, simple sentences
- 🌙 **Light and dark themes**, and works on any phone

---

## 🧠 How it works

Website ──► Render back end (Gradio API) ──► Gemma 4 (Gemini API)
▲ │
└──── prescription, ◄────┘ Python checks numbers, builds WhatsApp,
buttons, reminders Maps & Calendar links


1. **Front end:** a custom HTML/CSS/JS website on **GitHub Pages**
2. **Back end:** a **Gradio** API on **Render**, with four endpoints: `prescribe`, `read_document`, `visit_summary`, `rehearse`
3. **AI:** **Gemma 4** (open-weight) replies in structured JSON, with per-task temperature and automatic retry if an answer is incomplete
4. **Code, not guesses:** lab values are compared to reference ranges **by Python**, not by the AI. Reports get a second "double-check" pass.

---

## 🛠️ Tech stack

`Gemma 4` · `Gemini API` · `Ollama` (prototyping) · `Gradio` · `Python` · `HTML / CSS / JavaScript` · `Web Speech API` · `GitHub Pages` · `Render` · `Google Colab`

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

---

## 🛡️ Safety

| ✅ Stuck Doctor **will** | ❌ Stuck Doctor **won't** |
|---|---|
| Help you understand why you're avoiding care | Diagnose what's wrong with you |
| Give one tiny, doable first step | Suggest medicines, doses or home remedies |
| Explain report terms and flag out-of-range values | Read X-ray, MRI or CT images |
| Turn your doctor's instructions into reminders | Book appointments for you |
| Flag warning signs that mean "go sooner" | Replace a real doctor or pharmacist |

---

## 🗺️ What's next
- Offline mode for low-connectivity areas
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
