#import keybert
#from nltk.corpus import stopwords
from get_data import *
import re
import spacy

#model = keybert.KeyBERT()
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

def clean_job_description(text):
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    doc = nlp(text)
    cleaned_tokens = []
    for token in doc:
        if not token.is_stop and token.text.strip():
            cleaned_tokens.append(token.lemma_)
    return " ".join(cleaned_tokens)

def get_tags(input_df:pd.DataFrame) -> list:
    tags = []
    job_nature = input_df['Job Nature'].replace('/', ' ') 
    #job_desc = clean_desc(input_df['Job Description'])
    job_desc = input_df['Job Description']
    pos_offered = input_df['Position Offered'] 
    nature_of_business = input_df['Nature of Business'] 

    #tags.append(model.extract_keywords(job_desc, stop_words=stopwords.words('english')))
    return tags

jobs_df = get_jobs(initialize_driver())
input_data = jobs_df[['Job ID', 'Job Nature', 'Job Description', 'Position Offered', 'Nature of Business']]
print(input_data.iloc[1]['Job Description'])
#print(get_tags(input_data.iloc[1], model))