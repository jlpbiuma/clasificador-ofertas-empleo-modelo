#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[1]:


import pandas as pd
import numpy as np


# # Import RAW data

# In[2]:


filename = "./data/diccionario/frecuencia_elementos_corpes_1_0.txt"

columns = ["Forma", "Lema", "Categoria", "Frecuencia", "Frec. norm. con signos ort.", "Frec. norm. sin signos ort."]
df = pd.read_csv(filename, delimiter='\t', header=0, on_bad_lines="warn",encoding='utf-8', names=columns, skiprows=[0])

# Get only the first 3 columns
df = df.iloc[:,0:3]
# Cast columns names to unicode and uppercase
df.columns = [x.upper() for x in df.columns]
# Remove rows with NaN values
df = df.dropna()
# Remove rows with empty values
df = df[df["LEMA"] != " "]

df.head()


# # Visualize some tags see [etiquetario](./docs/etiquetario_RAE_sustantivos_adjetivos.pdf)

# In[3]:


# Get the unique values of the column "CATEGORIA"
categories = df["CATEGORIA"].unique()
# Create an empty DataFrame to store the sampled rows
sample_df = pd.DataFrame(columns=df.columns)
# Loop through each category and sample two rows without replacement
for category in categories:
    category_df = df[df["CATEGORIA"] == category]
    if len(category_df) >= 2:
        sampled_rows = category_df.sample(2, replace=False)
        sample_df = pd.concat([sample_df, sampled_rows])
# Reset the index of the resulting DataFrame
sample_df.reset_index(drop=True, inplace=True)
# Show the result
print(sample_df)


# # Get only the sustantives and adjectives see [etiquetado](./docs/etiquetario_RAE_sustantivos_adjetivos.pdf)

# In[4]:


# Extract only the column "CATEGORIA" which have the values of adjectives and sustantives
# Mirar la documentación en donde se define el tag de los sustantivos y adjetivos
sustantive_tag = "N"
adjective_tag = "A"
# Extract from the raw df DataFrame the rows with the tag "N" or "A"
print("Before: ", len(df))
df = df[df["CATEGORIA"].isin([sustantive_tag, adjective_tag])]
print("After: ", len(df))
df.head()


# # Split from sustantivo and adjetivo

# In[5]:


# Split the dataframe in sustantives and adjectives and sort by alphabetical order in FORMA and reset the index
sustantives_df = df[df["CATEGORIA"] == sustantive_tag][["LEMA", "FORMA"]]
adjectives_df = df[df["CATEGORIA"] == adjective_tag][["LEMA", "FORMA"]]
# Show the result
print(sustantives_df.head())
print(adjectives_df.head())


# # Filter, clean and delete data from dataframe

# In[6]:


import re
from unidecode import unidecode

def clean_word(word):
    # Delete all numbers
    word = re.sub(r"\d+", "", word)
    # Delete all accents
    word = unidecode(word.lower())
    # Remove simbols
    word = re.sub(r"[^a-z0-9ñ]", "", word)
    return word

def clean_and_process_df(df):
    # Remove registers with nan or empty values in the column "FORMA"
    df = df.dropna(subset=["FORMA"])
    # Apply the cleaning function to the "FORMA" and "LEMA" columns
    df["FORMA"] = df["FORMA"].apply(clean_word)
    df["LEMA"] = df["LEMA"].apply(clean_word)
    # Get all the registers with spaces in the column "FORMA" and delete them
    df = df[~df["FORMA"].str.contains(" ")]
    # Get all the registers with spaces in the column "LEMA" and delete them
    df = df[~df["LEMA"].str.contains(" ")]
    # Remove registers with nan or empty values in the column "LEMA"
    df = df.dropna(subset=["LEMA"])
    # Remove duplicates in the column "FORMA"
    df = df.drop_duplicates(subset=["FORMA"])
    # Remove rows where "LEMA" or "FORMA" are empty strings
    df = df[(df["LEMA"] != "") & (df["FORMA"] != "")]
    return df
# Clean the sustantives and adjectives DataFrames
print("Before: ", len(sustantives_df))
sustantives_df = clean_and_process_df(sustantives_df)
print("After: ", len(sustantives_df))
print("Before: ", len(adjectives_df))
adjectives_df = clean_and_process_df(adjectives_df)
print("After: ", len(adjectives_df))


# #  Delete stopwords in unstructrured data

# In[7]:


# Download stopwords in spanish and english from nltk
import nltk
nltk.download('stopwords')
# Import stopwords from nltk
from nltk.corpus import stopwords
# Get the stopwords in spanish
spanish_stopwords = stopwords.words('spanish')
# Get the stopwords in english
english_stopwords = stopwords.words('english')
# Extend into stopwords
stopwords = spanish_stopwords + english_stopwords
# Unidecode the stopwords
stopwords = [unidecode(word) for word in stopwords]
# Delete all aparitions of stopwords in the sustantives and adjectives DataFrames
sustantives_df = sustantives_df[~sustantives_df["FORMA"].isin(stopwords)]
adjectives_df = adjectives_df[~adjectives_df["FORMA"].isin(stopwords)]
# Show the result
print(sustantives_df.head())


# # Order alphabetical

# In[8]:


# Order alphabetically by "LEMA" and "FORMA" and reset the index
sustantives_df = sustantives_df.sort_values(by=["LEMA", "FORMA"]).reset_index(drop=True)
adjectives_df = adjectives_df.sort_values(by=["LEMA", "FORMA"]).reset_index(drop=True)


# # Get structure data

# In[9]:


# Show the result
sustantives_df.head(5)
# Save the DataFrames to CSV files in the folder "data/diccionario" as df_structured_sustantivos.csv and df_structured_adjetivos.csv
sustantives_df.to_csv("./data/diccionario/df_structured_sustantivos.csv", index=False)
adjectives_df.to_csv("./data/diccionario/df_structured_adjetivos.csv", index=False)


# # Get unstructured data

# In[10]:


# Get a list with all LEMAS of the sustantives and sort by alphabetical order
sustantives_lemas = list(sustantives_df["LEMA"])
# Get a list with all LEMAS of the adjetives and sort by alphabetical order
adjectives_lemas = list(adjectives_df["LEMA"])
# Show a sample of the sustantives with the format "index - lemma"
for i, lemma in enumerate(sustantives_lemas[:10]):
    print(i, lemma)
# Get a list with all FORMS of the sustantives and sort by alphabetical order
sustantives_forms = list(sustantives_df["FORMA"])
# Get a list with all FORMS of the adjetives and sort by alphabetical order
adjectives_forms = list(adjectives_df["FORMA"])
# Show a sample of the sustantives with the format "index - form"
for i, form in enumerate(sustantives_forms[:5]):
    print(i, form)
# Save in txt file as list_unstructured_sustantivos.txt and list_unstructured_adjetivos.txt
with open("./data/diccionario/list_unstructured_sustantivos.txt", "w") as f:
    f.write("\n".join(sustantives_lemas))
with open("./data/diccionario/list_unstructured_adjetivos.txt", "w") as f:
    f.write("\n".join(adjectives_lemas))


# # Test

# In[64]:


def get_syntax(words, df_nouns, unstructured_forms_nouns, df_adj, unstructured_forms_adj, estricto=False):
    # Object palabras_dict
    palabras_dict = {}
    # Object palabras_list
    palabras_list = []
    # Initialize nouns array
    nouns = []
    adjectives = []
    # Split by " "
    for word in words.split(" "):
        word = clean_word(word)
        # Verify if is a noun
        noun = get_lemma_df(word, df_nouns, unstructured_forms_nouns)
        adjective = get_lemma_df(word, df_adj, unstructured_forms_adj)
        adjectives, nouns = inference(adjective, noun, estricto, adjectives, nouns)
    palabras_dict["Sustantivos"] = nouns
    palabras_dict["Adjetivos"] = adjectives
    palabras_list = nouns + adjectives
    return palabras_dict, palabras_list

def clasify_estric_mode(adjective, noun, adjective_list, noun_list):
    if adjective is not None:
        adjective_list.append(adjective)
    elif noun is not None:
        noun_list.append(noun)
    return adjective_list, noun_list

def clasify_non_estric_mode(adjective, noun, adjective_list, noun_list):
    if noun is not None:
        noun_list.append(noun)
    if adjective is not None:
        adjective_list.append(adjective)
    return adjective_list, noun_list

def inference(adjective, noun, estricto, adjective_list, noun_list):
    if estricto:
        adjective_list, noun_list = clasify_estric_mode(adjective, noun, adjective_list, noun_list)
    else:
        adjective_list, noun_list = clasify_non_estric_mode(adjective, noun, adjective_list, noun_list)
    return adjective_list, noun_list

def get_lemma_df(word, df, unstructured_forms):
    try:
        word_index = unstructured_forms.index(word)
        return df.iloc[word_index]["LEMA"]
    except ValueError:
        return None  # Handle the case when the word is not found


# # Import and clean test data

# In[65]:


from notebooks.functions.tools import load_json
data = load_json('./data/test/test_palabras.json')
# Now cast data to a DataFrame
test_df = pd.DataFrame(data)
print(test_df.shape)
test_df.head()
# from functions.descripcion import clean_descripcion
import re

list_remove = ["www", "com","http", "https"]

def tokenize_descripcion(text):
    # Remove links (URLs) from the text using regular expressions
    text = re.sub(r'http(s)?:\s+\S+', '', text, flags=re.IGNORECASE)
    # Remove all occurrences of ".es" (case-insensitive)
    text = re.sub(r'\.es', '', text, flags=re.IGNORECASE)
    # Remove all non alpha characters from the text using regular expressions
    text = re.sub(r'[^a-zA-Z ]+', ' ', text, flags=re.IGNORECASE)
    # Remove unnecessary spaces from the text using regular expressions
    text = re.sub(r'\s+', ' ', text, flags=re.IGNORECASE)
    # Cast all words to lowercase
    text = text.lower()
    return text

def create_palabras_column(text):
    # Split the text into a list of words and filter simultaneously
    palabras = [palabra for palabra in text.split(" ") if len(palabra) > 1 and palabra not in list_remove]
    return palabras

def clean_descripcion(df):
    # tokenize the descripcion
    df['descripcion_oferta'] = df['descripcion_oferta'].apply(tokenize_descripcion)
    # Split the text into a list of words
    df['palabras_descripcion_oferta'] = df['descripcion_oferta'].apply(create_palabras_column)
    return df

def list_words(palabras_empleo_texto):
    # print(palabras_empleo_texto)
    return palabras_empleo_texto.lower().split(" ")[:-1]
test_df = clean_descripcion(test_df)
test_df['palabras_empleo_texto'] = test_df['palabras_empleo_texto'].apply(lambda x: list_words(x))


# # Test

# In[68]:


import time
import pandas as pd

# Function to process and update the DataFrame
def process_and_update_df(df, sustantives_df, sustantives_forms, adjectives_df, adjectives_forms):
    # Create empty lists to store the results
    palabras_dict_list = []
    palabras_list_all = []

    # Iterate over the DataFrame and apply the word extraction function
    for description in df["descripcion_oferta"]:
        palabras_dict, palabras_list = get_syntax(description, sustantives_df, sustantives_forms, adjectives_df, adjectives_forms)
        palabras_dict_list.append(palabras_dict)
        palabras_list_all.append(palabras_list)

    # Add the new columns to the DataFrame using .loc
    df.loc[:, "palabras_dict"] = palabras_dict_list
    df.loc[:, "palabras_list_all"] = palabras_list_all

    # Calculate and add the column with words that appear in palabras legacy but not in palabras nuevas
    df["palabras_legacy_minus_nuevas"] = df.apply(lambda row: list(set(row["palabras_empleo_texto"]) - set(row["palabras_list_all"])), axis=1)

    return df

# Function to measure time and apply the processing function
def process_and_measure_time(df, sustantives_df, sustantives_forms, adjectives_df, adjectives_forms):
    start_time = time.time()
    df = process_and_update_df(df, sustantives_df, sustantives_forms, adjectives_df, adjectives_forms)
    print("Time: ", time.time() - start_time)
    return df

# Get the first 5 rows of the DataFrame and save into a new DataFrame
test_df = test_df.iloc[0:5].copy()

# Call the processing function with your DataFrame
test_df = process_and_measure_time(test_df, sustantives_df, sustantives_forms, adjectives_df, adjectives_forms)
test_df.head(5)


# In[67]:


# Sort the "palabras_list_all" column alphabetically
test_df["palabras_list_all"] = test_df["palabras_list_all"].apply(lambda x: sorted(x))
# Sort the "palabras_empleo_texto" column alphabetically
test_df["palabras_empleo_texto"] = test_df["palabras_empleo_texto"].apply(lambda x: sorted(x))
# Sort the "palabras_legacy_minus_nuevas" column alphabetically
test_df["palabras_legacy_minus_nuevas"] = test_df["palabras_legacy_minus_nuevas"].apply(lambda x: sorted(x))
# Show palabras list all
print("Palabras nuevas: ", test_df["palabras_list_all"].iloc[0], len(test_df["palabras_list_all"].iloc[0]))
# Show palabras_empleo_texto
print("Palabras legacy: ", test_df["palabras_empleo_texto"].iloc[0], len(test_df["palabras_empleo_texto"].iloc[0]))
# Show palabras_legacy_minus_nuevas
print("Palabras no encontradas: ", test_df["palabras_legacy_minus_nuevas"].iloc[0], len(test_df["palabras_legacy_minus_nuevas"].iloc[0]))


# In[62]:


# Get the index of "alojamientos" in sustantives_forms
index = sustantives_forms.index("alojamientos")
print(index)


# In[47]:


print("Descripcion oferta: " + descriptions[0])
print()
print("Palabras legacy: " + ' '.join(palabras_empleo_texto[0]))
print()
print("Palabras nuevas: " + ' '.join(palabras_list_all[0]))
# Print the words that from palabras legacy that not appear in palabras nuevas
print()
print("Palabras legacy - Palabras nuevas: " + ' '.join(list(set(palabras_empleo_texto[0]) - set(palabras_list_all[0]))))


# In[ ]:


# Ejemplo de uso:
offer = """
En España está presente desde hace más de 25 años, con más de 130 oficinas y más de 1.800 Agentes asociados. Seleccionamos asesores inmobiliarios para nuestra oficina en calle Carvajal, con o sin experiencia.
Te ofrecemos tener tu negocio propio con la menor inversión del mercado trabajando en la empresa líder de Canarias es la mejor elección para profesionales como tu para la industria inmobiliaria y sus clientes, a través de la creación de un entorno de trabajo Sinérgico, transformando y profesionalizando esta industria.
Con RE/MAX puedes llegar a lo más alto de la profesión Inmobiliaria.
¿Qué hace un agente asociado RE/MAX?

- Calificar nuevos clientes.
- Estudia el mercado donde trabaja.
- Capta nuevos inmuebles para la venta.
- Elabora planes de marketing para los inmuebles en cartera.
- Atiende y da el seguimiento a las necesidades de sus clientes
- Aconseja financieramente a sus clientes.
- Concreta la venta de los inmuebles en cartera.
- Realiza valoraciones de valor de mercado de los inmuebles.
"""

def test_unitary(offer):
    start_time = time.time()
    palabras_dict, palabras_list = get_syntax(offer, sustantives_df, sustantives_forms, adjectives_df, adjectives_forms, estricto=True)
    print("Time: ", time.time() - start_time)
    return palabras_dict, palabras_list

