#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[ ]:


import pandas as pd


# # Import nacional offers

# In[ ]:


nacional_offers = pd.read_json('data/nacional_offers.json').dropna().reset_index(drop=True)
print(nacional_offers.shape)


# # Import estudio consejo offers

# In[ ]:


estudio_consejo_social = pd.read_json('data/estudio_consejos_social_21_23.json').dropna().reset_index(drop=True)
print(estudio_consejo_social.shape)


# # Cross by id_oferta

# In[ ]:


# Create a new df matching the offers and offers_infojobs on id_oferta and get all the columns
df = pd.merge(nacional_offers, estudio_consejo_social, left_on='id_oferta', right_on='id_oferta', how='left')
print(df.shape)
# Drop all register with null in 'id_oferta'
df = df.dropna(subset=['id_oferta','id_puesto_esco','palabras_empleo_texto'])
print(df.shape)
df.head()

