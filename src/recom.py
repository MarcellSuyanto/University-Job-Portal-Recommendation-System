import yaml
from get_data import *
import re
import spacy
from sentence_transformers import SentenceTransformer

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
model_to_use = SentenceTransformer("all-MiniLM-L6-v2")
config = get_config()

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

raw_description = """
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

def process_input(job_title, job_desc, job_nature):
    cleaned_desc = clean_job_description(job_desc)
    input_text = "Position: " + job_title + ". Nature: " + job_nature +". Details: " + cleaned_desc
    embeddings = model_to_use.encode(input_text)
    
    return embeddings

print(process_input("Marketing Associate", raw_description, "Full-time").shape)