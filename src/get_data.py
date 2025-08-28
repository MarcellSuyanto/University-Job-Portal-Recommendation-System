from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import yaml

def initialize_driver() -> webdriver:
    options = Options()
    #options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.cedars.hku.hk/netjobs")
    return driver

def portal_login(driver, user:str, password:str, job_type:str) -> None:
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
    time.sleep(3)
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
    job_type_button = driver.find_element(By.XPATH, f"//a[text()='{job_type} (']")
    job_type_button.click()

def get_data(driver):
    main_page = driver.current_window_handle
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

def get_config():
    with open('../config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config

def output_to_csv(df:pd.DataFrame):
    df.to_csv("jobs_data.csv", index=False)

def output_to_xlsx(df:pd.DataFrame):
    df.to_excel("jobs_data.xlsx", index=False)

def output_to_json(df:pd.DataFrame):
    df.to_json("jobs_data.json", index=False)

def get_jobs(driver):  
    def clean_data(data):
        # data: list of strings corresponding to job details
        for i in range(len(data)):
            data[i] = data[i].split(':\n')
        return data

    details = []
    jobs = driver.find_elements(By.XPATH, "//table[@id='search_jobs']/tbody/tr")

    for i, job in enumerate(jobs):
        job.click()
        data = clean_data(get_data(driver))
        details.append(data)

    driver.close()
    jobs_data = []
    for job in details:
        jobs_dict = dict()
        for detail in job:
            if len(detail) == 2: 
                jobs_dict[detail[0]] = detail[1]
            elif len(detail) > 2:  
                jobs_dict[detail[0]] = ' '.join(detail[1:])
            elif len(detail) == 1:
                if detail[0] not in jobs_dict:
                    jobs_dict[detail[0]] = 1
                else:
                    jobs_dict[detail[0]] += 1
        jobs_data.append(jobs_dict)
    
    jobs_df = pd.DataFrame(jobs_data)

    config = get_config()
    output_format = config['output_format']
    match output_format:
        case 'Excel':
            output_to_xlsx(jobs_df)
        case 'CSV':
            output_to_csv(jobs_df)
        case 'JSON':
            output_to_json(jobs_df)

    
    return jobs_df
        
        


