#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
import json
from tqdm import tqdm
import os


# # Import data

# In[2]:


# Read offers_canarias.json as a DataFrame in the folder data
df = pd.read_json('data/offers_canarias.json', encoding='utf-8')
# Add the column 'salaryOriginal' with NaN values
df['salaryOriginal'] = np.nan
# Define a custom function to access the 'label' key in a dictionary
def get_label(d):
    return d.get('label')
# Apply the custom function to the 'location' and 'category' columns
df['location'] = df['location'].apply(get_label)
df['category'] = df['category'].apply(get_label)
print(df.shape)
df.head()


# # Test connection to database

# In[3]:


# Test the connection to the database
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'test',
    'port': 3306
}

# SELECT * FROM test.jobmarket_canarias;
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()


# # Use database

# In[4]:


use_database = "USE test;"
cursor.execute(use_database)


# # Create table

# In[5]:


create_table_offers_query = '''
CREATE TABLE IF NOT EXISTS ofertas_jobmarket_canarias_21_23 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT NOT NULL,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    location VARCHAR(255),
    category VARCHAR(255),
    jobType VARCHAR(255),
    salaryOriginal VARCHAR(255),
    numberOfVacancies INT
);
'''
create_table_postings_query = '''
CREATE TABLE IF NOT EXISTS postings_jobmarket_canarias_21_23 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_posting VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    url VARCHAR(255) NOT NULL,
    titleOriginal VARCHAR(255) NOT NULL,
    site VARCHAR(255) NOT NULL,
    salaryOriginal VARCHAR(255)
);
'''

create_table_palabras_query = '''
CREATE TABLE IF NOT EXISTS palabras_jobmarket_canarias_21_23 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_posting VARCHAR(255) NOT NULL,
    palabra VARCHAR(255) NOT NULL
);
'''

cursor.execute(create_table_offers_query)
cursor.execute(create_table_postings_query)
cursor.execute(create_table_palabras_query)


# # Describe table

# In[6]:


# Describe the table
cursor.execute('DESCRIBE test.ofertas_jobmarket_canarias_21_23')
# Print the result
describe = cursor.fetchall()
# Print the column names
columns = [column[0] for column in describe]
print(columns)


# # Get salary

# In[7]:


def get_salary_to_df(df):
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
        postings = row['postings']
        for posting in postings:
            if 'salaryOriginal' in posting:
                df.loc[index, 'salaryOriginal'] = posting['salaryOriginal']
    return df
# Verify if offers_canarias_salary.csv exists
if os.path.exists('./data/offers_canarias_salary.csv'):
    # Read offers_canarias_salary.csv as a DataFrame
    df = pd.read_csv('./data/offers_canarias_salary.csv')
else:
    # Apply the function
    df = get_salary_to_df(df)
    # Write the DataFrame to a CSV file
    df.to_csv('./data/offers_canarias_salary.csv', index=False)


# # Import data to database

# In[8]:


def import_data_to_db(df):
    ids = []
    # Iterate over the rows in the DataFrame
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
        # Create an object with all the columns except "postings"
        row_data = row.drop('postings')
        row_data = row_data.to_dict()
        # Replace NaN values with None
        for key, value in row_data.items():
            if pd.isna(value):
                row_data[key] = None
        # Insert into the ofertas_jobmarket_canarias_21_23 table and get the id
        try:
            cursor.execute('INSERT INTO test.ofertas_jobmarket_canarias_21_23 ({}) VALUES ({})'.format(', '.join(row_data.keys()), ', '.join(['%s'] * len(row_data))), list(row_data.values()))
            id = cursor.lastrowid
            cnx.commit()
            # Add id to postings
            ids.append(id)
        except mysql.connector.errors.DataError:
            ids.append(None)
    return ids

# Verify if offers_canarias_db.csv exists
if os.path.exists('./data/offers_canarias_db.csv'):
    # Read offers_canarias_db.csv as a DataFrame
    df = pd.read_csv('./data/offers_canarias_db.csv')
else:
    # Import data to the database and get the ids
    ids = import_data_to_db(df)
    # Introduce ids to the DataFrame
    df['id'] = ids
    # Save the DataFrame as a CSV file
    df.to_csv('./data/offers_canarias_db.csv', index=False)


# # Get PALABRAS by function

# In[9]:


from functions.words import f_vector_palabras_json

# Define your checkpoint folder
checkpoint_folder = './data/checkpoints'
result_file = './data/offers_canarias_palabras_db.csv'

def get_palabras_from_offers(df, batch_size=1000):
    df_copy = df.copy()  # Create a copy of the DataFrame
    palabras_db = []  # Create an empty list to store the expanded data
    
    # Create the checkpoint folder if it doesn't exist
    os.makedirs(checkpoint_folder, exist_ok=True)

    checkpoint_files = os.listdir(checkpoint_folder)
    
    if checkpoint_files:
        latest_checkpoint = max(checkpoint_files, key=lambda x: int(x.split('.')[0]))
        latest_checkpoint = os.path.join(checkpoint_folder, latest_checkpoint)
        checkpoint_df = pd.read_csv(latest_checkpoint)
        start_from = len(checkpoint_df)
    else:
        start_from = 0
        checkpoint_df = pd.DataFrame()

    for index, row in tqdm(df_copy.iterrows(), total=len(df_copy), desc="Processing rows", initial=start_from):
        description = row['description']
        palabras = f_vector_palabras_json(description, "T")
        for palabra in palabras:
            palabras_db.append({'id': row['id'], 'palabra': palabra})

        if len(palabras_db) >= batch_size:
            # Save the checkpoint periodically
            checkpoint_file = os.path.join(checkpoint_folder, f'{index}.csv')
            checkpoint_df = pd.DataFrame(palabras_db)
            checkpoint_df.to_csv(checkpoint_file, index=False)
            palabras_db = []

    # Save the final result
    df_palabras = pd.DataFrame(palabras_db)
    df_palabras.to_csv(result_file, index=False)

    return df_palabras

# Verify if the result file exists
if os.path.exists(result_file):
    # Read the result file as a DataFrame
    df_palabras = pd.read_csv(result_file)
else:
    # Apply the function
    df_palabras = get_palabras_from_offers(df)


# # Insert palabras_ofertas

# In[ ]:


def import_palabras_to_db(df_palabras):
    # Iterate over the rows in the DataFrame
    for index, row in tqdm(df_palabras.iterrows(), total=len(df_palabras), desc="Processing rows"):
        # Create an object with all the columns except "postings"
        row_data = row.to_dict()
        # Replace NaN values with None
        for key, value in row_data.items():
            if pd.isna(value):
                row_data[key] = None
        # Insert into the ofertas_jobmarket_canarias_21_23 table and get the id
        try:
            cursor.execute('INSERT INTO test.palabras_jobmarket_canarias_21_23 ({}) VALUES ({})'.format(', '.join(row_data.keys()), ', '.join(['%s'] * len(row_data))), list(row_data.values()))
            cnx.commit()
        except mysql.connector.errors.DataError:
            pass
    return


# # Create postings dataframe

# In[ ]:


def create_postings(df, ids):
    # Create an empty list to store the expanded data
    expanded_data = []
    # Iterate through the original DataFrame
    for index, row in df.iterrows():
        id_value = ids[index]  # Get the id value
        if id_value == None:
            continue
        postings_list = row['postings']  # Get the list of postings
        # Iterate through the list of postings for each 'id'
        for posting in postings_list:
            posting['id_posting'] = id_value  # Add the 'id' to each posting
            expanded_data.append(posting)
    postings_df = pd.DataFrame(expanded_data)  # Create a new DataFrame from the expanded data
    return postings_df

# Create a new DataFrame from the expanded data
postings_df = create_postings(df, ids)
# Drop id from postings_df
postings_df = postings_df.drop('id', axis=1)
# Get the value of site from object
postings_df['site'] = postings_df['site'].apply(get_label)
# Show head
print(postings_df.shape)
postings_df.head()


# # Insert postings

# In[ ]:


def import_postings_to_db(postings_df):
    # Iterate over the rows in the DataFrame
    for index, row in tqdm(postings_df.iterrows(), total=len(postings_df), desc="Processing rows"):
        # Create an object with all the columns except "postings"
        row_data = row.to_dict()
        # Replace NaN values with None
        for key, value in row_data.items():
            if pd.isna(value):
                row_data[key] = None
        # Insert into the postings_jobmarket_canarias_21_23 table
        try:
            cursor.execute('INSERT INTO test.postings_jobmarket_canarias_21_23 ({}) VALUES ({})'.format(', '.join(row_data.keys()), ', '.join(['%s'] * len(row_data))), list(row_data.values()))
            cnx.commit()
        except mysql.connector.errors.DataError:
            continue
        
import_postings_to_db(postings_df)


# # Test MySQL table

# In[ ]:


import time

def timer(function=None, *args, **kwargs):
    start = time.time()
    query = function(*args, **kwargs)
    end = time.time()
    # print(f"Function: {function.__name__} Time: {end - start} seconds Query: {query} Args: {args} Kwargs: {kwargs}")
    return end - start, query.replace('\n', ' ')

def get_offers():
    query = 'SELECT * FROM test.ofertas_jobmarket_canarias_21_23'
    cursor.execute(query)
    data = cursor.fetchall()
    return query

def get_postings():
    query = 'SELECT * FROM test.postings_jobmarket_canarias_21_23'
    cursor.execute(query)
    data = cursor.fetchall()
    return query

def get_offers_and_postings():
    query = """SELECT * FROM test.ofertas_jobmarket_canarias_21_23 AS o
    INNER JOIN test.postings_jobmarket_canarias_21_23 AS p
    ON o.id = p.id
    """
    cursor.execute(query)
    data = cursor.fetchall()
    return query

def get_offer_by_id(id):
    query = f"SELECT * FROM test.ofertas_jobmarket_canarias_21_23 WHERE id = {id}"
    cursor.execute(query)
    data = cursor.fetchall()
    return query

def get_offers_by_dates(start_date, end_date):
    query = f"""SELECT * FROM test.postings_jobmarket_canarias_21_23
    WHERE date BETWEEN '{start_date}' AND '{end_date}'
    """
    cursor.execute(query)
    data = cursor.fetchall()
    return query

def get_offer_group_by_category_and_period(start_date, end_date):
    query = f"""SELECT category, count(*) FROM test.ofertas_jobmarket_canarias_21_23
    GROUP BY category
    ORDER BY 2 DESC
    """
    cursor.execute(query)
    data = cursor.fetchall()
    return query

timer(get_offers)

timer(get_postings)

timer(get_offers_and_postings)

timer(get_offer_by_id, 1)

timer(get_offers_by_dates, '2021-01-01', '2021-10-31')

timer(get_offer_group_by_category_and_period, '2021-01-01', '2021-10-31')


# # Create results table

# In[ ]:


import random

# Define a list of your testing functions
testing_functions = [
    get_offers,
    get_postings,
    get_offers_and_postings,
    lambda: get_offer_by_id(1),
    lambda: get_offers_by_dates('2021-01-01', '2021-10-31'),
    lambda: get_offer_group_by_category_and_period('2021-01-01', '2021-10-31')
]

def get_function_name(func):
    if hasattr(func, '__name__'):
        return func.__name__
    else:
        return "lambda"

def test_queries(test_types, N=100):
    all_test = []
    for _ in range(N):
        random_func = random.choice(test_types)
        name = get_function_name(random_func)
        if name == 'lambda':
            name = random_func.__name__
        time, query = timer(random_func)
        all_test.append({'name': name, 'time': time, 'query': query})
    # Save the results in a DataFrame
    return pd.DataFrame(all_test).sort_values(by='query', ascending=False)

df_results = test_queries(testing_functions, 1000)
# Save to excel file
df_results.to_excel('./test/results_jobmarket_canarias_21_23.xlsx', index=False)
# Now group by the same query and get the mean time
df_results.groupby('query')['time'].mean().sort_values(ascending=False).to_excel('./test/results_jobmarket_canarias_21_23_mean.xlsx')


# In[ ]:




