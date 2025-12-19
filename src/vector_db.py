import pandas as pd
import shutil
import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

VECTOR_DB_DIR = "data/chroma_db"

def create_job_content(row):
    # Handle potential missing values with 'N/A' or empty strings
    title = row.get('Position Offered', 'Unknown Position')
    company = row.get('Company Name (Eng)', 'Unknown Company')
    desc = row.get('Job Description', '')
    reqs = row.get('Fields of Study Required', '')
    benefits = row.get('Other Benefits', '')
    
    return f"""
    Job Title: {title}
    Company: {company}
    Description: {desc}
    Requirements: {reqs}
    Benefits: {benefits}
    """.strip()

def create_metadata(row):
    return {
        "job_id": str(row.get('Job ID', '')),
        "company": str(row.get('Company Name (Eng)', '')),
        "location": str(row.get('Work Location', '')),
        "employment_type": str(row.get('Employment Type', '')),
        "salary": str(row.get('Basic Salary', 'N/A')), 
        "business_nature": str(row.get('Nature of Business', ''))
    }

def update_vector_db(df: pd.DataFrame):
    """
    Clears the existing vector database and repopulates it with the provided DataFrame.
    """
    # 1. Clear existing database
    if os.path.exists(VECTOR_DB_DIR):
        try:
            shutil.rmtree(VECTOR_DB_DIR)
            print(f"Cleared existing vector database at {VECTOR_DB_DIR}")
        except Exception as e:
            print(f"Error clearing vector database: {e}")
    
    # 2. Prepare documents
    documents = []
    for _, row in df.iterrows():
        content = create_job_content(row)
        metadata = create_metadata(row)
        documents.append(Document(page_content=content, metadata=metadata))
    
    if not documents:
        print("No documents to index.")
        return

    # 3. Create Vector Store
    print("Creating vector database...")
    try:
        # Using HuggingFaceEmbeddings (all-MiniLM-L6-v2 is a good default)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=VECTOR_DB_DIR,
            collection_name="hku_jobs"
        )
        print(f"Vector database updated with {len(documents)} jobs.")
    except Exception as e:
        print(f"Failed to create vector database: {e}")
