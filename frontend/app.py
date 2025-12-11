import streamlit as st
import requests
from pathlib import Path

st.set_page_config(page_title="Youtuber RAG Bot")

API_URL = "http://127.0.0.1:8000"

# avatar image
ASSETS_PATH = Path(__file__).absolute().parents[1] / "assets"
AVATAR = ASSETS_PATH / "image.png"


def ask_api(prompt: str):
    """Send user prompt to FastAPI backend."""
    response = requests.post(f"{API_URL}/rag/query", json={"prompt": prompt})

    if response.status_code != 200:
        return {"answer": "API returned an error.", "filename": "", "filepath": ""}

    return response.json()


def layout():
    st.title("The Youtuber – Chatbot")

    user_input = st.text_input("Your message:")

    if st.button("Send") and user_input.strip():
        ask_api(user_input)

    # fetch history
    history = requests.get(f"{API_URL}/rag/history").json()

    st.header("Chat History")

    for message in history:
        if message["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            col1, col2 = st.columns([1, 9])
            with col1:
                st.image(AVATAR, width=60)
            with col2:
                st.markdown(f"**Youtuber:** {msg['content']}")

    if st.button("Reset Conversation"):
        requests.post(f"{API_URL}/rag/reset")
        st.rerun()


if __name__ == "__main__":
    layout()
