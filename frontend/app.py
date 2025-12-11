import streamlit as st
import requests
from pathlib import Path

st.set_page_config(page_title="Youtuber RAG Bot")

API_URL = "http://127.0.0.1:8000"

ASSETS_PATH = Path(__file__).absolute().parents[1] / "assets"
AVATAR_IMAGE = ASSETS_PATH / "image.png"


def layout():
    st.title("The Youtuber – Data Engineering Chatbot")
    text_input = st.text_input("Your message:")

    if st.button("Send") and text_input.strip():
        response = requests.post(
            f"{API_URL}/rag/query",
            json={"prompt": text_input}
        )
        if response.status_code != 200:
            st.error("API error")

    history_response = requests.get(f"{API_URL}/rag/history")
    history = history_response.json()

    st.header("Chat History")

    for msg in history:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Youtuber:** {msg['content']}")
            st.image(AVATAR_IMAGE, width=90)

    if st.button("Reset Conversation"):
        requests.post(f"{API_URL}/rag/reset")
        st.rerun()


if __name__ == "__main__":
    layout()
