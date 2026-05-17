import streamlit as st
import requests
import time


API_URL = "http://127.0.0.1:8000/ask"


st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 AI Knowledge Assistant")

st.write("Ask questions about your internal knowledge base")


# User input
question = st.text_input(
    "Enter your question"
)


if st.button("Ask"):

    if question.strip() == "":
        st.warning("Please enter a question")

    else:

        with st.spinner("Thinking..."):

            response = requests.post(
                API_URL,
                json={
                    "question": question
                }
            )

            data = response.json()

            # Display answer
            st.subheader("Answer")

            st.write(data["answer"])

            # Display citations
            st.subheader("Citations")

            for citation in data["citations"]:

                st.write(f"- {citation}")

            # Display latency
            st.subheader("Latency")

            st.write(f"{data['latency_seconds']} seconds")