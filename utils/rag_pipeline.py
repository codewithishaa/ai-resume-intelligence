from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

def get_qa_chain(vector_store):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        chain_type="stuff"
    )

    return qa_chain