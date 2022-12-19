# Description: This script scrapes the data from the website and stores it in a csv file

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

options = Options()
options.headless = False
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(10)
driver.get("https://sira.artaabruzzo.it/#/stazioni-fisse") 
try:
    #Waiting for the table to load and storing it in a variable
    html_table = driver.find_element(By.XPATH, '//*[@id="cdk-accordion-child-1"]/div/table')
    #driver.find_element(By.CLASS_NAME, 'mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion')

    #Converting the table to a pandas dataframe
    pd_table = pd.read_html(html_table.get_attribute('outerHTML'))

    #Storing the table in a csv file
    pd_table[0].to_csv('data.csv', index=False)

    print("Found element")
except:
    print("Element not found")
driver.save_screenshot('screenshot.png')
driver.quit()
