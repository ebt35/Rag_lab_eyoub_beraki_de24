import streamlit as st
import requests
from dotenv import load_dotenv
import os 

load_dotenv()

st.set_page_config(page_title="Youtuber RAG Bot")

URL = f"https://ragbot-ebt.azurewebsites.net/rag/query?code={os.getenv('FUNCTION_APP_API')}"

def layout():
    st.title("The Youtuber – A cool Chatbot")
    text_input = st.text_input("Ask a question:")

    if st.button("Send") and text_input.strip():
        response = requests.post(URL, json={"prompt": text_input})

        data =response.json()

        if response.status_code != 200:
            st.error("API error")
            return
        
        answer = response.json().get("answer", "No answer returned")
        st.markdown(f"**Youtuber:** {answer}")

if __name__ == "__main__":
    layout()
