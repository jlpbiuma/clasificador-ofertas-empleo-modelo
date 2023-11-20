#!/usr/bin/env python
# coding: utf-8

# # Import neccesary libraries

# In[2]:


import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.collocations import ngrams


# # Functions

# In[3]:


import re
from unidecode import unidecode

stemmer = SnowballStemmer("spanish")
expections = ["@", r"\."]
stopwords = stopwords.words('spanish')

def clean_text(text):
    # ! EXCEPCIONES MANUALES!!!
    # Cast exceptions to "a"
    text = re.sub(r'@', 'a', text)
    # Cast from "." to ""
    text = re.sub(r'\.', '', text)
    
    # Trim the text
    text = text.strip()
    # Remove accents using unidecode, excluding 'ñ' and 'Ñ'
    text = ''.join(char if char in ('ñ', 'Ñ') else unidecode(char) for char in text)
    # Delete non-alphanumeric characters
    text = re.sub(r'[^\w\s]', ' ', text)
    # Delete additional spaces with regex
    text = re.sub(r'\s+', ' ', text).upper()
    return text

def filter_words(text):
    # Split the text by " "
    list_words = text.split(" ")
    # Delete empty strings
    list_words = list(filter(None, list_words))
    # Filter all stopwords
    return [word for word in list_words if word not in stopwords]

def get_list_stems(list_words):
    # Get stems
    return [stemmer.stem(word).upper() for word in list_words]

def get_n_gramas(list_stems, min_n_gramas, max_n_gramas):
    list_n_gramas = [" ".join(n_grama) for n in range(min_n_gramas, max_n_gramas + 1)
                     for n_grama in ngrams(list_stems, n)]
    return list_n_gramas

def calculate_forms(text, min_n_gramas=2, max_n_gramas=4):
    # First clean text
    text = clean_text(text)
    # Filter words
    list_words = filter_words(text)
    # Get list of stems
    list_stems = get_list_stems(list_words)
    # Get the n gramas
    list_n_gramas = get_n_gramas(list_stems, min_n_gramas, max_n_gramas)
    if list_n_gramas != []:
        return list_n_gramas
    else:
        return None


# # Import collocations dictionary

# In[4]:


df_collocations = pd.read_csv("./static/diccionario_collocation.csv")
list_collocations = df_collocations["FORMAS"].tolist()
df_collocations.head()


# # Import offers

# In[5]:


df_offers = pd.read_json("./data/descripcion_ofertas_infojobs_21_23.json")
df_offers.head()


# # Get COLLOCATIONS from descripcion_oferta

# In[7]:


def get_collocations(descripcion_oferta):
    # Get all forms from the description
    list_forms = calculate_forms(descripcion_oferta)
    # Find in the list of collocations
    list_collocations_found = [form for form in list_forms if form in list_collocations]
    # Get the LEMA from the collocations
    list_collocations_found = [df_collocations[df_collocations["FORMAS"] == form]["LEMA"].iloc[0] for form in list_collocations_found]
    return list_collocations_found

df_offers["COLLOCATIONS"] = df_offers["descripcion_oferta"].apply(get_collocations)


# # Save to compare the dataframe

# In[ ]:


df_offers.to_json("./data/descripcion_ofertas_infojobs_21_23_collocations.json")

