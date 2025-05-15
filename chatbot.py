from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate

from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

def main(question):
    persist_directory = './ragdb'

    vectordb = Chroma(
        persist_directory = persist_directory,
        embedding_function = OpenAIEmbeddings(model='text-embedding-3-small'),
        collection_name='chatbotdb'
    )

    retriever = vectordb.as_retriever()

    prompt = PromptTemplate.from_template("""
        You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. 
        Answer in Korean.

        #Question: 
        {question} 
        #Context: 
        {context} 

        #Answer:"""
    )

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    response = chain.invoke(question)

    return response

if __name__ == '__main__':
    result = main('삼성전자가 자체 개발한 AI 의 이름은?')
    print(result)