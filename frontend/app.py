import streamlit as st
import requests
import os 
from dotenv import load_dotenv

load_dotenv()

URL = f"https://ragbot-ebt.azurewebsites.net/rag/query?code={os.getenv('FUNCTION_APP_API')}"

ASSISTANT_AVATAR = "assets/assistant.png"


def layout():
    st.title("The Youtuber – A cool Chatbot")
    st.caption("Ask any data engineering related question")

    st.session_state.setdefault(
        "messages", [{"role": "assistant", "content": "How can I help you?"}]
    )

    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.chat_message(
                "assistant", avatar=ASSISTANT_AVATAR#LLM
            ).write(message["content"])
        else:
            st.chat_message("user").write(message["content"])

    prompt = st.chat_input("Ask a question")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        response = requests.post(URL, json={"prompt": prompt})
        response.raise_for_status()

        data = response.json()
        answer = data.get("answer")
        source = data.get("filepath")

        st.session_state.messages.append({"role": "assistant", "content": answer})

        with st.chat_message("assistant", avatar=ASSISTANT_AVATAR): #LLM
            st.write(answer)
            if source:
                st.caption(f"Source: {source}")


if __name__ == "__main__":
    layout()
