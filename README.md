# Tiny AI Q&A Bot

A very simple AI-powered Q&A bot for the intern assignment.  
Provides a command-line interface and a small Streamlit UI.

---

## What it does

- Ask a question (CLI or Streamlit) and get an answer from OpenAI's Chat API (gpt-3.5-turbo by default).
- Saves local history to `history.json`.
- Minimal UI available via Streamlit (`streamlit_app.py`).

---

## Files

- `app.py` — Main CLI app (ask single Q / chat / view history).
- `streamlit_app.py` — Simple Streamlit UI (optional).
- `requirements.txt` — Python requirements.
- `.env.example` — Example env file.
- `history.json` — Auto-created after first question.

---

## Setup (step-by-step)

1. Install Python 3.9+ (recommended).  
   - On Windows: use the official installer from python.org.  
   - On Mac/Linux: use your package manager.

2. Clone or create the repository:
   ```bash
   mkdir ai-qa-bot
   cd ai-qa-bot
   # create files from the assignment (or copy)
