import streamlit as st
import llm_generate
import doc_processing
from styles.message_styles import style_message

Chunk_size = 1000
Chunk_overalp = 100


# Session State Variables
if "filename" not in st.session_state:
    st.session_state.filename = []
if "document_chunks" not in st.session_state:
    st.session_state.document_chunks =  None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def clear_text():
    st.session_state["input_text"] = ""

def submit():
    user_query = st.session_state.user_input
    if user_query:
        st.session_state.chat_history.append({"role": "user", "text": user_query})
        st.session_state.chat_history = st.session_state.chat_history[:20]

        context_messages = st.session_state.chat_history[-5:]
       
        combined_query = ""
        for msg in context_messages:
            prefix = "User: " if msg["role"] == "user" else "BOT: "
            combined_query += prefix + msg["text"] + "\n"
        
        # Add the current user query at the end to get the response contextually
        combined_query += "User: " + user_query + "\n"

        retriever = doc_processing.create_retriever(st.session_state.document_chunks)
        response = llm_generate.get_response(retriever,user_query)

        # Append the bot's response to history
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
                st.session_state.filename = [file.name for file in uploaded_files]
                for file in uploaded_files:  
                    st.session_state.document_chunks = doc_processing.chunk_documents(file, Chunk_size, Chunk_overalp)
                    
                    
    if uploaded_files and st.session_state.document_chunks:      
        st.text_input("Your query:", key="user_input", on_change=submit)
        st.button("Submit", on_click=submit)

        for chat in st.session_state.chat_history:
            styled_msg = style_message(chat['text'], chat['role'])
            st.markdown(styled_msg, unsafe_allow_html=True)

            
    elif st.session_state.document_chunks == []:
        st.info("Unable to extract the text")


if __name__ == "__main__":
    main()
