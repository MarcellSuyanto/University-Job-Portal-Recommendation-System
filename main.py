from src.get_data import *
from src.recom import *

import os
import pandas as pd
from dotenv import load_dotenv

def get_env():
    load_dotenv()
    user = os.getenv("UID")
    password = os.getenv("PASSWORD")
    return user, password

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
    job_type = config['job_type']

    driver = initialize_driver()
    portal_login(driver, user, password, job_type)
    jobs = get_jobs(driver)

if __name__ == "__main__":
    main()