from langchain_ollama import ChatOllama
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

# Step 1: Initialize the Ollama chat model
def get_response(retriever,modelname,query):
    llm = ChatOllama(model=modelname, temperature=0)

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



