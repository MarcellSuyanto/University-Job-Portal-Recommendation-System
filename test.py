import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer, util

# --- 1. Load a pre-trained sentence-transformer model ---
# This model is great for semantic similarity tasks.
model = SentenceTransformer('all-MiniLM-L6-v2')

# --- 2. Sample Job Data ---
# In a real project, this would come from your database.
jobs_data = {
    'position': [
        'Data Scientist',
        'Software Engineer (Backend)',
        'Product Manager',
        'Data Analyst',
        'Senior Python Developer'
    ],
    'description': [
        'We are looking for a data scientist to develop machine learning models. Must have experience with Python, scikit-learn, and TensorFlow. Understanding of NLP is a plus.',
        'Seeking a backend software engineer to build and maintain our server-side applications. Key technologies are Node.js, Express, and PostgreSQL. Experience with cloud services like AWS is required.',
        'The Product Manager will guide the success of a product and lead the cross-functional team that is responsible for improving it. This is a leadership role.',
        'The Data Analyst will be responsible for collecting, processing, and performing statistical analyses of data. Strong SQL and Tableau skills are a must.',
        'Join our team as a Senior Python Developer. You will be responsible for writing and testing scalable code, developing back-end components, and integrating user-facing elements. Must know Django and REST APIs.'
    ],
    'nature': [
        'Full-time',
        'Full-time',
        'Full-time',
        'Contract',
        'Remote'
    ]
}
jobs_df = pd.DataFrame(jobs_data)

# --- 3. Keyword Extraction Function (using TF-IDF) ---
def extract_keywords(descriptions, num_keywords=10):
    """
    Extracts the top keywords from a list of job descriptions using TF-IDF.
    """
    # Vectorize the text
    vectorizer = TfidfVectorizer(stop_words='english', max_features=50)
    tfidf_matrix = vectorizer.fit_transform(descriptions)
    
    # Get feature names (the keywords)
    feature_names = np.array(vectorizer.get_feature_names_out())
    
    keywords_list = []
    for doc_vector in tfidf_matrix:
        # Sort the terms in the document vector by their TF-IDF score
        sorted_indices = doc_vector.toarray().argsort()[0, ::-1]
        # Get the top N keywords
        top_indices = sorted_indices[:num_keywords]
        keywords = feature_names[top_indices]
        keywords_list.append(", ".join(keywords))
        
    return keywords_list

# Add keywords to our DataFrame
jobs_df['keywords'] = extract_keywords(jobs_df['description'])
print("--- Job Data with Extracted Keywords ---")
print(jobs_df[['position', 'keywords']])
print("\n" + "="*50 + "\n")


# --- 4. Embedding Generation ---

# Method 1: Concatenation (Your Original Idea)
def get_concatenated_embeddings(df):
    # Embed each feature separately
    position_embeddings = model.encode(df['position'].tolist())
    keywords_embeddings = model.encode(df['keywords'].tolist())
    nature_embeddings = model.encode(df['nature'].tolist())
    
    # Concatenate them into a single vector for each job
    return np.concatenate((position_embeddings, keywords_embeddings, nature_embeddings), axis=1)

# Method 2: Structured String (Recommended)
def get_structured_string_embeddings(df):
    # Create a single descriptive string for each job
    structured_strings = "Position: " + df['position'] + ". Nature: " + df['nature'] + ". Key Skills: " + df['keywords']
    
    # Embed the combined strings
    return model.encode(structured_strings.tolist())

# Choose which method to use for creating job embeddings
# job_embeddings = get_concatenated_embeddings(jobs_df) # Option 1
job_embeddings = get_structured_string_embeddings(jobs_df) # Option 2 (Recommended)

print(f"--- Embeddings Generated ---")
print(f"Shape of our job embeddings matrix: {job_embeddings.shape}")
print("(Number of jobs, embedding dimension)")
print("\n" + "="*50 + "\n")


# --- 5. User Query and Similarity Search ---
def find_best_jobs(user_query, job_embeddings_matrix, jobs_dataframe, top_n=3):
    """
    Finds the most similar jobs to a user's query.
    """
    # IMPORTANT: The user query must be embedded in the same way as the jobs.
    # For the structured string method, we just embed the query directly.
    # For concatenation, it's more complex, which is why structured strings are easier.
    query_embedding = model.encode([user_query])
    
    # Calculate cosine similarity between the user query and all job embeddings
    cosine_scores = util.cos_sim(query_embedding, job_embeddings_matrix)[0]
    
    # Get the top N scores
    top_results_indices = np.argsort(cosine_scores)[-top_n:][::-1]
    
    print(f"--- Top {top_n} Job Recommendations for query: '{user_query}' ---")
    for idx in top_results_indices:
        position = jobs_dataframe.iloc[idx]['position']
        score = cosine_scores[idx]
        print(f"{position} (Score: {score:.4f})")


# --- Run the recommendation ---
user_interest = "I am a developer who knows Python and works with web frameworks and APIs."
find_best_jobs(user_interest, job_embeddings, jobs_df)

print("\n")

user_interest_2 = "I want to work with data and machine learning."
find_best_jobs(user_interest_2, job_embeddings, jobs_df)