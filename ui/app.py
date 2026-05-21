import streamlit as st
import requests
import time



headers = {
    "x-api-token": "mysecret123"
}


API_URL = "http://127.0.0.1:8000/ask"


st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)
uploaded_file = st.file_uploader(
    "Upload Document",
    type=["txt", "md", "pdf", "docx", "csv"]
)


if uploaded_file:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }

    response = requests.post(
        "http://127.0.0.1:8000/upload",
        files=files
    )

    st.success(response.json()["message"])

# if uploaded_file:

    save_path = f"data/uploads/{uploaded_file.name}"

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully")

if st.button("Extract & Index"):

    response = requests.post(
        "http://127.0.0.1:8000/reindex"
    )

    st.success(response.json()["message"])

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
                json={"question": question},
                headers=headers
            )

            data = response.json()


            st.session_state.answer = data["answer"]
            st.session_state.citations = data["citations"]

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


# Export options-Word
if st.button("Export to Word"):

    response = requests.post(
        "http://127.0.0.1:8000/export/word",
        json={
            "question": question,
            "answer": st.session_state.answer,
            "citations": st.session_state.citations
        }
    )

    with open("response.docx", "wb") as f:
        f.write(response.content)

    st.success("Word file downloaded")



# Export options-Excel
if st.button("Export to Excel"):

    response = requests.post(
        "http://127.0.0.1:8000/export/excel",
        json={
            "question": question,
            "answer": st.session_state.answer,
            "citations": st.session_state.citations
        }
    )

    with open("response.xlsx", "wb") as f:
        f.write(response.content)

    st.success("Excel file downloaded")