import streamlit as st
import requests
import time

# --- CONFIGURATION ---
headers = {
    "x-api-token": "mysecret123"
}

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM STYLING ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6B7280;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: ADMIN & DATA MANAGEMENT ---
with st.sidebar:
    st.title("⚙️ Admin Panel")
    st.markdown("Manage your internal knowledge base here.")
    st.divider()

    st.subheader("1. Upload Document")
    uploaded_file = st.file_uploader(
        "Supported formats: txt, md, pdf, docx, csv",
        type=["txt", "md", "pdf", "docx", "csv"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }
        
        with st.spinner("Uploading..."):
            response = requests.post("http://127.0.0.1:8000/upload", files=files)
            st.success(response.json()["message"])

        save_path = f"data/uploads/{uploaded_file.name}"
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        st.success(f"File saved locally: {uploaded_file.name}")

    st.divider()
    
    st.subheader("2. Update Knowledge Base")
    st.markdown("Run this to process newly uploaded files.")
    if st.button("Extract & Index", type="primary", use_container_width=True):
        with st.spinner("Indexing documents..."):
            response = requests.post("http://127.0.0.1:8000/reindex")
            st.success(response.json()["message"])

# --- MAIN INTERFACE: Q&A ---
st.markdown('<div class="main-header">🤖 AI Knowledge Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Ask questions and get answers directly from your internal documents.</div>', unsafe_allow_html=True)

# Question Input Section
with st.container(border=True):
    question = st.text_input("What would you like to know?", placeholder="Type your question here...")
    
    # Use columns to keep the Ask button tight
    ask_col1, ask_col2, _ = st.columns([1, 1, 4])
    with ask_col1:
        ask_pressed = st.button("🔍 Ask", type="primary", use_container_width=True)

# Process Question
if ask_pressed:
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

            # Save to session state so it survives Streamlit reruns
            st.session_state.answer = data["answer"]
            st.session_state.citations = data["citations"]
            st.session_state.latency = data["latency_seconds"]
            st.session_state.last_question = question

# --- RESULTS & EXPORT SECTION ---
# Display only if an answer exists in the session state
if "answer" in st.session_state:
    st.divider()
    
    # 3:1 column split for main answer vs metadata/actions
    res_col1, res_col2 = st.columns([3, 1])
    
    with res_col1:
        st.subheader("Answer")
        st.info(st.session_state.answer, icon="💡")
        
        # Hide citations inside an expander to keep the UI clean
        with st.expander("📚 View Citations", expanded=False):
            for citation in st.session_state.citations:
                st.markdown(f"- {citation}")
                
    with res_col2:
        st.subheader("Metrics")
        st.metric("Latency", f"{st.session_state.latency}s")
        
        st.divider()
        st.markdown("**Export Options**")
        
        # Safely get the exact question that generated this answer
        export_question = st.session_state.get("last_question", question)
        
        if st.button("📥 Export to Word", use_container_width=True):
            with st.spinner("Generating document..."):
                response = requests.post(
                    "http://127.0.0.1:8000/export/word",
                    json={
                        "question": export_question,
                        "answer": st.session_state.answer,
                        "citations": st.session_state.citations
                    }
                )
                with open("response.docx", "wb") as f:
                    f.write(response.content)
                st.success("Word file downloaded!")

        if st.button("📥 Export to Excel", use_container_width=True):
            with st.spinner("Generating spreadsheet..."):
                response = requests.post(
                    "http://127.0.0.1:8000/export/excel",
                    json={
                        "question": export_question,
                        "answer": st.session_state.answer,
                        "citations": st.session_state.citations
                    }
                )
                with open("response.xlsx", "wb") as f:
                    f.write(response.content)
                st.success("Excel file downloaded!")