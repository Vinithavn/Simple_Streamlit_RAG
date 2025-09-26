import streamlit as st
import llm_response


# Session State Variables
if "filename" not in st.session_state:
    st.session_state.filename = []

#Initialization
model_options = ["Grok 4"]

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
                st.write(st.session_state.filename)

    if uploaded_files:      
        user_query = st.text_input("Ente your query")     
        selected_model = st.selectbox(
            "Choose the LLM model",
            model_options,
            index=0,
        )

        side_submit = st.button("Submit",type="primary")
        if side_submit:
            if selected_model == "Grok 4":
                st.write(llm_response.generate_grok(user_query))

            




if __name__ == "__main__":
    main()
