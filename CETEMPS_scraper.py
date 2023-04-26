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
import time

options = Options()
options.headless = False
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(10)
driver.get("http://meteorema.aquila.infn.it/tempaq/dati_noaa.html")

time.sleep(5)

for year in range(2000, 2023):
    for month in range(1, 13):
        try:
            driver.find_element_by_link_text(f"{year}_{month:02d}.txt").click()
            time.sleep(2)
        except:
            print(f"File {year}_{month:02d}.txt not found")
            continue

driver.quit()