#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[10]:


from notebooks.functions.tools import load_json
import pandas as pd
import time
from unidecode import unidecode
from nltk.corpus import stopwords


# # Import test set and dictionaries

# In[11]:


data = load_json('./data/test/test_palabras.json')
# Now cast data to a DataFrame
test_df = pd.DataFrame(data)
print(test_df.shape)
test_df.head()
sustantives_df = pd.read_csv('./data/diccionario/df_structured_sustantivos.csv')
adjectives_df = pd.read_csv('./data/diccionario/df_structured_adjetivos.csv')
adverbs_df = pd.read_csv('./data/diccionario/df_structured_adverbios.csv')
verbs_df = pd.read_csv('./data/diccionario/df_structured_verbos.csv')
# Read the txt files sustantives and adjectives
with open('./data/diccionario/list_unstructured_sustantivos.txt', 'r') as f:
    sustantives_forms = f.read().splitlines()
with open('./data/diccionario/list_unstructured_adjetivos.txt', 'r') as f:
    adjectives_forms = f.read().splitlines()
with open('./data/diccionario/list_unstructured_verbs.txt', 'r') as f:
    verbs_forms = f.read().splitlines()
with open('./data/diccionario/list_unstructured_adverbios.txt', 'r') as f:
    adverbs_forms = f.read().splitlines()
# Get the spanish stopwords with nltk
stop_words = stopwords.words('spanish')


# In[12]:


# Delete all samples that a one of the columns is null in verbs_df
print("Before: ", verbs_df.shape)
verbs_df = verbs_df.dropna()
print("After: ", verbs_df.shape)
# Get the list of verbs in the column "FORMA"
verbs_forms = verbs_df['FORMA'].tolist()


# # Clean test

# In[13]:


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

def list_words(palabras_empleo_texto):
    # print(palabras_empleo_texto)
    return palabras_empleo_texto.lower().split(" ")[:-1]

def clean_descripcion(df):
    # tokenize the descripcion
    df['descripcion_oferta'] = df['descripcion_oferta'].apply(tokenize_descripcion)
    # Split the text into a list of words
    df['palabras_descripcion_oferta'] = df['descripcion_oferta'].apply(create_palabras_column)
    # Convert the string into a list
    df['palabras_empleo_texto'] = df['palabras_empleo_texto'].apply(lambda x: list_words(x))
    return df

test_df = clean_descripcion(test_df)


# # Test functions

# In[14]:


def clean_word(word):
    # Delete all numbers
    word = re.sub(r"\d+", "", word)
    # Delete all accents
    word = unidecode(word.lower())
    # Remove simbols
    word = re.sub(r"[^a-z0-9ñ]", "", word)
    return word

def get_lemma_df(word, df, unstructured_forms):
    # Verify if the column "LEMA" exists in the df
    try:
        if "LEMA" in df.columns:
            index = unstructured_forms.index(word)
            return df.iloc[index]["LEMA"]
        else:
            index = unstructured_forms.index(word)
            return df.iloc[index]["INF"]
    except:
        return None

def conditional_inference(word, df_nouns, unstructured_forms_nouns, df_adj, unstructured_forms_adj, df_verbs, unstructured_forms_verb):
    verb = get_lemma_df(word, df_verbs, unstructured_forms_verb)
    if verb == None:
        noun = get_lemma_df(word, df_nouns, unstructured_forms_nouns)
        if noun == None:
            adjective = get_lemma_df(word, df_adj, unstructured_forms_adj)
            if adjective == None:
                return None
            else:
                return adjective
        else:
            return noun
    else:
        return verb   

def get_syntax(words, df_nouns, unstructured_forms_nouns, df_adj, unstructured_forms_adj, unstructured_forms_adv, df_verbs, unstructured_forms_verb):
    # Object palabras_list
    palabras_list = []
    # Split by " "
    for word in words.split(" "):
        word = clean_word(word)
        if word in stop_words or word in unstructured_forms_adv:
            continue
        # Verify if is a noun
        solution = conditional_inference(word, df_nouns, unstructured_forms_nouns, df_adj, unstructured_forms_adj, df_verbs, unstructured_forms_verb)
        if solution != None:
            palabras_list.append(solution)
    return palabras_list

def process_and_update_df(df, sustantives_df, sustantives_forms, adjectives_df, adjectives_forms, adverbs_forms ,verbs_df, verbs_forms):
    # Create a new column in the DataFrame to store the result
    df["palabras_list_all"] = ""
    # Iterate over the DataFrame and apply the word extraction function
    for index, description in df["descripcion_oferta"].items():
        palabras_list = get_syntax(description, sustantives_df, sustantives_forms, adjectives_df, adjectives_forms, adverbs_forms ,verbs_df, verbs_forms)
        # Save palabras_list in a new column in the DataFrame, insert the full list
        df.at[index, "palabras_list_all"] = palabras_list
        # Save palabras_dict in a new column in the DataFrame
    # Calculate and add the column with words that appear in palabras legacy but not in palabras nuevas
    df["palabras_legacy_minus_nuevas"] = df.apply(lambda row: list(set(row["palabras_empleo_texto"]) - set(row["palabras_list_all"])), axis=1)
    return df

# Function to measure time and apply the processing function
def process_and_measure_time(df, sustantives_df, sustantives_forms, adjectives_df, adjectives_forms, adverbs_forms ,verbs_df, verbs_forms):
    start_time = time.time()
    df = process_and_update_df(df, sustantives_df, sustantives_forms, adjectives_df, adjectives_forms, adverbs_forms ,verbs_df, verbs_forms)
    print("Time: ", time.time() - start_time)
    return df


# # Test

# In[15]:


# Get the first 5 rows of the DataFrame and save into a new DataFrame
test_df = test_df.iloc[0:5].copy()
# Call the processing function with your DataFrame
test_df = process_and_measure_time(test_df, sustantives_df, sustantives_forms, adjectives_df, adjectives_forms, adverbs_forms ,verbs_df, verbs_forms)
test_df.head(5)


# # Export results

# In[16]:


def get_reference(descripcion_oferta, df, index, column):
    # Get the accuracy of the words in palabras_empleo_texto that are in descripcion_oferta
    error = 0
    accuracy = 0
    for word in descripcion_oferta:
        if unidecode(word) not in df[column].iloc[index]:
            error += 1
        else:
            accuracy += 1
    return error, accuracy

def export_results_to_markdown(index, test_df, output_file):
    # Get list of words in descripcion_oferta
    descripcion_oferta = test_df["descripcion_oferta"].iloc[index].split(" ")
    error, accuracy = get_reference(descripcion_oferta, test_df, index, "palabras_list_all")
    
    with open("./test/" + str(index) + "_" + output_file, "w") as md_file:
        # Write header for the section
        md_file.write(f"**Descripcion oferta:** {test_df['descripcion_oferta'].iloc[index]}\n")
        md_file.write(f"**Total de palabras en descripción:** {len(descripcion_oferta)}\n")
        md_file.write(f"**Accuracy - palabras nuevas:** {accuracy}\n")
        md_file.write(f"**Error - palabras nuevas:** {error}\n")
        md_file.write(f"**Palabras nuevas:** {', '.join(test_df['palabras_list_all'].iloc[index])}\n")
        palabras_not_found = list(set(test_df['palabras_list_all'].iloc[index]) - set(descripcion_oferta))
        md_file.write(f"**Palabras nuevas no encontradas en descripción:** {', '.join(palabras_not_found)}\n")
        
        error, accuracy = get_reference(descripcion_oferta, test_df, index, "palabras_empleo_texto")
        md_file.write(f"**Accuracy - palabras legacy:** {accuracy}\n")
        md_file.write(f"**Error - palabras legacy:** {error}\n")
        md_file.write(f"**Palabras legacy:** {', '.join(test_df['palabras_empleo_texto'].iloc[index])}\n")
        
        palabras_not_found = list(set(test_df['palabras_empleo_texto'].iloc[index]) - set(descripcion_oferta))
        md_file.write(f"**Palabras legacy no encontradas en descripción:** {', '.join(palabras_not_found)}\n")

# Define the Markdown output file
output_file = "test.md"

# Call the function to export the results to Markdown
for index in range(0, test_df.shape[0]):
    export_results_to_markdown(index, test_df, output_file)

