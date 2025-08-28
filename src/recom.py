import yaml
from get_data import get_config
import re
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


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

raw_description = """Strong programming ability, and knowledge in hands-on coding with
Machine Learning and Deep Learning paradigms;
Aim to utilize the latest AI technology to Finance and Biology;
Self discipline to learn and contribute in a research environment"""

"""
Oxbridge Economics is seeking a Marketing Associate who is creative, organized, and passionate about bridging strategic communication with compelling design. You will support our business development and client engagement efforts by producing high-quality marketing materials, coordinating events, and serving as a key liaison with potential clients and partners.
  Key Responsibilities Client Communication: Engage with prospective clients, partners, and stakeholders through email, meetings, and events to promote Oxbridge’s offerings.
Marketing Content Creation:Design and prepare decks, posters, email campaigns, social media posts, and promotional videos to support product launches and brand visibility.
Event Coordination:Organize and execute marketing events, webinars, and campaigns, including logistics, materials, and follow-up communication.
  Qualifications    Strong communication skills, both written and verbal, in English.
 Proven ability to create polished marketing materials with tools like Canva, PowerPoint, or Adobe Suite.
 An eye for design with a clear understanding of branding and business tone.
 Detail-oriented, reliable, and self-motivated with a passion for marketing and storytelling.
 Experience in social media, email marketing platforms, or video production is a plus.
  Preferred Traits    A sense of ownership and responsibility in managing tasks independently.
 Creative thinker with a strong sense of aesthetics and strategic messaging.
 Prior experience in B2B marketing or working with startups is a bonus.
"""

def process_jobs(job_title, job_desc, job_nature):
    # Change to batch encoding
    cleaned_desc = clean_job_description(job_desc)
    input_text = "Position: " + job_title + ". Industry: " + job_nature +". Details: " + cleaned_desc
    embeddings = model_to_use.encode(input_text)
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

job_embeddings = process_jobs("Deep Learning Intern", raw_description, "IT/Programming")
user_embeddings = process_input("Marketing Associate", ["marketing", "communication", "design"], "Marketing/Finance/Business")

print(f"Similarity Score: {compare_embeddings(job_embeddings, user_embeddings)}")