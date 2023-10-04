#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[1]:


from notebooks.functions.tools import load_json
import pandas as pd
import time
from unidecode import unidecode
from nltk.corpus import stopwords


# # Import test set and dictionaries

# In[2]:


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
# with open('./data/diccionario/list_unstructured_verbs.txt', 'r') as f:
#     verbs_forms = f.read().splitlines()
with open('./data/diccionario/list_unstructured_adverbios.txt', 'r') as f:
    adverbs_forms = f.read().splitlines()
# Get the spanish stopwords with nltk
stop_words = stopwords.words('spanish')
# Cast all word to unicode
sustantives_forms = [unidecode(word) for word in sustantives_forms]


# # Fix verbs df

# In[3]:


# Delete all samples that a one of the columns is null in verbs_df
print("Before: ", verbs_df.shape)
verbs_df = verbs_df.dropna()
# Find all the verbs that have a space in the column "FORMA" and delete them
verbs_df = verbs_df[verbs_df['FORMA'].str.contains(' ') == False]
print("After: ", verbs_df.shape)
verbs_df = verbs_df.sort_values(by=['FORMA']).reset_index(drop=True)
# Get the list of verbs in the column "FORMA"
verbs_forms = verbs_df['FORMA'].tolist()


# In[4]:


# Get the index of the verbs that are in the list of verbs_forms
verb = "hara"
index = verbs_forms.index(verb)
# Get the INF value of the verb
inf = verbs_df.iloc[index]['INF']
print(inf)


# # Indexialice unstructured lists

# In[11]:


def create_index_list(unstructured_forms):
    index_list = {}
    for index, string in enumerate(unstructured_forms):
        first_letter = string[0:2]
        if first_letter not in index_list:
            index_list[first_letter] = index
    return index_list

def find_indices(string, index_list, unstructured_forms):
    if not string:  # Check if the string is empty
        return 0, len(unstructured_forms)
    first_letter = string[0]
    start_index = index_list.get(first_letter, 0)
    if first_letter == "zu":
        end_index = len(unstructured_forms)
    else:
        next_letter = chr(ord(first_letter) + 1)
        end_index = index_list.get(next_letter, len(unstructured_forms))
    return start_index, end_index

def find_indices(string, index_list, unstructured_forms):
    if not string:  # Check if the string is empty
        return 0, len(unstructured_forms)
    first_letter = string[0:2]
    start_index = index_list.get(first_letter, 0)
    if first_letter == "zu":
        end_index = len(unstructured_forms)
    else:
        next_letter = get_next_letter(first_letter, index_list)
        end_index = index_list.get(next_letter, len(unstructured_forms))
    return start_index, end_index

def get_next_letter(first_letter, index_list):
    keys_list = list(index_list.keys())
    if first_letter in keys_list:
        next_letter_index_key = keys_list.index(first_letter) + 1
        return keys_list[next_letter_index_key]
    else:
        return chr(ord(first_letter[0]) + 1)
        
    

sustantives_index_list = create_index_list(sustantives_forms)
adjectives_index_list = create_index_list(adjectives_forms)
verbs_index_list = create_index_list(verbs_forms)
print(verbs_index_list)
verbs_df.tail()


# # Clean test

# In[7]:


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

# In[8]:


def clean_word(word):
    # Delete all numbers
    word = re.sub(r"\d+", "", word)
    # Delete all accents
    word = unidecode(word.lower())
    # Remove simbols
    word = re.sub(r"[^a-z0-9ñ]", "", word)
    return word

def get_reference(descripcion_oferta, df, index, column):
    # Get the accuracy of the words in palabras_empleo_texto that are in descripcion_oferta
    error = 0
    accuracy = 0
    if column == "palabras_empleo_texto":
        list_words = df[column].iloc[index]
    else:
        list_words = df[column].iloc[index].lower().split(" ")
    
    for word in descripcion_oferta.split(" "):
        if unidecode(word) not in list_words:
            error += 1
        else:
            accuracy += 1
    return error, accuracy

def show_process_stats(end_time_process, times, palabras, metrics):
    # Print total of offers
    print("Total of offers: {:.0f}".format(len(times)))
    # Print the time process
    print("Time process: {:.2f} seg".format(end_time_process))
    # Get mean of times
    mean_time = sum(times) / len(times)
    print("Mean time: {:.2f} seg".format(mean_time))
    # Sum all the words is a list of lists
    total_words = sum(palabras)
    print("Total words: {:.0f}".format(total_words))
    # Get words per time
    words_per_time = total_words / end_time_process
    print("Words per time: {:.2f}".format(words_per_time))
    # Get the mean of er_nuevas, acc_nuevas, er_legacy, acc_legacy
    er_nuevas = sum([metric["er_nuevas"] for metric in metrics]) / len(metrics)
    acc_nuevas = sum([metric["acc_nuevas"] for metric in metrics]) / len(metrics)
    er_legacy = sum([metric["er_legacy"] for metric in metrics]) / len(metrics)
    acc_legacy = sum([metric["acc_legacy"] for metric in metrics]) / len(metrics)
    # Print the metrics
    print("Error medio producido en palabras nuevas: {:.2f}".format(er_nuevas))
    print("Precisión media obtenida en palabras nuevas: {:.2f}".format(acc_nuevas))
    print("Error medio anterio: {:.2f}".format(er_legacy))
    print("Precisión media anterior: {:.2f}".format(acc_legacy))

def get_lemma_df(word, df, unstructured_forms, index_list):
    # start, end = (0, len(unstructured_forms))
    start, end = find_indices(word, index_list, unstructured_forms)
    # Is faster to handler the exception than to check if the word is in the list
    try:
        index = unstructured_forms.index(word, start, end)
        if "LEMA" in df.columns:
            return df.iloc[index]["LEMA"]
        else:
            return df.iloc[index]["INF"]
    except:
        return None

def conditional_inference(word, df_nouns, unstructured_forms_nouns, df_adj, unstructured_forms_adj, df_verbs, unstructured_forms_verb):
    verb = get_lemma_df(word, df_verbs, unstructured_forms_verb, verbs_index_list)
    if verb == None:
        noun = get_lemma_df(word, df_nouns, unstructured_forms_nouns, sustantives_index_list)
        if noun == None:
            adjective = get_lemma_df(word, df_adj, unstructured_forms_adj, adjectives_index_list)
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
    import time
    # Create a new column in the DataFrame to store the result
    df["palabras_empleo_texto_nuevas"] = ""
    times = []
    n_palabras = []
    metrics = []
    start_time_process = time.time()
    # Iterate over the DataFrame and apply the word extraction function
    for index, description in df["descripcion_oferta"].items():
        start_time = time.time()
        # Get the list of words
        palabras_list = get_syntax(description, sustantives_df, sustantives_forms, adjectives_df, adjectives_forms, adverbs_forms ,verbs_df, verbs_forms)
        # Save palabras_list in a new column in the DataFrame, insert the full list
        df.at[index, "palabras_empleo_texto_nuevas"] = ' '.join(palabras_list).upper()
        remain_time = time.time() - start_time
        times.append(remain_time)
        n_palabras.append(len(description.split(" ")))
        er_nuevas, acc_nuevas = get_reference(description, df, index, "palabras_empleo_texto_nuevas")
        er_legacy, acc_legacy = get_reference(description, df, index, "palabras_empleo_texto")
        metrics.append({"er_nuevas": er_nuevas, "acc_nuevas": acc_nuevas, "er_legacy": er_legacy, "acc_legacy": acc_legacy})
    # Calculate and add the column with words that appear in palabras legacy but not in palabras nuevas
    df["palabras_legacy_minus_nuevas"] = df.apply(lambda row: list(set(row["palabras_empleo_texto"]) - set(row["palabras_empleo_texto_nuevas"])), axis=1)
    end_time_process = time.time() - start_time_process
    show_process_stats(end_time_process, times, n_palabras, metrics)
    return df, times, n_palabras


# # Test

# In[9]:


# Get the first 5 rows of the DataFrame and save into a new DataFrame
partial_df = test_df.iloc[0:100].copy()
# print(partial_df["descripcion_oferta"].iloc[0])
# Call the processing function with your DataFrame
partial_df, time_list, n_palabras = process_and_update_df(partial_df, sustantives_df, sustantives_forms, adjectives_df, adjectives_forms, adverbs_forms ,verbs_df, verbs_forms)
partial_df.head(5)


# # Export results

# In[ ]:


test_df.to_csv("./data/test/test_palabras_nuevas.csv", index=False)


def export_results_to_markdown(index, test_df, output_file, time):
    # Get list of words in descripcion_oferta
    descripcion_oferta = test_df["descripcion_oferta"].iloc[index]
    error, accuracy = get_reference(descripcion_oferta, test_df, index, "palabras_empleo_texto_nuevas")
    
    with open("./test/" + str(index) + "_" + output_file, "w") as md_file:
        # Write header for the section
        md_file.write(f"## Descripcion oferta: \n{test_df['descripcion_oferta'].iloc[index]}\n")
        md_file.write(f"### Total de palabras en descripción: \n{len(descripcion_oferta)}\n")
        md_file.write(f"\n")
        md_file.write(f"## Palabras nuevas: \n{test_df['palabras_empleo_texto_nuevas'].iloc[index]}\n")
        md_file.write(f"### Accuracy - palabras nuevas: \n{accuracy}\n")
        md_file.write(f"### Error - palabras nuevas: \n{error}\n")
        palabras_not_found = list(set(test_df['palabras_empleo_texto_nuevas'].iloc[index].lower().split(" ")) - set(descripcion_oferta.split(" ")))
        md_file.write(f"## Palabras nuevas no encontradas en descripción: \n{', '.join(palabras_not_found)}\n")
        md_file.write(f"\n")
        error, accuracy = get_reference(descripcion_oferta, test_df, index, "palabras_empleo_texto")
        md_file.write(f"## Palabras legacy: \n{', '.join(test_df['palabras_empleo_texto'].iloc[index])}\n")
        md_file.write(f"### Accuracy - palabras legacy: \n{accuracy}\n")
        md_file.write(f"### Error - palabras legacy: \n{error}\n")
        palabras_not_found = list(set(test_df['palabras_empleo_texto'].iloc[index]) - set(descripcion_oferta))
        md_file.write(f"## Palabras legacy no encontradas en descripción: \n{', '.join(palabras_not_found)}\n")
        md_file.write(f"\n")
        md_file.write(f"## Tiempo de ejecución: \n{time} segundos\n")
        md_file.write(f"## Relación palabras/tiempo: \n{len(descripcion_oferta)/time} palabras/segundo\n")

# Define the Markdown output file
output_file = "test.md"

# Call the function to export the results to Markdown
for index in range(0, 1):
    time = time_list[index]
    export_results_to_markdown(index, partial_df, output_file, time)

