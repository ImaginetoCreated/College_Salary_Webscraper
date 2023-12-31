import pandas as pd
from directory import FilePath

path = FilePath()
path.change_working_directory(__file__)

# Todo - Read CSV file and create a dataframe
# create dataframe from the college_program_salary.csv file
df = pd.read_csv('college_program_salary.csv')

# view top 5 rows in dataframe
top_5 = df.head()
print('Top 5 rows in df \n',top_5)

# view last 5 rows
bottom_5 = df.tail()
print('\n\nBottom 5 rows in df\n',bottom_5)

# view df dimensions (rows, columns)
df_dimensions = df.shape
print(f'\n\ndataframe dimensions (# rows, # cols): ',df_dimensions)

# column labels
df_labels = df.columns
print('\nThe dataframe has the following column headers: \n',df_labels)

# Are there missing values in dataframe (or is there bad data)?
print('\n\n NA values or blank cells:\n', df.isna)

# medium salary
med_salary = df['Early Career Pay']
print('\n\nEarly career Median Salary\n',med_salary)

# Find College Major with Highest Starting Salaries
max_med_salary = df['Early Career Pay'].max()
print('\n\nMax Starting Early Career Salary:',max_med_salary)
# print('Max Starting Early Career Salary degree: ',max_med_salary.)
# Which college major earns the highest maximum starting median salary on average?

# .idxmax() method will give us index for the row with the largest value
id = df['Early Career Pay'].idxmax()
print('\n\nId > using .idmax() method\n',id)
# Use the .loc property to see the name of the major that corresponds to that particular row
major_row = df['Major'].loc[43]
print('\n\nview a particular major by row number: ',major_row)

# Using double square brackets can return the same as above
major_row = df['Major'][id]
print('\nUsing double square brackets to return above\n',major_row)

# Return an entire row using a single bracket
row = df.loc[id]
print('\n\nReturn an entire row using single square bracket\n',row)

# Todo - Sorting
# Column Expressions can be used with pandas df - example a simple substraction operator b/w two columns
difference = df['Mid-Career Pay'] - df['Early Career Pay']
print('\n\nNew df showing the difference between early career and mid-career pay\n'\
    ,difference)
# Pandas df also have a .subtract() method. A new pandas df is the output
difference = df['Mid-Career Pay'].subtract(df['Early Career Pay'])
print('\n\nSame output as above. Difference between early career and mid-career pay:\n',difference)

# Sorting by the highest early career pays
high_early_payers = df.sort_values('Early Career Pay')
print(high_early_payers)

