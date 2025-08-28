from get_data import get_config
import re
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import heapq


MODEL = "all-MiniLM-L6-v2"
print(f"Model in use: {MODEL}")
print("Setting up model and configuration...")

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
model_to_use = SentenceTransformer(MODEL) # all-mpnet-base-v2, best quality # all-MiniLM-l6-v2, fast and good quality
config = get_config()
print(f"Model and configuration loaded")


def clean_job_description(text):
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    doc = nlp(text)
    cleaned_tokens = []
    for token in doc:
        if not token.is_stop and token.text.strip():
            cleaned_tokens.append(token.lemma_)
    return " ".join(cleaned_tokens)

def process_job(job_title, job_desc, job_nature):
    # Change to batch encoding
    cleaned_desc = clean_job_description(job_desc)
    input_text = "Position: " + job_title + ". Industry: " + job_nature +". Details: " + cleaned_desc
    embeddings = model_to_use.encode(input_text)
    return embeddings

def process_jobs(df:pd.DataFrame):
    embeddings = dict()
    input_df = df[['Job ID','Position Offered', 'Job Description', 'Job Nature']].to_dict(orient='records')
    for job in input_df:
        job_id = job.get("Job ID", "")
        job_title = job.get("Position Offered", "")
        job_desc = job.get("Job Description", "")
        job_nature = job.get("Job Nature", "")
        embeddings[job_id] = process_job(job_title, job_desc, job_nature)
    return embeddings

def process_input(job_title, skills, industry):
    input_text = "Position: " + job_title + ". Skills: " + ", ".join(skills) + ". Industry: " + industry
    print("================================")
    print(f"Position: {job_title}")
    print(f"Skills: {', '.join(skills)}")
    print(f"Industry: {industry}")
    embeddings = model_to_use.encode(input_text)
    return embeddings


def compare_embeddings(embeddings1, embeddings2):
    print(f"Comparing embeddings...")
    return cosine_similarity([embeddings1], [embeddings2])[0][0]

# job_embeddings = process_job("Deep Learning Intern", raw_description, "IT/Programming")
# user_embeddings = process_input("Marketing Associate", ["marketing", "communication", "design"], "Marketing/Finance/Business")
job_embeddings = process_jobs(pd.read_excel("data/jobs_data.xlsx"))
user_embeddings = process_input("Marketing Associate", ["marketing", "communication", "design"], "Marketing/Finance/Business")

k = 5
scored_jobs = []
for job_id, embedding in job_embeddings.items():
    similarity = compare_embeddings(embedding, user_embeddings)
    scored_jobs.append((job_id, similarity))

top_k = heapq.nlargest(k, scored_jobs, key=lambda x: x[1])
print("Top K job recommendations:")
for job_id, score in top_k:
    print(f"Job ID: {job_id}, Similarity Score: {score}")