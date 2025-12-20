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
        "business_nature": str(row.get('Nature of Business', '')),
        "application_deadline": str(row.get('Application Deadline', '')),
        "posting_date": str(row.get('Posting Date', ''))
    }

def update_vector_db(df: pd.DataFrame):
    """
    Updates the vector database incrementally:
    1. Deletes jobs that are in the DB but not in the new DataFrame (old postings).
    2. Adds jobs that are in the new DataFrame but not in the DB (new postings).
    3. Ignores jobs that are already present.
    """
    print("Initializing vector database connection...")
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Initialize Chroma client with persistence
        vectorstore = Chroma(
            persist_directory=VECTOR_DB_DIR,
            embedding_function=embeddings,
            collection_name="hku_jobs"
        )
        
        # Get all existing IDs from the database
        existing_data = vectorstore.get(include=[])
        existing_ids = set(existing_data['ids'])
        
        # Ensure IDs are strings
        df['Job ID'] = df['Job ID'].astype(str)
        new_ids = set(df['Job ID'])
        
        # Calculate differences
        ids_to_delete = existing_ids - new_ids
        ids_to_add = new_ids - existing_ids
        
        print(f"Database status: {len(existing_ids)} existing jobs.")
        print(f"Update status: {len(ids_to_delete)} to delete, {len(ids_to_add)} to add.")
        
        # 1. Delete old jobs
        if ids_to_delete:
            print(f"Deleting {len(ids_to_delete)} old jobs...")
            vectorstore.delete(ids=list(ids_to_delete))
            print("Deletion complete.")
            
        # 2. Add new jobs
        if ids_to_add:
            print(f"Adding {len(ids_to_add)} new jobs...")
            
            # Filter DataFrame for only new jobs
            df_to_add = df[df['Job ID'].isin(ids_to_add)]
            
            documents = []
            doc_ids = []
            
            for _, row in df_to_add.iterrows():
                content = create_job_content(row)
                metadata = create_metadata(row)
                documents.append(Document(page_content=content, metadata=metadata))
                doc_ids.append(str(row['Job ID']))
            
            if documents:
                vectorstore.add_documents(documents=documents, ids=doc_ids)
                print(f"Successfully added {len(documents)} jobs.")
        else:
            print("No new jobs to add.")
            
    except Exception as e:
        print(f"Failed to update vector database: {e}")
