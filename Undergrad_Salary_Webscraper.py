import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import os
from directory import FilePath

path = FilePath()
path.change_working_directory(__file__)

# See https://www.selenium.dev/documentation/webdriver/browsers/chrome/
# See https://chromedriver.chromium.org/capabilities#h.p_ID_102 for a list of options

# Todo 1 - Set up Chromedriver
URL = "https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(name="detach",
                                       value=True)
driver = webdriver.Chrome(
    # service=service,
    options=chrome_options)
driver.get(url=URL)

time.sleep(5)

# creating a dictionary
data = {}
# creating a table format for csv file
csv_data = []

# Data table - table with info on salary by undergrad degree
table_obj = driver.find_element(By.CSS_SELECTOR,"table[class='data-table']")
# Headers
col_headers = table_obj.find_elements(By.CSS_SELECTOR,'thead th')
# Create a list of the headers in the table
col_header_list = [i.text for i in col_headers]
# Count number of columns in table
col_count = len(col_headers)
# Table body (excluding headers)
table_rows = table_obj.find_elements(By.CSS_SELECTOR,'tbody tr')
# Count rows in table
row_count = len(table_rows)
# create initial increment values (i is dynamic | value_num is cell specific)
i = 0
value_num = 0

# Todo - Create a key-value pair for each column name with an empty list (JSON)
for col in range(col_count):
    data[col_header_list[i]] = []
    i += 1
print(data)

# Todo - loop through table and add values to keys in data dictionary
# Todo (continued) - write rows into a csv format
# Insert the headers into the csv_data list
csv_data.append(col_header_list)
# Loop through table body
for row in table_rows:
    # increase incrementation
    i+=1
    # create a empty list for each of the cells to be added to (CSV table - row)
    row_list = []
    # row_items = row.find_elements(By.CSS_SELECTOR,"span[class='data-table__title']")
    row_values = row.find_elements(By.CSS_SELECTOR,'td')
    for item in row_values:
        if value_num > (col_count - 1):
            value_num = 0
        header_name = col_header_list[value_num] # json specific
        cell_value = item.find_element(By.CSS_SELECTOR, "span[class='data-table__value']").text
        # add cell value into row_list (CSV table - individual cell)
        row_list.append(cell_value)
        for key,value in data.items():
            if header_name == key:
                value.append(cell_value)
        # increase cell incremen
        value_num += 1
        # print(f'header name: {header_name}')
        # print(f'cell value = {cell_value}')
    csv_data.append(row_list)

print(csv_data)

with open('college_program_salary.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)
    # for row in csv_data:
    #     writer.writerow()

# Close driver
driver.quit()


