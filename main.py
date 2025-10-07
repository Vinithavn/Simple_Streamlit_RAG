import streamlit as st
from src import llm_generate,doc_processing
from styles.message_styles import style_message,chat_container_css
from src.utils import *

Chunk_size = 1000
Chunk_overalp = 100


# Session State Variables
if "filename" not in st.session_state:
    st.session_state.filename = []
if "document_chunks" not in st.session_state:
    st.session_state.document_chunks =  None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "retriever" not in st.session_state:
    st.session_state.retriever = None

def clear_text():
    st.session_state["input_text"] = ""

def clear_states():
    st.session_state.chat_history = []



def submit():
    user_query = st.session_state.user_input
    if user_query:
        st.session_state.chat_history.append({"role": "user", "text": user_query})
        st.session_state.chat_history = st.session_state.chat_history[:20]
        retriever = st.session_state.retriever
        
        context_messages = st.session_state.chat_history[-5:]
       
        combined_query = ""
        for msg in context_messages:
            prefix = "User: " if msg["role"] == "user" else "BOT: "
            combined_query += prefix + msg["text"] + "\n"
        
        combined_query += "User: " + user_query + "\n"

        
        if retriever is None:
            st.error("No document has been uploaded or processed.")
            return
        
        response = llm_generate.get_response(retriever,combined_query)

        st.session_state.chat_history.append({"role": "BOT", "text": response})

        # Clear input box
        st.session_state.user_input = ""

def main():
    with st.sidebar:
        with st.form('upload_form',clear_on_submit=True):
            uploaded_files = st.file_uploader("Upload file",
                                         type=["PDF","DOCX"],
                                         accept_multiple_files=True,
                                         )
            submitted = st.form_submit_button("Process document")
            if submitted and uploaded_files is not None:
                clear_states()
                st.session_state.filename = [file.name for file in uploaded_files]
                for file in uploaded_files:  
                    st.session_state.document_chunks = doc_processing.chunk_documents(file, Chunk_size, Chunk_overalp)
                if st.session_state.document_chunks:
                    st.session_state.retriever = doc_processing.create_retriever(st.session_state.document_chunks)
                             
    if uploaded_files and st.session_state.document_chunks:  
        st.markdown(chat_container_css(), unsafe_allow_html=True)   
        chat_container = st.container()

        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for chat in st.session_state.chat_history:
                styled_msg = style_message(chat['text'], chat['role'])
                st.markdown(styled_msg, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        
        st.markdown('<div class="fixed-input">', unsafe_allow_html=True)
        st.text_input("Your query:", key="user_input", on_change=submit)
        st.button("Submit", on_click=submit)
        st.markdown("")

            
    elif st.session_state.document_chunks == []:
        st.info("Unable to extract the text") 


if __name__ == "__main__":
    main()
