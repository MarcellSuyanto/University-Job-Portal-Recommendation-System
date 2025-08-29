from src.get_data import *
from src.recom import get_recommendations
from data.read_data import get_df

import os
import argparse
from dotenv import load_dotenv
import yaml

def get_env():
    load_dotenv()
    user = os.getenv("UID")
    password = os.getenv("PASSWORD")
    return user, password

def get_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config
"""
get_data.py

- initialize_driver()
- portal_login(driver, user, password, job_type)
- get_data(driver)
- get_jobs(driver)
"""

"""
recom.py

"""

def main():
    user, password = get_env()
    config = get_config()

    parser = argparse.ArgumentParser(description='Job Recommendation System')
    parser.add_argument('--get_data', action='store_true', help='Fetch new job data')
    args = parser.parse_args()

    if args.get_data:
        print("Scraping data")
        job_type = config['job_type']
        driver = initialize_driver(headless=config['headless'])
        portal_login(driver, user, password, job_type)
        jobs = get_jobs(driver, config) #jobs:

    # Get dataframe 
    if os.path.exists("data/jobs_data.xlsx"):
        jobs = get_df("excel")
    elif os.path.exists("data/jobs_data.json"):
        jobs = get_df("json")
    elif os.path.exists("data/jobs_data.csv"):
        jobs = get_df("csv")
    recommendations, titles = get_recommendations(jobs, config['user'], config['top_k'])
    print("Top K job recommendations:")
    for job_id, score in recommendations:
        print(f"Job ID: {job_id}, Position: {titles[job_id]}, Similarity Score: {score}")
    

if __name__ == "__main__":
    main()