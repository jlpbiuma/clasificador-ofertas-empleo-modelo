#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[ ]:


import pandas as pd
import numpy as np


# # Import obtained data from API

# In[ ]:


# Read offers.json in the data folder
offers = pd.read_json('./data/formated_offers.json')
print(offers.shape)
offers.head()


# # Import offers already classified

# In[ ]:


# Read ofertas_clasificadas_infojobs_jobmarket.json in the data folder
offers_infojobs = pd.read_json('./data/estudio_fp_informatica.json')
print(offers_infojobs.shape)
# Drop registers with nan values in their columns
offers_infojobs = offers_infojobs.dropna()
print(offers_infojobs.shape)
offers_infojobs.head()


# # Match the two df frames on id_oferta into new one

# In[ ]:


# Create a new df matching the offers and offers_infojobs on id_oferta and get all the columns
df = pd.merge(offers, offers_infojobs, left_on='id_oferta', right_on='id_oferta', how='left')
print(df.shape)
# Drop all register with null in 'id_oferta'
df = df.dropna(subset=['id_oferta','id_puesto_esco','palabras_empleo_texto'])
print(df.shape)
df.head()


# In[ ]:


# Calculate the non matching offers
df['matching'] = np.where(df['id_oferta'].isnull(), 'no', 'yes')
# Show the number of matching and non matching offers
print(df['matching'].value_counts())
# Delete all non matching offers
df = df[df['matching'] == 'yes']
# Delete duplicate offers
df = df.drop_duplicates(subset='id_oferta', keep='first')
# Delete the offers with "id_puesto_esco_ull" NaN
df = df.dropna(subset=['id_puesto_esco'])
print(df.shape)
# Save to json file in the data folder
df.to_json('./test/offers_matching_nacional_fp_informatica.json', orient='records', lines=True)
df.head()

