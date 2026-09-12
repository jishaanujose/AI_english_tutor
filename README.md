Here is a clean, professional `README.md` text tailored specifically for your GitHub repository.

---

# 🎓 AI English Speaking Tutor

An interactive, web-based conversational English tutor built with **Streamlit**. This application enables users to practice spoken English in real-time through voice interactions, receive dynamic voice responses from an AI teacher, and get comprehensive evaluations on grammar, vocabulary, fluency, and sentence formation.

---

## 🌟 Key Features

* **Real-time Audio Conversation:** Speak directly to the AI teacher using an embedded microphone component.
* **Instant Speech-to-Text (STT):** Powered by Groq's high-speed Whisper model for accurate voice transcription.
* **Intelligent Teacher Responses:** Conversational AI powered by Groq's LLM APIs for natural follow-up questions.
* **Voice Output (TTS):** Generates fast, natural-sounding voice responses using Kokoro TTS.
* **Detailed Performance Evaluation:** Evaluates each session and provides scores for grammar, vocabulary, fluency, sentence formation, and actionable feedback.

---

## 🛠️ Tech Stack & Architecture

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Speech-to-Text (STT):** [Groq API](https://groq.com/)
* **LLM Engine & Evaluation:** [Groq API](https://groq.com/)
* **Text-to-Speech (TTS):** [Kokoro TTS](https://github.com/hexgrad/kokoro)
* **Audio Recorder:** `audio-recorder-streamlit`

---

## 🚀 Getting Started

### 1. Prerequisites

Make sure you have **Python 3.10, 3.11, or 3.12** installed on your system.

### 2. Clone the Repository

```bash
git clone https://github.com/jishaanujose/AI_english_tutor.git
cd AI_english_tutor

```

### 3. Install System Dependencies

Kokoro TTS and PyTorch audio dependencies require system-level audio tools.

* **Linux / Ubuntu:**
```bash
sudo apt-get update && sudo apt-get install -y ffmpeg libsndfile1 portaudio19-dev

```


* **macOS:**
```bash
brew install ffmpeg portaudio

```



### 4. Install Python Dependencies

```bash
pip install -r requirements.txt

```

---

## 🔑 Environment Setup

Create a `.env` file in the root directory (or `.streamlit/secrets.toml` for Streamlit Cloud deployment) and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here

```

---

## 🏃 Running the Application

Launch the Streamlit app locally:

```bash
streamlit run app.py

```

Open your browser and navigate to `http://localhost:8501`.

---

## 📁 Repository Structure

```text
├── app.py                      # Main Streamlit UI & conversation logic
├── tutor.py                    # Session initialization & teacher persona logic
├── evaluator.py                # Post-call conversation analysis & scoring
├── groq_client.py              # STT & LLM integration via Groq
├── kokoro_tts.py               # Text-to-speech audio synthesis
├── teacher_img.png             # Teacher avatar icon
├── packages.txt                # Linux binary dependencies for cloud deployment
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation

```
