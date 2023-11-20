#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[1]:


import pandas as pd
import time
from nltk.corpus import stopwords
import json
import numpy as np


# # Legacy function

# In[2]:


dictionary_path = "./notebooks/josejuan-palabras-empleo-texto/data/"
stopwords = stopwords.words('spanish')

def f_vector_palabras_json(texto, palabra_generica):
    # importamos las librerías necesarias
    inicio = time.time()
    #Obtenemos las stopwords del idioma del módulo nltk
    #adverbios
    adverbios = ['ahora', 'antes', 'despues', 'tarde', 'luego', 'ayer', 'temprano', 'ya',
             'todavia', 'anteayer', 'aun', 'pronto', 'hoy', 'aqui', 'ahi', 'alli',
             'cerca', 'lejos', 'fuera', 'dentro', 'alrededor', 'aparte', 'encima',
             'debajo', 'delante', 'detras', 'asi', 'bien', 'mal', 'despacio',
             'deprisa', 'como', 'mucho', 'poco', 'muy', 'casi', 'todo', 'nada', 'algo',
             'medio', 'demasiado', 'bastante', 'mas', 'menos', 'ademas', 'incluso',
             'tambien', 'si', 'asimismo', 'no', 'tampoco', 'jamas', 'nunca', 'acaso',
             'quiza', 'quizas', 'tal', 'vez', 'mejor']
    stopwords.extend(adverbios)

    # Obtengo en un dataframe el diccionario de empleo
    with open(dictionary_path + 'diccionario_empleo.json', encoding="latin-1") as f:
        aux_emp = f.read()
    diccionario_empleo = json.loads(aux_emp)

    paso1 = time.time()
    paso2 = time.time()
    diccionario_palabra = {}
    diccionario_masc = {}
    diccionario_fem = {}
    diccionario_masc_p = {}
    diccionario_fem_p = {}
    for i in range(len(diccionario_empleo)):
        if not (isinstance(diccionario_empleo[i]['PALABRA'], float)):
            # quitar caracteres a la izquierda y la derecha (se ha omitido los símbolos + y @)
            tratar = diccionario_empleo[i]['PALABRA'].strip(r"!#$%^&*()[]{};:,./<>?\|`~-'=_·")
            tratar = tratar.strip('"')

            # quitamos el símbolo español ¡¿ºª y corregimos los acentos y letra ñ
            sin_simbolo = tratar.replace("¡", "")
            sin_simbolo = sin_simbolo.replace("»", "")
            sin_simbolo = sin_simbolo.replace("«", "")
            sin_simbolo = sin_simbolo.replace("¿", "")
            sin_simbolo = sin_simbolo.replace("°", "")
            sin_simbolo = sin_simbolo.replace("º", "")
            sin_simbolo = sin_simbolo.replace("ª", "")
            sin_simbolo = sin_simbolo.replace("á", "A")
            sin_simbolo = sin_simbolo.replace("à", "A")
            sin_simbolo = sin_simbolo.replace("À", "A")
            sin_simbolo = sin_simbolo.replace("Á", "A")
            sin_simbolo = sin_simbolo.replace("é", "E")
            sin_simbolo = sin_simbolo.replace("è", "E")
            sin_simbolo = sin_simbolo.replace("È", "E")
            sin_simbolo = sin_simbolo.replace("É", "E")
            sin_simbolo = sin_simbolo.replace("í", "I")
            sin_simbolo = sin_simbolo.replace("ì", "I")
            sin_simbolo = sin_simbolo.replace("Ì", "I")
            sin_simbolo = sin_simbolo.replace("Í", "I")
            sin_simbolo = sin_simbolo.replace("ó", "O")
            sin_simbolo = sin_simbolo.replace("ò", "O")
            sin_simbolo = sin_simbolo.replace("Ò", "O")
            sin_simbolo = sin_simbolo.replace("Ó", "O")
            sin_simbolo = sin_simbolo.replace("ú", "U")
            sin_simbolo = sin_simbolo.replace("ù", "U")
            sin_simbolo = sin_simbolo.replace("Ù", "U")
            sin_simbolo = sin_simbolo.replace("Ú", "U")
            sin_simbolo = sin_simbolo.replace("ñ", "Ñ")

            # corrección de tildes
            sin_simbolo = sin_simbolo.replace("?", "")

            # comprobamos que no sea un número
            es_numero = sin_simbolo.isdigit()

            # guardamos la palabra si no es número y no vacío
            if ((es_numero == False) and (sin_simbolo != '')):
                # sustituimos en el diccionario la palabra tratada
                palabra_final = sin_simbolo

            diccionario_palabra[palabra_final] = i

        # MASCULINO
        if ((not (isinstance(diccionario_empleo[i]['MASCULINO'], float))) & (
                str(diccionario_empleo[i]['MASCULINO']).isdigit() == False)):
            # quitamos el símbolo español ¡¿ºª y corregimos los acentos y letra ñ
            sin_simbolo = str(diccionario_empleo[i]['MASCULINO']).replace("¡", "")
            sin_simbolo = sin_simbolo.replace("»", "")
            sin_simbolo = sin_simbolo.replace("«", "")
            sin_simbolo = sin_simbolo.replace("¿", "")
            sin_simbolo = sin_simbolo.replace("°", "")
            sin_simbolo = sin_simbolo.replace("º", "")
            sin_simbolo = sin_simbolo.replace("ª", "")
            sin_simbolo = sin_simbolo.replace("á", "A")
            sin_simbolo = sin_simbolo.replace("à", "A")
            sin_simbolo = sin_simbolo.replace("À", "A")
            sin_simbolo = sin_simbolo.replace("Á", "A")
            sin_simbolo = sin_simbolo.replace("é", "E")
            sin_simbolo = sin_simbolo.replace("è", "E")
            sin_simbolo = sin_simbolo.replace("È", "E")
            sin_simbolo = sin_simbolo.replace("É", "E")
            sin_simbolo = sin_simbolo.replace("í", "I")
            sin_simbolo = sin_simbolo.replace("ì", "I")
            sin_simbolo = sin_simbolo.replace("Ì", "I")
            sin_simbolo = sin_simbolo.replace("Í", "I")
            sin_simbolo = sin_simbolo.replace("ó", "O")
            sin_simbolo = sin_simbolo.replace("ò", "O")
            sin_simbolo = sin_simbolo.replace("Ò", "O")
            sin_simbolo = sin_simbolo.replace("Ó", "O")
            sin_simbolo = sin_simbolo.replace("ú", "U")
            sin_simbolo = sin_simbolo.replace("ù", "U")
            sin_simbolo = sin_simbolo.replace("Ù", "U")
            sin_simbolo = sin_simbolo.replace("Ú", "U")
            sin_simbolo = sin_simbolo.replace("ñ", "Ñ")

            # comprobamos que no sea un número
            es_numero = sin_simbolo.isdigit()

            # guardamos la palabra si no es número y no vacío
            if ((es_numero == False) and (sin_simbolo != '')):
                # sustituimos en el diccionario la palabra tratada
                masculino_final = sin_simbolo
                diccionario_masc[masculino_final] = i

        # FEMENINO
        if ((not (isinstance(diccionario_empleo[i]['FEMENINO'], float))) & (
                str(diccionario_empleo[i]['FEMENINO']).isdigit() == False)):

            sin_simbolo = str(diccionario_empleo[i]['FEMENINO']).replace("á", "A")
            sin_simbolo = sin_simbolo.replace("á", "A")
            sin_simbolo = sin_simbolo.replace("à", "A")
            sin_simbolo = sin_simbolo.replace("À", "A")
            sin_simbolo = sin_simbolo.replace("Á", "A")
            sin_simbolo = sin_simbolo.replace("é", "E")
            sin_simbolo = sin_simbolo.replace("è", "E")
            sin_simbolo = sin_simbolo.replace("È", "E")
            sin_simbolo = sin_simbolo.replace("É", "E")
            sin_simbolo = sin_simbolo.replace("í", "I")
            sin_simbolo = sin_simbolo.replace("ì", "I")
            sin_simbolo = sin_simbolo.replace("Ì", "I")
            sin_simbolo = sin_simbolo.replace("Í", "I")
            sin_simbolo = sin_simbolo.replace("ó", "O")
            sin_simbolo = sin_simbolo.replace("ò", "O")
            sin_simbolo = sin_simbolo.replace("Ò", "O")
            sin_simbolo = sin_simbolo.replace("Ó", "O")
            sin_simbolo = sin_simbolo.replace("ú", "U")
            sin_simbolo = sin_simbolo.replace("ù", "U")
            sin_simbolo = sin_simbolo.replace("Ù", "U")
            sin_simbolo = sin_simbolo.replace("Ú", "U")
            sin_simbolo = sin_simbolo.replace("ñ", "Ñ")

            # comprobamos que no sea un número
            es_numero = sin_simbolo.isdigit()

            # guardamos la palabra si no es número y no vacío
            if ((es_numero == False) and (sin_simbolo != '')):
                # sustituimos en el diccionario la palabra tratada
                femenino_final = sin_simbolo
                diccionario_fem[femenino_final] = i

        # MASC_PLURAL
        if ((not (isinstance(diccionario_empleo[i]['MASC_PLURAL'], float))) & (
                str(diccionario_empleo[i]['MASC_PLURAL']).isdigit() == False)):

            sin_simbolo = str(diccionario_empleo[i]['MASC_PLURAL']).replace("á", "A")
            sin_simbolo = sin_simbolo.replace("à", "A")
            sin_simbolo = sin_simbolo.replace("À", "A")
            sin_simbolo = sin_simbolo.replace("Á", "A")
            sin_simbolo = sin_simbolo.replace("é", "E")
            sin_simbolo = sin_simbolo.replace("è", "E")
            sin_simbolo = sin_simbolo.replace("È", "E")
            sin_simbolo = sin_simbolo.replace("É", "E")
            sin_simbolo = sin_simbolo.replace("í", "I")
            sin_simbolo = sin_simbolo.replace("ì", "I")
            sin_simbolo = sin_simbolo.replace("Ì", "I")
            sin_simbolo = sin_simbolo.replace("Í", "I")
            sin_simbolo = sin_simbolo.replace("ó", "O")
            sin_simbolo = sin_simbolo.replace("ò", "O")
            sin_simbolo = sin_simbolo.replace("Ò", "O")
            sin_simbolo = sin_simbolo.replace("Ó", "O")
            sin_simbolo = sin_simbolo.replace("ú", "U")
            sin_simbolo = sin_simbolo.replace("ù", "U")
            sin_simbolo = sin_simbolo.replace("Ù", "U")
            sin_simbolo = sin_simbolo.replace("Ú", "U")
            sin_simbolo = sin_simbolo.replace("ñ", "Ñ")

            # comprobamos que no sea un número
            es_numero = sin_simbolo.isdigit()

            # guardamos la palabra si no es número y no vacío
            if ((es_numero == False) and (sin_simbolo != '')):
                # sustituimos en el diccionario la palabra tratada
                masc_plural_final = sin_simbolo
                diccionario_masc_p[masc_plural_final] = i

        # FEM_PLURAL
        if ((not (isinstance(diccionario_empleo[i]['FEM_PLURAL'], float))) & (
                str(diccionario_empleo[i]['FEM_PLURAL']).isdigit() == False)):

            sin_simbolo = str(diccionario_empleo[i]['FEM_PLURAL']).replace("á", "A")
            sin_simbolo = sin_simbolo.replace("à", "A")
            sin_simbolo = sin_simbolo.replace("À", "A")
            sin_simbolo = sin_simbolo.replace("Á", "A")
            sin_simbolo = sin_simbolo.replace("é", "E")
            sin_simbolo = sin_simbolo.replace("è", "E")
            sin_simbolo = sin_simbolo.replace("È", "E")
            sin_simbolo = sin_simbolo.replace("É", "E")
            sin_simbolo = sin_simbolo.replace("í", "I")
            sin_simbolo = sin_simbolo.replace("ì", "I")
            sin_simbolo = sin_simbolo.replace("Ì", "I")
            sin_simbolo = sin_simbolo.replace("Í", "I")
            sin_simbolo = sin_simbolo.replace("ó", "O")
            sin_simbolo = sin_simbolo.replace("ò", "O")
            sin_simbolo = sin_simbolo.replace("Ò", "O")
            sin_simbolo = sin_simbolo.replace("Ó", "O")
            sin_simbolo = sin_simbolo.replace("ú", "U")
            sin_simbolo = sin_simbolo.replace("ù", "U")
            sin_simbolo = sin_simbolo.replace("Ù", "U")
            sin_simbolo = sin_simbolo.replace("Ú", "U")
            sin_simbolo = sin_simbolo.replace("ñ", "Ñ")

            # comprobamos que no sea un número
            es_numero = sin_simbolo.isdigit()

            # guardamos la palabra si no es número y no vacío
            if ((es_numero == False) and (sin_simbolo != '')):
                # sustituimos en el diccionario la palabra tratada
                fem_plural_final = sin_simbolo
                diccionario_fem_p[fem_plural_final] = i

    paso3 = time.time()

    # Obtengo en un dataframe el diccionario de equivalencias
    with open(dictionary_path + 'diccionario_equivalencias.json',
              encoding="latin-1") as f:
        aux_equiv = f.read()
    diccionario_equiv = json.loads(aux_equiv)
    paso4 = time.time()
    diccionario_equiv_p = {}
    for i in range(len(diccionario_equiv)):
        if ((not (isinstance(diccionario_equiv[i]['PALABRA'], float))) & (str(diccionario_equiv[i]['PALABRA']).isdigit() == False)):
            # quitar caracteres a la izquierda y la derecha (se ha omitido los símbolos + y @)
            tratar = diccionario_equiv[i]['PALABRA'].strip(r"!#$%^&*()[]{};:,./<>?\|`~-'=_·")
            tratar = tratar.strip('"')

            # quitamos el símbolo español ¡¿ºª y corregimos los acentos y letra ñ
            sin_simbolo = tratar.replace("¡", "")
            sin_simbolo = sin_simbolo.replace("»", "")
            sin_simbolo = sin_simbolo.replace("«", "")
            sin_simbolo = sin_simbolo.replace("¿", "")
            sin_simbolo = sin_simbolo.replace("°", "")
            sin_simbolo = sin_simbolo.replace("º", "")
            sin_simbolo = sin_simbolo.replace("ª", "")
            sin_simbolo = sin_simbolo.replace("á", "A")
            sin_simbolo = sin_simbolo.replace("à", "A")
            sin_simbolo = sin_simbolo.replace("À", "A")
            sin_simbolo = sin_simbolo.replace("Á", "A")
            sin_simbolo = sin_simbolo.replace("é", "E")
            sin_simbolo = sin_simbolo.replace("è", "E")
            sin_simbolo = sin_simbolo.replace("È", "E")
            sin_simbolo = sin_simbolo.replace("É", "E")
            sin_simbolo = sin_simbolo.replace("í", "I")
            sin_simbolo = sin_simbolo.replace("ì", "I")
            sin_simbolo = sin_simbolo.replace("Ì", "I")
            sin_simbolo = sin_simbolo.replace("Í", "I")
            sin_simbolo = sin_simbolo.replace("ó", "O")
            sin_simbolo = sin_simbolo.replace("ò", "O")
            sin_simbolo = sin_simbolo.replace("Ò", "O")
            sin_simbolo = sin_simbolo.replace("Ó", "O")
            sin_simbolo = sin_simbolo.replace("ú", "U")
            sin_simbolo = sin_simbolo.replace("ù", "U")
            sin_simbolo = sin_simbolo.replace("Ù", "U")
            sin_simbolo = sin_simbolo.replace("Ú", "U")
            sin_simbolo = sin_simbolo.replace("ñ", "Ñ")

            # corrección de tildes
            sin_simbolo = sin_simbolo.replace("?", "")

            # comprobamos que no sea un número
            es_numero = sin_simbolo.isdigit()

            # guardamos la palabra si no es número y no vacío
            if ((es_numero == False) and (sin_simbolo != '')):
                # sustituimos en el diccionario la palabra tratada
                equivalencia_palabra = sin_simbolo
                diccionario_equiv_p[equivalencia_palabra] = i

    paso5 = time.time()

    vector_palabras = list()

    lista_palabras = str(texto).lower()
    palabras = lista_palabras.split()
    filtered_words = [word for word in palabras if word not in stopwords]

    table = {33: 32, 35: 32, 36: 32, 37: 32, 94: 32, 38: 32, 42: 32, 40: 32, 41: 32, 91: 32, 93: 32,
             123: 32, 125: 32, 58: 32, 59: 32, 44: 32, 47: 32, 60: 32, 62: 32, 92: 32, 124: 32, 96: 32,
             126: 32, 45: 32, 34: 32, 39: 32, 61: 32, 95: 32, 43: 32}

    palabras_encontradas = []

    for j in range(len(filtered_words)):
        sin_simbolo = filtered_words[j].replace("¡", "")
        sin_simbolo = sin_simbolo.replace("»", "")
        sin_simbolo = sin_simbolo.replace("«", "")
        sin_simbolo = sin_simbolo.replace("¿", "")
        sin_simbolo = sin_simbolo.replace("°", "")
        sin_simbolo = sin_simbolo.replace("º", "")
        sin_simbolo = sin_simbolo.replace("ª", "")
        sin_simbolo = sin_simbolo.replace("_x000d_", "")
        sin_simbolo = sin_simbolo.replace("@", "o")
        sin_simbolo = sin_simbolo.replace("á", "a")
        sin_simbolo = sin_simbolo.replace("à", "a")
        sin_simbolo = sin_simbolo.replace("À", "a")
        sin_simbolo = sin_simbolo.replace("Á", "a")
        sin_simbolo = sin_simbolo.replace("é", "e")
        sin_simbolo = sin_simbolo.replace("è", "e")
        sin_simbolo = sin_simbolo.replace("È", "e")
        sin_simbolo = sin_simbolo.replace("É", "e")
        sin_simbolo = sin_simbolo.replace("í", "i")
        sin_simbolo = sin_simbolo.replace("ì", "i")
        sin_simbolo = sin_simbolo.replace("Ì", "i")
        sin_simbolo = sin_simbolo.replace("Í", "i")
        sin_simbolo = sin_simbolo.replace("ó", "o")
        sin_simbolo = sin_simbolo.replace("ò", "o")
        sin_simbolo = sin_simbolo.replace("Ò", "o")
        sin_simbolo = sin_simbolo.replace("Ó", "o")
        sin_simbolo = sin_simbolo.replace("ú", "u")
        sin_simbolo = sin_simbolo.replace("ù", "u")
        sin_simbolo = sin_simbolo.replace("Ù", "u")
        sin_simbolo = sin_simbolo.replace("Ú", "u")
        sin_simbolo = sin_simbolo.replace("ñ", "ñ")
        sin_simbolo = sin_simbolo.replace("?", "")
        tratar = sin_simbolo.strip(r"!#$%^&*()[]{};:,./<>?\|`~-'=_·")
        tratar2 = tratar.translate(table)
        palabras = tratar2.split()
        tokens = []
        for palabra in palabras:
            if palabra not in stopwords:
                tokens.append(palabra.upper())
        for w in tokens:
            es_numero = w.isdigit()
            if len(w) > 2 and not es_numero:
                palabras_encontradas.append(w)

    for i in range(len(palabras_encontradas)):
        # Se comprueba PALABRA de DICCIONARIO_EMPLEO
        if palabras_encontradas[i] in diccionario_palabra and diccionario_empleo[diccionario_palabra[palabras_encontradas[i]]]['PALABRA'] not in vector_palabras and (diccionario_empleo[diccionario_palabra[palabras_encontradas[i]]]['PALABRA_GENERICA'] == str(palabra_generica) or str(palabra_generica) == "T"):
            vector_palabras.append(diccionario_empleo[diccionario_palabra[palabras_encontradas[i]]]['PALABRA'])
        # Se comprueba MASCULINO de DICCIONARIO_EMPLEO
        elif palabras_encontradas[i] in diccionario_masc and diccionario_empleo[diccionario_masc[palabras_encontradas[i]]]['PALABRA'] not in vector_palabras and (diccionario_empleo[diccionario_masc[palabras_encontradas[i]]]['PALABRA_GENERICA'] == str(palabra_generica) or str(palabra_generica) == "T"):
            vector_palabras.append(diccionario_empleo[diccionario_masc[palabras_encontradas[i]]]['PALABRA'])
        # Se comprueba FEMENINO de DICCIONARIO_EMPLEO
        elif palabras_encontradas[i] in diccionario_fem and diccionario_empleo[diccionario_fem[palabras_encontradas[i]]]['PALABRA'] not in vector_palabras and (diccionario_empleo[diccionario_fem[palabras_encontradas[i]]]['PALABRA_GENERICA'] == str(palabra_generica) or str(palabra_generica) == "T"):
            vector_palabras.append(diccionario_empleo[diccionario_fem[palabras_encontradas[i]]]['PALABRA'])
        # Se comprueba MASC_PLURAL de DICCIONARIO_EMPLEO
        elif palabras_encontradas[i] in diccionario_masc_p and diccionario_empleo[diccionario_masc_p[palabras_encontradas[i]]]['PALABRA'] not in vector_palabras and (diccionario_empleo[diccionario_masc_p[palabras_encontradas[i]]]['PALABRA_GENERICA'] == str(palabra_generica) or str(palabra_generica) == "T"):
            vector_palabras.append(diccionario_empleo[diccionario_masc_p[palabras_encontradas[i]]]['PALABRA'])
        # Se comprueba FEM_PLURAL de DICCIONARIO_EMPLEO
        elif palabras_encontradas[i] in diccionario_fem_p and diccionario_empleo[diccionario_fem_p[palabras_encontradas[i]]]['PALABRA'] not in vector_palabras and (diccionario_empleo[diccionario_fem_p[palabras_encontradas[i]]]['PALABRA_GENERICA'] == str(palabra_generica) or str(palabra_generica) == "T"):
            vector_palabras.append(diccionario_empleo[diccionario_fem_p[palabras_encontradas[i]]]['PALABRA'])
        # Se comprueba DICCIONARIO_EQUIVALENCIAS
        elif palabras_encontradas[i] in diccionario_equiv_p and diccionario_equiv[diccionario_equiv_p[palabras_encontradas[i]]]['PALABRA_CORRECTA'] not in vector_palabras and (diccionario_empleo[diccionario_equiv_p[palabras_encontradas[i]]]['PALABRA_GENERICA'] == str(palabra_generica) or str(palabra_generica) == "T"):
            vector_palabras.append(diccionario_equiv[diccionario_equiv_p[palabras_encontradas[i]]]['PALABRA_CORRECTA'])
    print("Paso 1: " + str(paso1 - inicio))
    print("Paso 2: " + str(paso2 - paso1))
    print("Paso 3: " + str(paso3 - paso2))
    print("Paso 4: " + str(paso4 - paso3))
    print("Paso 5: " + str(paso5 - paso4))
    print("Paso 6: " + str(time.time() - paso5))
    print("Tiempo total: " + str(time.time() - inicio))
    return vector_palabras

texto = '''
Oferta de empleo de ingeniero de software con experiencia en desarrollo de aplicaciones web y móviles. Voz sobre protocolo de internet Necesaria experiencia en Python, Java y C++.
'''
palabra_generica = "T"
lista_palabras = f_vector_palabras_json(texto, palabra_generica)
print(lista_palabras)


# # Import dictionario empleo

# In[3]:


with open(dictionary_path + 'diccionario_empleo.json', encoding="latin-1") as f:
    aux_emp = f.read()
diccionario_empleo = json.loads(aux_emp)
# Take 10 random items from the list
import random
random_items = random.sample(diccionario_empleo, 10)
# Print the random items
for item in random_items:
    # Do not show the property 'ID_PALABRA' and display the rest of properties
    print(item)


# # Cast dictionario empleo to dataframe

# In[26]:


# Cast the list to a dataframe with two columns LEMA that will be PALABRA and FORMA that will be the rest of properties
new_dict = []
formas = ['MASCULINO', 'FEMENINO', 'MASC_PLURAL', 'FEM_PLURAL', 'PALABRA_VISUAL']
for item in diccionario_empleo:
    for forma in formas:
        if forma in item.keys() and item[forma] != '':
            new_dict.append({'LEMA': item['PALABRA'], 'FORMA': item[forma], 'PROCENDIA': 'empleo'})
# Cast from list of dictionaries to dataframe
df_empleo = pd.DataFrame(new_dict)
print(df_empleo.shape)
df_empleo.head(10)
# Save to csv
df_empleo.to_csv(dictionary_path + 'diccionario_empleo.csv', index=False)


# In[25]:


palabra = "A360"
# Find this word in FORMA and display the LEMA


# # Import dicionario equivalencias

# In[19]:


with open(dictionary_path + 'diccionario_equivalencias.json', encoding="latin-1") as f:
    aux_emp = f.read()
dicionario_equivalencias = json.loads(aux_emp)
# Take 10 random items from the list
import random
random_items = random.sample(dicionario_equivalencias, 10)
# Print the random items
for item in random_items:
    # Do not show the property 'ID_PALABRA' and display the rest of properties
    item.pop('ID_PALABRA')
    print(item)


# # Cast dicionario equivalencias to dataframe

# In[27]:


# Cast the list to a dataframe with two columns LEMA that will be PALABRA and FORMA that will be the rest of properties
new_dict = []
formas = ['PALABRA']
for item in dicionario_equivalencias:
    for forma in formas:
        if forma in item.keys() and item[forma] is not '':
            new_dict.append({'LEMA': item['PALABRA_CORRECTA'], 'FORMA': item[forma], 'PROCENDIA': 'equivalencias'})
# Cast from list of dictionaries to dataframe
df_equivalencias = pd.DataFrame(new_dict)
print(df_equivalencias.shape)
# Show 10 random samples from the dataframe
print(df_equivalencias.iloc[np.random.randint(0, len(df_equivalencias), 10)])
# Save to csv
df_equivalencias.to_csv(dictionary_path + 'diccionario_equivalencias.csv', index=False)


# # Modified function

# In[21]:


import re

def clean_text(text):
    # Trim the text
    text = text.strip()
    # Delete additional spaces with regex
    text = re.sub(r'\s+', ' ', text)
    # Delete non alphanumeric characters
    text = re.sub(r'\W+', ' ', text)
    return text.upper()

df_empleo['FORMA'] = df_empleo['FORMA'].apply(clean_text)
df_equivalencias['FORMA'] = df_equivalencias['FORMA'].apply(clean_text)

def get_words_by_text(text, df_empleo, df_equivalencias):
    # Clean the text
    text = clean_text(text)
    # Split the text by " "
    list_words = text.split(" ")
    # Delete empty strings
    list_words = list(filter(None, list_words))
    # Delete stopwords
    list_words = [word for word in list_words if word not in stopwords]
    final_words = []
    for word in list_words:
        # Find the word in the dataframe FORMA column and return the LEMA column the first match
        lema_empleo = df_empleo[df_empleo['FORMA'] == word]['LEMA'].values
        if "A360" in lema_empleo:
            print(word)        
        if len(lema_empleo) > 0:
            final_words.append(lema_empleo[0])
        lema_equivalencias = df_equivalencias[df_equivalencias['FORMA'] == word]['LEMA'].values
        if "A360" in lema_equivalencias:
            print(word)   
        if len(lema_equivalencias) > 0:
            final_words.append(lema_equivalencias[0])
    return final_words
    
    
    
texto = '''
Oferta de empleo de ingeniero de software con experiencia en desarrollo de aplicaciones web y móviles. Voz sobre protocolo de internet Necesaria experiencia en Python, Java y C++.
'''
list_words = get_words_by_text(texto, df_empleo, df_equivalencias)
print(list_words)


# # Import offers

# In[22]:


# Read the offers file 'TRAIN_2021_2023_INFOJOBS.json' as dataframe
df_offers = pd.read_json(dictionary_path + 'descripcion_ofertas_infojobs_21_23.json')
# Show the shape of the dataframe
print(df_offers.shape)
df_offers.head()


# # Cast offers dataframe to list of descriptions

# In[23]:


# Get a list of 10 random samples from the dataframe in the column 'descripcion_oferta'
offers = df_offers['descripcion_oferta'].sample(10)
print(offers)

results = []

for offer in offers:
    # Get the list of words by text
    list_words_legacy = f_vector_palabras_json(offer, "T")
    list_words_new = get_words_by_text(offer, df_empleo, df_equivalencias)
    # If list_words_new have "A360" or "ES2015" display offer
    if "A360" in list_words_new or "ES2015" in list_words_new:
        print(offer)
    missing_words = set(list_words_legacy) - set(list_words_new)
    results.append({'offer': offer, 'list_words_legacy': list_words_legacy, 'list_words_new': list_words_new, 'num_missing_words': len(missing_words), 'missing_words': list(missing_words)})
    
# Cast to dataframe
df_results = pd.DataFrame(results)
# Save CSV file
df_results.to_csv(dictionary_path + 'results.csv', index=False)


# # Show results

# In[24]:


for result in results:
    print("OFFER:\n" + result['offer'])
    print("LEGACY:\n" + str(result['list_words_legacy']))
    print("NEW:\n" + str(result['list_words_new']))
    # Print the amount of missing words
    print("AMOUNT OF MISSING WORDS IN NEW:\n" + str(len(set(result['list_words_legacy']) - set(result['list_words_new']))))
    # Now print the words in legacy that are not in new
    print("MISSING WORDS IN NEW:\n" + str(set(result['list_words_legacy']) - set(result['list_words_new'])))

