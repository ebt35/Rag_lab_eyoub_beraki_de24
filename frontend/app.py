import streamlit as st
import requests
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

URL = f"https://ragbot-ebt.azurewebsites.net/rag/query?code={os.getenv('FUNCTION_APP_API')}"
ASSISTANT_AVATAR = "assets/assistant.png"

def layout():
    st.title("The Youtuber – A cool Chatbot")
    st.caption("Ask any data engineering related questions")

    st.session_state.setdefault(
        "messages", [{"role": "assistant", "content": "How can I help you?"}]
    )

    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
                st.write(message["content"])
                if message.get("source"):
                    st.caption(f"Source: {message['source']}")
        else:
            st.chat_message("user").write(message["content"])

    prompt = st.chat_input("Ask a question")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("Thinking..."):
            response = requests.post(URL, json={"prompt": prompt})

        if response.status_code != 200:
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "Something went wrong on the server. Please try again.",
                }
            )
            st.rerun()

        data = response.json()
        answer = data.get("answer")
        source = data.get("filepath")

        source_name = Path(source).stem if source else None

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "source": source_name,
            }
        )
        st.rerun()
        
if st.button("Rensa chatt"):
    st.session_state.messages = []
    st.rerun()

if __name__ == "__main__":
    layout()
