from src.get_data import *
from src.recom import get_recommendations
from src.vector_db import update_vector_db
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

def main():
    user, password = get_env()
    config = get_config()

    parser = argparse.ArgumentParser(description='Job Recommendation System')
    parser.add_argument('--get_data', action='store_true', help='Fetch new job data')
    parser.add_argument('--get_recs', action='store_true', help='Get job recommendations')
    args = parser.parse_args()

    # If user requests data scraping
    if args.get_data:
        print("Scraping data")
        job_type = config['job_type']
        driver = initialize_driver(headless=config['headless'])
        portal = portal_login(driver, user, password, job_type)
        match portal:
            case "Successful Login":
                print("Login successful")
                print("Scraping Jobs...")
                jobs = get_jobs(driver, config)
                print("Updating Vector Database...")
                update_vector_db(jobs)
                print("Data scraping and vector database update complete.")
            case "Password Error":
                print("Login failed: Invalid password")
                return
            case "Username Error":
                print("Login failed: Invalid username")
                return
            case "Login Failed":
                print("Login failed due to an unexpected error")
                return
            
    #if user requests recommendations
    if args.get_recs:
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