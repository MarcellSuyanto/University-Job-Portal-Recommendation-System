
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import pandas as pd
import sqlite3
import json

from get_data import portal_login

load_dotenv()
user = os.getenv("UID")
password = os.getenv("PASSWORD")

#JOB TYPE: 
# Graduate 
# Internsip 
# Temporary 
# Summer
job_type = "Internship"


portal_login(user, password, job_type)

yesterday = datetime.now() - timedelta(1)
yesterday = datetime.strftime(yesterday, '%Y-%m-%d')
yesterday

def clean_data(data):
    # data: list of strings corresponding to job details
    for i in range(len(data)):
        data[i] = data[i].split(':\n')
    return data
        

def get_data(driver):
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

    for window_handle in driver.window_handles:
        if window_handle != main_page:
            driver.switch_to.window(window_handle)
            break
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='content']"))
    )
    extract_data = driver.find_elements(By.XPATH, "//div[@id='content']//div[contains(@class, 'crow')]")
    data = [i.text for i in extract_data if i.text.strip()]
    
    driver.close()
    driver.switch_to.window(main_page)
    return data

details = []
jobs = driver.find_elements(By.XPATH, "//table[@id='search_jobs']/tbody/tr")

for i, job in enumerate(jobs):
    job.click()
    data = clean_data(get_data(driver))
    details.append(data)

driver.close()
    


def format_json(job):
    job_json = {}   
    for item in job:
        if len(item) >= 2:  
            key = item[0]
            value = item[1]
            job_json[key] = value
    return json.dumps(job_json)  





import nbformat

# Load the notebook
with open('get_jobs.ipynb') as f:
    notebook = nbformat.read(f, as_version=4)

# Extract code cells
code_cells = [cell.source for cell in notebook.cells if cell.cell_type == 'code']

# Write to a .py file
with open('output_script.py', 'w') as f:
    for cell in code_cells:
        f.write(cell + '\n\n')


