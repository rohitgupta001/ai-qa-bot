#!/usr/bin/env python3
"""
AI Q&A Bot - CLI and small helper functions.

Usage (CLI):
  python app.py --ask "What is unit testing?"           # ask a single question
  python app.py --chat                                  # enter interactive chat mode
  python app.py --history                               # show saved history

Streamlit UI:
  streamlit run streamlit_app.py
"""
import os
import json
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
HISTORY_FILE = Path("history.json")

if not OPENAI_API_KEY:
    # We do not raise here to let the program show a friendly message when used.
    pass

def save_history(entry):
    history = []
    if HISTORY_FILE.exists():
        try:
            history = json.loads(HISTORY_FILE.read_text())
        except Exception:
            history = []
    history.append(entry)
    HISTORY_FILE.write_text(json.dumps(history, indent=2))

def show_history():
    if not HISTORY_FILE.exists():
        print("No history yet.")
        return
    try:
        history = json.loads(HISTORY_FILE.read_text())
    except Exception as e:
        print("Could not read history:", e)
        return
    for i, item in enumerate(history, 1):
        ts = item.get("timestamp", "")
        q = item.get("question", "")
        a = item.get("answer", "")
        print(f"--- [{i}] {ts} ---")
        print("Q:", q)
        print("A:", a)
        print()

def ask_openai(question):
    """Ask OpenAI ChatCompletion (v0.28) with a safe fallback on error."""
    if not OPENAI_API_KEY:
        return ("error", "No OPENAI_API_KEY set. Copy .env.example to .env and set your key.")

    try:
        import openai
    except ImportError:
        return ("error", "Missing package 'openai'. Run: pip install -r requirements.txt")

    openai.api_key = OPENAI_API_KEY

    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers concisely."},
                {"role": "user", "content": question}
            ],
            max_tokens=512,
            temperature=0.2,
        )
        ans = response.choices[0].message.content.strip()
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "question": question,
            "answer": ans,
            "source": "openai"
        }
        save_history(entry)
        return ("ok", ans)

    except Exception as e:
        # Log the real error into history (so you can show you handled errors)
        fallback_msg = (
            "Sorry, I couldn't reach the API. Here's a short fallback answer: "
            "Artificial Intelligence (AI) is the simulation of human intelligence in machines that are "
            "programmed to think and learn. Key areas include machine learning, natural language processing, "
            "and computer vision."
        )
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "question": question,
            "answer": fallback_msg,
            "error": str(e),
            "source": "fallback"
        }
        try:
            save_history(entry)
        except Exception:
            pass
        # Return an "ok" status so the CLI shows an answer (useful for demos)
        return ("ok", fallback_msg)

def interactive_chat():
    print("AI Q&A Bot — interactive chat. Type 'exit' or blank line to quit.")
    while True:
        q = input("\nYou: ").strip()
        if q == "" or q.lower() == "exit":
            print("Bye.")
            break
        status, ans = ask_openai(q)
        if status == "ok":
            print("\nBot:", ans)
        else:
            print("\nError:", ans)

def main():
    parser = argparse.ArgumentParser(description="AI Q&A Bot (CLI)")
    parser.add_argument("--ask", type=str, help="Ask a single question")
    parser.add_argument("--chat", action="store_true", help="Interactive chat mode")
    parser.add_argument("--history", action="store_true", help="Show saved Q/A history")
    args = parser.parse_args()

    if args.ask:
        status, ans = ask_openai(args.ask)
        if status == "ok":
            print(ans)
        else:
            print("Error:", ans)
    elif args.chat:
        interactive_chat()
    elif args.history:
        show_history()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
