#import keybert
#from nltk.corpus import stopwords
from get_data import *
import re

#model = keybert.KeyBERT()
def clean_desc(desc):
    desc = re.split(r'', desc)
    return desc

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