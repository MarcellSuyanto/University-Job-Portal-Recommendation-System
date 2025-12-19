import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

VECTOR_DB_DIR = "data/chroma_db"

def get_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    if not os.path.exists(VECTOR_DB_DIR):
        raise FileNotFoundError(f"Vector database not found at {VECTOR_DB_DIR}. Please run 'python main.py --get_data' first.")
        
    vectorstore = Chroma(
        persist_directory=VECTOR_DB_DIR,
        embedding_function=embeddings,
        collection_name="hku_jobs"
    )
    return vectorstore

def start_chat(model_name='openai/gpt-oss-120b:free'):
    load_dotenv()
    api_key = os.getenv("OPENROUTER_KEY")
    
    if not api_key:
        print("Error: OPENROUTER_KEY not found in environment variables.")
        print("Please set OPENROUTER_KEY in your .env file.")
        return

    print("Initializing Chatbot...")
    
    try:
        vectorstore = get_vector_store()
        # Retrieve top 5 most relevant jobs
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    except Exception as e:
        print(f"Error initializing vector store: {e}")
        return

    llm = ChatOpenAI(
        model=model_name,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.7,
        api_key=api_key
    )

    template = """
    You are a helpful career assistant for HKU students. 
    Use the following pieces of retrieved job context to answer the student's question.
    If the user asks for job recommendations, summarize the relevant jobs found in the context.
    Include the Job ID, Company Name, and a brief description in your response so the student can find them.
    If the context doesn't contain relevant information, say you couldn't find any matching jobs in the database.
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:
    """
    
    prompt = PromptTemplate(
        template=template, 
        input_variables=["context", "question"]
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print("\n--- HKU NetJobs Chatbot (Type 'quit' to exit) ---")
    while True:
        query = input("\nYou: ")
        if query.lower() in ['quit', 'exit', 'q']:
            break
        
        if not query.strip():
            continue
            
        print("Thinking...")
        try:
            response = rag_chain.invoke(query)
            print(f"\nBot: {response}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    start_chat()