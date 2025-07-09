from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
def getData(user, password, job_type):
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
    internship_button = driver.find_element(By.XPATH, f"//a[text()='{job_type} (']")
    internship_button.click()