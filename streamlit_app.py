import streamlit as st
from dotenv import load_dotenv
import os
from app import ask_openai, HISTORY_FILE

load_dotenv()

st.set_page_config(page_title="AI Q&A Bot", layout="centered")
st.title("Tiny AI Q&A Bot")

if "history" not in st.session_state:
    st.session_state.history = []

question = st.text_area("Ask anything:", height=120)

col1, col2 = st.columns([3,1])
with col1:
    if st.button("Ask"):
        if not question.strip():
            st.warning("Type a question first.")
        else:
            status, ans = ask_openai(question)
            if status == "ok":
                st.session_state.history.insert(0, {"q": question, "a": ans})
                st.success("Got answer (saved to local history).")
            else:
                st.error(ans)

with col2:
    if st.button("Clear UI History"):
        st.session_state.history = []

st.markdown("### Recent (session) Q/A")
for item in st.session_state.history:
    st.markdown(f"**Q:** {item['q']}")
    st.markdown(f"**A:** {item['a']}")
    st.write("---")

st.markdown("### Local saved history file")
if HISTORY_FILE.exists():
    try:
        import json
        data = json.loads(HISTORY_FILE.read_text())
        if data:
            for item in reversed(data[-5:]):  # show last 5
                st.write(f"- **{item['question']}** → {item['answer'][:200]}...")
        else:
            st.write("No saved history yet.")
    except Exception:
        st.write("Could not read history file.")
else:
    st.write("No history file found yet.")

