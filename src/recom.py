import keybert
from nltk.corpus import stopwords
from get_data import *

model = keybert.KeyBERT()

input_data = jobs_df[['Job ID', 'Job Nature', 'Job Description', 'Position Offered', 'Nature of Business']]
print(input_data.iloc[1]['Job Description'])
print(get_tags(input_data.iloc[1], model))