# Stuck_Doctor
Helps people who keep putting off the doctor actually book. Built with Gemma + Ollama + Gradio.
**For people who keep putting off the doctor.**

Most apps tell you *what* to do. Stuck Doctor asks *why you're stuck* first (scared of bad news, hate calling, "it's probably nothing", don't know which doctor, worried about cost, feeling awkward) and gives you one tiny step that fits that reason. Then it helps you actually take it.

> Not medical advice. Stuck Doctor doesn't diagnose or treat anything. It only helps you get to someone who can.

Built at **Hacktoberfest 2026**.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR-REAL-USERNAME/Stuck_Doctor/blob/main/Stuck_Doctor.ipynb)

## ✨ What it does

- **Diagnoses your "stuck"**: names the kind of avoidance you're in, kindly
- **2-minute first move**: one small action you can do right now
- **Picks a time for you**: choose "I'm not sure, guide me" and it suggests the best time
- **Ready-to-send message**: in English, Hinglish or Bengali
- **Questions to ask the doctor**, plus gentle "while you wait" tips and warning signs to watch for
- **Real action buttons**:
  - 💬 Opens WhatsApp with the booking message already typed
  - 📍 Opens Google Maps to find the right kind of doctor near you
  - 📅 Adds a "remind me to book" event to Google Calendar

## 🧠 How it works

1. You fill in what you're avoiding and why.
2. **Gemma** (an open-weight model by Google), running on **Ollama**, replies in structured JSON.
3. Python turns that JSON into the answer and the WhatsApp, Maps and Calendar links.
4. **Gradio** shows it all as a web app.

The AI isn't trained or changed. It's guided by a prompt, and the app turns its answer into actions.

## 🚀 Run it yourself

1. Click **Open in Colab** above.
2. Go to **Runtime → Change runtime type → T4 GPU**.
3. Click **Runtime → Run all**.
4. Open the `gradio.live` link that appears at the bottom.

The link only works while the Colab notebook is running.

## 🛠️ Built with

- [Gemma](https://ai.google.dev/gemma), the open-weight model
- [Ollama](https://ollama.com) and [ollama-python](https://github.com/ollama/ollama-python), to run the model
- [Gradio](https://gradio.app), for the web interface
- Google Colab
- AI assistance (Claude) was used to help write the code

## ⚠️ Limits

- It doesn't know real doctors or their availability. The Maps button finds real clinics; the clinic confirms timings.
- It doesn't book appointments. It gets *you* to book, which is the part people get stuck on.

## 📄 License

Code is under the MIT License. Gemma is subject to Google's Gemma terms of use.
