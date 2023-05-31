import base64
import time

import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from util_func import scrape_table_data


st.write("""
# govgr web scraping app
""")

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

    data.to_csv("govgr_data.csv", index=False)
    # Display the resulting DataFrame
    #print(data)

## read df from github
#github_data_path = "https://raw.githubusercontent.com/Giovalentini/govgr/main/"
#df = pd.read_csv(github_data_path + 'govgr_data.csv')

# show df in app
st.dataframe(data)

# Create a button to download the DataFrame
def download_dataframe(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV file</a>'
    return href

st.dataframe(data)

if st.button('Download'):
    st.markdown(download_dataframe(data), unsafe_allow_html=True)