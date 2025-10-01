from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders.word_document import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS 
from langchain_google_genai import GoogleGenerativeAIEmbeddings

import tempfile


def read_pdf_file(uploaded_file):
    loader = PyPDFLoader(uploaded_file)
    documents = loader.load()
    return documents

def read_docx_file(uploaded_file):
    loader = Docx2txtLoader(uploaded_file)
    documents = loader.load()


def chunk_documents(uploaded_file, Chunk_size, Chunk_overalp):
    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}"
                    ) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name
    if uploaded_file.name.endswith(".pdf"):
        documents = read_pdf_file(tmp_file_path)
    elif uploaded_file.name.endswith(".docx"):
        documents = read_docx_file(tmp_file_path)
    else:
        return "Unable to Process Document"
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=Chunk_size,
    chunk_overlap=Chunk_overalp)
    chunks = text_splitter.split_documents(documents)
    return chunks 



def create_retriever(documents):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001")
    vectorstore = FAISS.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever()
    return retriever


