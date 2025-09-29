import streamlit as st
import llm_response
import doc_processing

Chunk_size = 1000
Chunk_overalp = 100


# Session State Variables
if "filename" not in st.session_state:
    st.session_state.filename = []
if "document_chunks" not in st.session_state:
    st.session_state.document_chunks =  None

#Initialization
model_options = ["Gemma","Llama","Qwen"]
model_dict = {"Gemma":"gemma3:latest",
              "Llama":"llama3",
              "Quen":"qwen3:latest"}

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
                    st.session_state.document_chunks= doc_processing.chunk_documents(file, Chunk_size, Chunk_overalp)
                    
                    
    if uploaded_files and st.session_state.document_chunks:      
        user_query = st.text_input("Ente your query")     
        selected_model = st.selectbox(
            "Choose the LLM model",
            model_options,
            index=0,
        )

        side_submit = st.button("Submit",type="primary")
        if side_submit and selected_model:
            retriever = doc_processing.create_retriever(model_dict[selected_model],st.session_state.document_chunks)
            response = llm_response.get_response(retriever,model_dict[selected_model],user_query)
            st.write(response)


if __name__ == "__main__":
    main()
