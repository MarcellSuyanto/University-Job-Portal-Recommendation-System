from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def initialize_driver(headless) -> webdriver:
    options = Options()
    options.add_argument('--log-level=3')
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.cedars.hku.hk/netjobs")
    return driver



def portal_login(driver, user:str, password:str, job_type:str) -> None:
    # Click on Student Login

    def password_error():
        error_message = driver.find_elements(By.XPATH, "//span[@id='errorText']")
        if error_message:
            print("Password error")
            return True
        return False
    
    def username_error():
        error_message = driver.find_elements(By.XPATH, "//div[@class='error-msg']")
        if error_message:
            print("Username error")
            return True
        return False

    try:
        student_login = driver.find_element(By.XPATH, "//a[text()='HKU Student']")
        student_login.click()

        #Input email and log in
        email_input = WebDriverWait(driver, timeout=10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        login_button = driver.find_element(By.ID, "login_btn")

        email_input.send_keys(user)
        login_button.click()

        if username_error():
            driver.close()
            return "Username Error"

        #Input password
        password_input = WebDriverWait(driver, timeout=10).until(
            EC.presence_of_element_located((By.ID, "passwordInput"))
        )
        sign_in_button = driver.find_element(By.ID, "submitButton")
        password_input.send_keys(password)
        sign_in_button.click()

        if password_error():
            driver.close()
            return "Password Error"

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

        return "Successful Login"
    except Exception as e:
        print(f"An error occurred during login: {e}")
        driver.close()
        return "Login Failed"

def output_to_csv(df:pd.DataFrame):
    df.to_csv("data/jobs_data.csv", index=False)

def output_to_xlsx(df:pd.DataFrame):
    df.to_excel("data/jobs_data.xlsx", index=False)

def output_to_json(df:pd.DataFrame):
    df.to_json("data/jobs_data.json", index=False)

def get_jobs(driver, config):  
    def clean_data(data):
        # data: list of strings corresponding to job details
        for i in range(len(data)):
            data[i] = data[i].split(':\n')
        return data

    details = []
    jobs = driver.find_elements(By.XPATH, "//table[@id='search_jobs']/tbody/tr")
    main_window = driver.current_window_handle
    
    BATCH_SIZE = 5
    print(f"Found {len(jobs)} jobs. Starting batch processing (Batch Size: {BATCH_SIZE})...")

    for i in range(0, len(jobs), BATCH_SIZE):
        batch = jobs[i : i + BATCH_SIZE]
        print(f"Processing batch {i//BATCH_SIZE + 1} / {(len(jobs)-1)//BATCH_SIZE + 1}...")
        
        # Click all jobs in batch
        for job in batch:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", job)
                job.click()
                time.sleep(0.2) # Small delay to allow window trigger
            except Exception as e:
                print(f"Error clicking job: {e}")

        # Wait for windows to open
        try:
            WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        except:
            print("No new windows opened for this batch.")
            continue

        # Process opened windows
        current_handles = driver.window_handles
        popup_handles = [h for h in current_handles if h != main_window]
        pending_handles = list(popup_handles)
        
        batch_start_time = time.time()
        BATCH_TIMEOUT = 60

        while pending_handles:
            if time.time() - batch_start_time > BATCH_TIMEOUT:
                print("Batch timeout reached. Closing remaining windows.")
                for h in pending_handles:
                    try:
                        driver.switch_to.window(h)
                        driver.close()
                    except:
                        pass
                break

            processed_any = False
            for handle in list(pending_handles):
                try:
                    driver.switch_to.window(handle)
                    # Check if content is ready (non-blocking)
                    if driver.find_elements(By.XPATH, "//div[@id='content']"):
                        extract_data = driver.find_elements(By.XPATH, "//div[@id='content']//div[contains(@class, 'crow')]")
                        data = [item.text for item in extract_data if item.text.strip()]
                        
                        if data:
                            details.append(clean_data(data))
                        
                        driver.close()
                        pending_handles.remove(handle)
                        processed_any = True
                except Exception as e:
                    print(f"Error processing window: {e}")
                    if handle in pending_handles:
                        pending_handles.remove(handle)
            
            if not processed_any:
                time.sleep(0.5)
        
        driver.switch_to.window(main_window)

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

    output_format = config['output_format']
    match output_format:
        case 'Excel':
            output_to_xlsx(jobs_df)
        case 'CSV':
            output_to_csv(jobs_df)
        case 'JSON':
            output_to_json(jobs_df)

    
    return jobs_df

        
        


