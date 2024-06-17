# Description: This script scrapes the data from the website and stores it in a csv file

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

from datetime import timedelta, date, datetime
import pandas as pd
import time

options = Options()
options.add_argument("--window-size=1920,1200")
options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(GeckoDriverManager().install()), options=options)

driver.implicitly_wait(10)
driver.get("https://sira.artaabruzzo.it/#/stazioni-fisse") 

CURRENT_DATE = date.today()
DAYS_TO_SCRAPE = 500

partial_tables = []
try:
    for i in range(1, DAYS_TO_SCRAPE):
        last_fetched_date = ""
        #Making a copy of the current data.csv to avoid changing it

        #Waiting for the table to load and storing it in a variable
        #html_table = driver.find_element(By.XPATH, '//*[@id="cdk-accordion-child-1"]/div/table')
        html_table = driver.find_element(By.XPATH, '/html/body/app-root/main-nav/mat-sidenav-container/mat-sidenav-content/div[2]/app-stazioni-fisse/div[2]/div[2]/mat-expansion-panel[2]/div/div/table')
        #Waiting for half a second to let the table load and avoid getting blocked
        time.sleep(0.5)

        #Clicking on the previous-day button to load the previous-day table
        button = driver.find_element(
            By.XPATH,
            '/html/body/app-root/main-nav/mat-sidenav-container/mat-sidenav-content/div[2]/app-stazioni-fisse/div[1]/div[1]/img[1]'
        )
        ActionChains(driver).click(button).perform()

        #Converting the table to a pandas dataframe
        pd_table = pd.read_html(html_table.get_attribute('outerHTML'))
        print(f"Scraping data for the date: {CURRENT_DATE - timedelta(days=i - 1)}")
        #Computing the date of the selected table
        selected_date = CURRENT_DATE - timedelta(days=i - 1)
        pd_table[0]['Date'] = selected_date

        #Appending the table to the list of tables
        partial_tables.append(pd_table[0])

        #Waiting for half a second to let avoid getting blocked
        time.sleep(0.5)

    print("Successfully scraped the data for the last 30 days")
except:
    print("Element not found")

    
#Concatenating all the tables
full_table = pd.concat(partial_tables)

#Storing the table in a csv file
full_table.to_csv(f'datau.csv', index=False)

driver.save_screenshot('screenshot.png')
driver.quit()
