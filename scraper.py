# Description: This script scrapes the data from the website and stores it in a csv file

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

from datetime import timedelta, date, datetime
import pandas as pd
import time

options = Options()
options.headless = False
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(10)
driver.get("https://sira.artaabruzzo.it/#/stazioni-fisse") 

CURRENT_DATE = date.today()
DAYS_TO_SCRAPE = 30

try:
    partial_tables = []
    for i in range(1, DAYS_TO_SCRAPE):
        #Waiting for the table to load and storing it in a variable
        html_table = driver.find_element(By.XPATH, '//*[@id="cdk-accordion-child-1"]/div/table')

        #Waiting for half a second to let the table load and avoid getting blocked
        time.sleep(0.3)

        #Clicking on the previous-day button to load the previous-day table
        button = driver.find_element(
            By.XPATH, 
            '/html/body/app-root/main-nav/mat-sidenav-container/mat-sidenav-content/div[2]/app-stazioni-fisse/div[1]/div[1]/img[1]'
            )
        ActionChains(driver).click(button).perform()

        #Converting the table to a pandas dataframe
        pd_table = pd.read_html(html_table.get_attribute('outerHTML'))

        #Computing the date of the selected table
        selected_date = CURRENT_DATE - timedelta(days=i - 1)
        pd_table[0]['Date'] = selected_date

        #Appending the table to the list of tables
        partial_tables.append(pd_table[0])
    
    #Concatenating all the tables
    full_table = pd.concat(partial_tables)

    #Storing the table in a csv file
    full_table.to_csv(f'data.csv', index=False)
    print("Successfully scraped the data for the last 30 days")
except:
    print("Element not found")
driver.save_screenshot('screenshot.png')
driver.quit()
