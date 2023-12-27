import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from directory import FilePath

path = FilePath()
path.change_working_directory(__file__)

# See https://www.selenium.dev/documentation/webdriver/browsers/chrome/
# See https://chromedriver.chromium.org/capabilities#h.p_ID_102 for a list of options

# Todo 1 - Driver > Set up Chromedriver
URL = "https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(name="detach",
                                       value=True)
driver = webdriver.Chrome(
    # service=service,
    options=chrome_options)
driver.get(url=URL)

# Todo 2 - Driver > class
class Webscraper():
    def __init__(self):
        self.driver = driver
    def next_page(self):
        # time.sleep(5)
        next_button = self.driver.find_element(By.CSS_SELECTOR,"a[class='pagination__btn pagination__next-btn']")
        ActionChains(driver) \
            .click(next_button) \
            .perform()
        time.sleep(5)

# Todo 3 - create an empty dictionary for json and an empty list for csv
# creating a dictionary
data = {}
# creating a table format for csv file
csv_data = []

# Todo 4 - Create a Column header list and add to csv_data list as 1st row
# Data table - table with info on salary by undergrad degree
table_obj = driver.find_element(By.CSS_SELECTOR,"table[class='data-table']")
# Headers
col_headers = table_obj.find_elements(By.CSS_SELECTOR,'thead th')
# Create a list of the headers in the table
col_header_list = [i.text for i in col_headers]
# Insert the headers into the csv_data list
csv_data.append(col_header_list)

# Todo 5 - Create a key-value pair for each column name with an empty list (JSON)
# create initial increment values (i is dynamic | value_num is cell specific)
i = 0
value_num = 0
# Count number of columns in table
col_count = len(col_headers)
# Create key-value pairs with column names as keys and empty list as values
for col in range(col_count):
    data[col_header_list[i]] = []
    i += 1

# Todo - Set up a while loop to loop through each page to scrape data
# Table Continues
table_status = True
# Webscraper class
scraper = Webscraper()

# Loop through all pages and get table data
while table_status:
    time.sleep(2)
    # Todo - Locate the Table data
    # Data table - table with info on salary by undergrad degree
    table_obj = driver.find_element(By.CSS_SELECTOR, "table[class='data-table']")
    # Table body (excluding headers)
    table_rows = table_obj.find_elements(By.CSS_SELECTOR, 'tbody tr')
    # Count rows in table
    row_count = len(table_rows)
    # Todo - Loop through table and add rows to csv_data list
    # Loop through table body
    for row in table_rows:
        # increase incrementation
        i += 1
        # create a empty list for each of the cells to be added to (CSV table - row)
        row_list = []
        # row_items = row.find_elements(By.CSS_SELECTOR,"span[class='data-table__title']")
        row_values = row.find_elements(By.CSS_SELECTOR,'td')
        for item in row_values:
            if value_num > (col_count - 1):
                value_num = 0
            header_name = col_header_list[value_num]
            cell_value = item.find_element(By.CSS_SELECTOR, "span[class='data-table__value']").text
            # Todo - Type format col 0 as int, 3-4 as float (money), and 5 as float (percent)
            if value_num == 0:
                cell_value = int(cell_value)
            elif value_num not in [1, 2, 5]:
                cell_value = float(cell_value.replace('$','').replace('-','0').replace(',',''))
            elif col_header_list[value_num] == 5:
                cell_value = float(cell_value.replace('-','').replace('%',''))/100
            # add cell value into row_list (CSV table - individual cell)
            row_list.append(cell_value)
            for key,value in data.items():
                if header_name == key:
                    value.append(cell_value)
            # increase cell incremen
            value_num += 1
        # append row_list to csv_data list
        csv_data.append(row_list)
    # Todo - Select next page, if error then no more pages and exit while loop
    try:
        scraper.next_page()
    except:
        print('No more pages')
        table_status = False


# Todo - Open up a csv file (or create if doesn't exist) and write csv_data to it
with open('college_program_salary.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)

# Todo - Ensure Driver closes when finished writing all data to csv file
# Close driver
driver.quit()