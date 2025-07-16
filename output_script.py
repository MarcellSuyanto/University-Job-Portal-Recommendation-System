from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time
from datetime import datetime, timedelta
import pandas as pd
import sqlite3
import json

load_dotenv()
user = os.getenv("UID")
password = os.getenv("PASSWORD")

#JOB TYPE: 
# Graduate 
# Internsip 
# Temporary 
# Summer
job_type = "Internship"
print(user, password)

driver = webdriver.Chrome()
driver.get("https://www.cedars.hku.hk/netjobs")
main_page = driver.current_window_handle

# Click on Student Login
student_login = driver.find_element(By.XPATH, "//a[text()='HKU Student']")
student_login.click()

#Input email and log in
email_input = WebDriverWait(driver, timeout=10).until(
    EC.presence_of_element_located((By.ID, "email"))
)
login_button = driver.find_element(By.ID, "login_btn")

email_input.send_keys(user)
login_button.click()

#Input password
password_input = WebDriverWait(driver, timeout=10).until(
    EC.presence_of_element_located((By.ID, "passwordInput"))
)
sign_in_button = driver.find_element(By.ID, "submitButton")
password_input.send_keys(password)
sign_in_button.click()

#Trust Page
continue_button = WebDriverWait(driver, timeout=10).until(
    EC.presence_of_element_located((By.ID, "idSIButton9"))
)
continue_button.click()
#Stay Singed in page
stay_button = WebDriverWait(driver, timeout=10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @id='idSIButton9']"))
)
stay_button.click()



check_box = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//input[@type='checkbox']"))
)
check_box.click()
agree_btn = WebDriverWait(driver,10).until(
    EC.element_to_be_clickable((By.ID, "btn-agree"))
)
agree_btn.click()

time.sleep(1)
internship_button = driver.find_element(By.XPATH, f"//a[text()='{job_type} (']")
internship_button.click()


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

details[2]

#Set up a connection
conn = sqlite3.connect('jobs.db')
cursor = conn.cursor()
create_table_query = """
CREATE TABLE IF NOT EXISTS jobs (
    JobID TEXT PRIMARY KEY,
    PostingDate TEXT,
    EmploymentType TEXT,
    EmplymentMode TEXT,
    CompanyNameEng TEXT,
    CompanyNameChi TEXT, 
    NatureOfBusiness TEXT,
    OriginOfCompanyOwnership TEXT,
    NoOfEmployees TEXT,
    PositionOffered TEXT,
    NoOfVacancies TEXT,
    JobNature TEXT,
    JobDescription TEXT,
    BasicSalary TEXT,
    WorkLocatin TEXT, 
    WorkMode TEXT,
    FieldsOfStudyRequired TEXT,
    LevelOfAward TEXT,
    NoOfWorkingHoursPerDay INTEGER,
    NoOfWorkingHoursPerWeek INTEGER,
    ClosingDataForApplication TEXT,
    ApplicationShouldBeSubmittedVia TEXT,
    ApplicationDocumentsRequired TEXT
);
"""

cursor.execute(create_table_query)



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


