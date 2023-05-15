import time
import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from util_func import scrape_table_data

if __name__ == "__main__":
    # Set the options for the ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode, without opening a browser window

    # Create an instance of the ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the initial page
    driver.get("https://keyd.gsis.gr/dsae2/iif/faces/pages/static/publicationList.xhtml#")

    # Initialize an empty DataFrame
    data = pd.DataFrame()

    i = 0
    # Scrape data from each page
    while i<3:
        print(i)
        # Extract the page source and pass it to BeautifulSoup for parsing
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Pass the function for scraping the table
        scraped_data = scrape_table_data(soup)

        if i == 0:
            data = scraped_data

        else:
            # Concatenate the new data with the existing data
            data = pd.concat([scraped_data, data], ignore_index=True)

        # Check if there is a next page
        next_page_element = driver.find_element(By.CSS_SELECTOR, "[aria-label='Next Page']")
        next_page_class = next_page_element.get_attribute("class")
        if "disabled" in next_page_class.split():
            break

        # Navigate to the next page
        next_page_element.click()

        time.sleep(2)

        i += 1

    # Close the browser and clean up the resources
    driver.quit()

    data.to_csv("govgr_data.csv")
    # Display the resulting DataFrame
    #print(data)