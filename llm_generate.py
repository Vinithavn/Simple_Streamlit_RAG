from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

from dotenv import load_dotenv
import os
load_dotenv()  

os.environ["GOOGLE_API_KEY"]  = os.getenv("GEMINI_API")

def get_response(retriever,query):
    llm =  ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,)

    prompt = ChatPromptTemplate.from_template(
        """
        Answer the following question based only on the given context.

        <context>
        {context}
        </context>

        Question: {input}
        """
    )

    # Step 3: Create a documents chain that combines retrieved documents into the prompt
    docs_chain = create_stuff_documents_chain(llm, prompt)

    # Step 4: Create a retrieval chain by joining the retriever and the documents chain
    retrieval_chain = create_retrieval_chain(retriever, docs_chain)

    # Step 5: Query the chain with a question
    response = retrieval_chain.invoke({"input": query})

    return response["answer"]



