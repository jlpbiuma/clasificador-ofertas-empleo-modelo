#!/usr/bin/env python
# coding: utf-8

# # Import libraries and models

# In[1]:


import spacy
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
# Load the Spanish language model
nlp = spacy.load("es_core_news_sm")


# # Declare function

# In[2]:


# Function to lemmatize a verb in Spanish
def lemmatize_spanish_verb(text):
    doc = nlp(text)
    lemmatized_verb = ""
    
    for token in doc:
        print(token.text, token.pos_, token.lemma_)
        if token.pos_ == "VERB":
            lemmatized_verb = token.lemma_
            break  # Stop after finding the first verb
    
    return lemmatized_verb
verbo = "fliparás"
print(lemmatize_spanish_verb(verbo))


# In[8]:


import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import re

def get_conjugation_list(verbs):
    # Define a list of pronouns to remove
    pronouns = ["yo", "tú", "él", "nosotros", "vosotros", "ellos"]
    verbs = ''.join(verbs)
    # Remove pronouns and strip the string
    for pronoun in pronouns:
        verbs = verbs.replace(pronoun, "")
    # Remove additional spaces with regex
    verbs = re.sub(' +', ' ', verbs)
    # Split by " "
    if verbs.strip()[0] == "h":
        verbs = verbs.strip().split(" h")
        # And add the "h" again at the beginning of each element
        verbs = ["h" + verbs[i] if i > 0 else verbs[i] for i in range(len(verbs))]
    else:
        verbs = verbs.strip().split(" ")
    return verbs

def get_conjugation_imperative_list(verbs, form):
    if "Imperativo negativo" == form:
        verb = ''.join(verbs)
        # Remove the "no" and "-" from the string
        verb_forms = verb.replace("no ", " ").replace("-", "").strip().split(" ")
    else:
        verbs = ' '.join(verbs)
        # Remove "-" from the string
        verbs = verbs.replace("-", "")
        # Split by " "
        verbs = verbs.strip().split(" ")
        # Join the 0 element with the 1 element and so on
        verb_forms = [verbs[i] + verbs[i+1] for i in range(0, len(verbs), 2)]
    return verb_forms

def clasify_verb_form(verbs, form, actual_forms):
    if "Simple" == form:
        verb = ''.join(verbs)
        if "Simple" not in actual_forms:
            form = "Infinitivo simple"
            verb_forms = [verb]
        else:
            form = "Gerundio simple"
            verb_forms = [verb]
    elif "Compuesto" == form:
        verb = ''.join(verbs)
        # Remove additional spaces with regex
        verb = re.sub(' +', ' ', verb)
        if "Compuesto" not in actual_forms:
            form = "Infinitivo compuesto"
            verb_forms = [verb]
        else:
            form = "Gerundio compuesto"
            verb_forms = [verb]
    elif "Imperativo" in form:
        verb_forms = get_conjugation_imperative_list(verbs, form)
    else:
        # Create list of verbs with their conjugations
        verb_forms = get_conjugation_list(verbs)
    return form, verb_forms

def scrape_verb_conjugations(verb):
    # URL of the website to scrape
    url = f"https://www.conjugacion.es/del/verbo/{verb}.php"

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        conjugations = {}  # Dictionary to store conjugations

        # Find the element with id "gauche" that contains verb conjugation data
        gauche_div = soup.find("div", id="gauche")
        if gauche_div is not None:
            # Loop through all conjugation tenses
            for tense_div in gauche_div.find_all("div", class_="tempstab"):
                form = tense_div.find("h3", class_="tempsheader").text.strip()  # Get the tense name
                # Eliminar el imperativo negativo ya que se repite
                
                # Extract conjugation forms for the tense
                verbs = tense_div.find_all("div", class_="tempscorps")[0].stripped_strings
                # Classify the verb form
                form, verb_forms = clasify_verb_form(verbs, form, conjugations.keys())
                # Add the verb form and its conjugations to the dictionary
                conjugations[form] = verb_forms
            return conjugations
        else:
            return {}
    else:
        return {}
verbo = "aberrar"
scrape_verb_conjugations(verbo)
# Now do it for a collection of all verbs
with open("./data/diccionario/verbos-espanol.txt", "r", encoding="utf-8") as f:
    verbs = f.read().splitlines()
# For each verb, lemmatize it and scrape its conjugations
    
# # Example usage:
# verb = "tener"
# conjugation_data = scrape_verb_conjugations(verb)
# print(conjugation_data)
# palabra = "Tuvieramos"
# for time in conjugation_data:
#     if conjugation_data[time][0].find(palabra.lower()) > 0:
#         print("Tiempo encontrado: " + time)
#         break


# In[9]:

from tqdm import tqdm

with open("./data/diccionario/verbos-espanol.txt", "r", encoding="utf-8") as f:
    verbs = f.read().splitlines()

diccionario = {}
for verb in tqdm(verbs, desc="Processing verbs"):
    last_chars = verb[-2:]
    if last_chars in ["ar", "er", "ir"]:
        conjugation_data = scrape_verb_conjugations(verb)
        if conjugation_data == {}:
            continue
        diccionario[verb] = conjugation_data



# # Main

# In[ ]:


verb = "tener"
conjugation_data = scrape_verb_conjugations(verb)
# list_times = list(conjugation_data.keys())
# print(list_times)
# conjugation_data['Pretérito perfecto compuesto']
print(conjugation_data)


# In[ ]:


# Abre el archivo en modo lectura
with open('./data/diccionario/verbos-espanol-conjugaciones.txt', 'r') as archivo:
    lineas = archivo.readlines()

# Crea un diccionario para almacenar los verbos y sus conjugaciones agrupados por el patrón de infinitivo
diccionario_verbos = {}

# Inicializa variables para rastrear el verbo actual y sus conjugaciones
verbo_actual = None
conjugaciones = []

# Itera a través de las líneas del archivo
for linea in lineas:
    linea = linea.strip()
    
    # Si la línea tiene el formato de un verbo en infinitivo
    if linea.endswith("ar") or linea.endswith("er") or linea.endswith("ir"):
        # Guarda el verbo anterior y sus conjugaciones en el diccionario
        if verbo_actual:
            diccionario_verbos[verbo_actual] = conjugaciones
        # Actualiza el verbo actual y reinicia la lista de conjugaciones
        verbo_actual = linea
        conjugaciones = []
    else:
        # Agrega la conjugación a la lista
        conjugaciones.append(linea)

# Agrega el último verbo y sus conjugaciones al diccionario
if verbo_actual:
    diccionario_verbos[verbo_actual] = conjugaciones
# Save to json file
import json
with open('./data/diccionario/verbos-espanol-conjugaciones.json', 'w', encoding='utf-8') as archivo:
    json.dump(diccionario_verbos, archivo, indent=4)


# In[ ]:


# Read json file
import json
with open('./data/diccionario/verbos-espanol-conjugaciones.json', 'r', encoding='utf-8') as archivo:
    diccionario_verbos = json.load(archivo)
# Verify if this word is a verb looking for the conjugations
palabra = "Tuviéramos"
for verbo in diccionario_verbos:
    if palabra.lower() in diccionario_verbos[verbo]:
        print("Verbo encontrado: " + verbo)
        break


# In[ ]:


# Ruta al archivo de texto
diccionario_verbos_path = './data/diccionario/verbos-espanol-conjugaciones.txt'

# Palabra que deseas buscar
palabra = "tuviéramos"

def read_diccionario_verbos():
    # Abre el archivo en modo lectura (encoding='utf-8' es necesario para manejar caracteres en español)
    with open(diccionario_verbos_path, 'r', encoding='utf-8') as archivo:
        # Read and strip each line
        diccionario_verbos = [linea.strip() for linea in archivo.readlines()]
    return diccionario_verbos

def buscar_palabra(palabra, diccionario_verbos):
    # Busca la palabra en el diccionario
    if palabra in diccionario_verbos:
        print(f"La palabra '{palabra}' es un verbo")
        # Return the index
        return diccionario_verbos.index(palabra)
    else:
        print(f"La palabra '{palabra}' no es un verbo")
        
diccionario_verbos = read_diccionario_verbos()
buscar_palabra(palabra, diccionario_verbos)

