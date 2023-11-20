#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[1]:


import pandas as pd
import json
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk import ngrams
import nltk


# # Global variables

# In[2]:


data_path = './notebooks/palabras-empleo-texto/data/'
dictionary_path = './notebooks/palabras-empleo-texto/static/'
stopwords = stopwords.words('spanish')
stemmer = SnowballStemmer('spanish')
df_empleo = pd.read_csv(dictionary_path + 'diccionario_empleo.csv')
df_equivalencias = pd.read_csv(dictionary_path + 'diccionario_equivalencias.csv')
df_collocations = pd.read_csv(dictionary_path + 'diccionario_collocation.csv')
list_collocations = df_collocations['FORMAS'].tolist()


# # Legacy functions

# In[3]:


def f_vector_palabras_json(texto, palabra_generica="T"):
    # importamos las librerías necesarias
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


    # Obtengo en un dataframe el diccionario de equivalencias
    with open(dictionary_path + 'diccionario_equivalencias.json',
              encoding="latin-1") as f:
        aux_equiv = f.read()
    diccionario_equiv = json.loads(aux_equiv)
    
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
    return vector_palabras


def f_vector_collocation_json(texto):

    # adverbios
    adverbios = ['ahora', 'antes', 'despues', 'tarde', 'luego', 'ayer', 'temprano', 'ya',
                 'todavia', 'anteayer', 'aun', 'pronto', 'hoy', 'aqui', 'ahi', 'alli',
                 'cerca', 'lejos', 'fuera', 'dentro', 'alrededor', 'aparte', 'encima',
                 'debajo', 'delante', 'detras', 'asi', 'bien', 'mal', 'despacio',
                 'deprisa', 'como', 'mucho', 'poco', 'muy', 'casi', 'todo', 'nada', 'algo',
                 'medio', 'demasiado', 'bastante', 'mas', 'menos', 'ademas', 'incluso',
                 'tambien', 'si', 'asimismo', 'no', 'tampoco', 'jamas', 'nunca', 'acaso',
                 'quiza', 'quizas', 'tal', 'vez', 'mejor']
    stopwords.extend(adverbios)

    # obtengo en un dataframe el diccionario de collocation
    with open(dictionary_path + 'diccionario_collocation.json',
              encoding="latin-1") as f:
        aux_collocations = f.read()
    diccionario_collocations = json.loads(aux_collocations)

    # obtengo en un dataframe el diccionario de equivalencias de collocation
    with open(dictionary_path + 'diccionario_equivalencias_collocation.json',
              encoding="latin-1") as f:
        aux_equiv = f.read()
    dic_equiv_collocations = json.loads(aux_equiv)

    vector_collocation = list()
    collocations_dic = list()
    collocations_equiv = list()

    for i in range(len(diccionario_collocations)):
        collocations_dic.append(diccionario_collocations[i]['RAIZ_COLLOCATION'])

    for i in range(len(dic_equiv_collocations)):
        collocations_equiv.append(dic_equiv_collocations[i]['RAIZ_COLLOCATION'])

    stemmer = SnowballStemmer("spanish")

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
    collocations = []
    for n in [2, 3]:
        collocations.extend(nltk.ngrams(palabras_encontradas, n))

    for coll in collocations:
        if len(coll) == 2:
            coll_final = coll[0] + " " + coll[1]
        if len(coll) == 3:
            coll_final = coll[0] + " " + coll[1] + " " + coll[2]
        coll_sep = coll_final.split(sep=' ')
        coll_def = ""
        for k in range(len(coll_sep)):
            coll_def = coll_def + stemmer.stem(coll_sep[k]).upper() + " "
        coll_def = coll_def[:-1]
        if coll_def in collocations_dic and coll_final not in vector_collocation:
            vector_collocation.append(coll_final)
        elif coll_def in collocations_equiv and coll_final not in vector_collocation:
            vector_collocation.append(coll_final)

    value = {
        "vector_collocation": vector_collocation
    }

    return json.dumps(value)

def f_vector_collocation_json(texto):

    # adverbios
    adverbios = ['ahora', 'antes', 'despues', 'tarde', 'luego', 'ayer', 'temprano', 'ya',
                 'todavia', 'anteayer', 'aun', 'pronto', 'hoy', 'aqui', 'ahi', 'alli',
                 'cerca', 'lejos', 'fuera', 'dentro', 'alrededor', 'aparte', 'encima',
                 'debajo', 'delante', 'detras', 'asi', 'bien', 'mal', 'despacio',
                 'deprisa', 'como', 'mucho', 'poco', 'muy', 'casi', 'todo', 'nada', 'algo',
                 'medio', 'demasiado', 'bastante', 'mas', 'menos', 'ademas', 'incluso',
                 'tambien', 'si', 'asimismo', 'no', 'tampoco', 'jamas', 'nunca', 'acaso',
                 'quiza', 'quizas', 'tal', 'vez', 'mejor']
    stopwords.extend(adverbios)

    # obtengo en un dataframe el diccionario de collocation
    with open(dictionary_path + 'diccionario_collocation.json',
              encoding="latin-1") as f:
        aux_collocations = f.read()
    diccionario_collocations = json.loads(aux_collocations)

    # obtengo en un dataframe el diccionario de equivalencias de collocation
    with open(dictionary_path + 'diccionario_equivalencias_collocation.json',
              encoding="latin-1") as f:
        aux_equiv = f.read()
    dic_equiv_collocations = json.loads(aux_equiv)

    vector_collocation = list()
    collocations_dic = list()
    collocations_equiv = list()

    for i in range(len(diccionario_collocations)):
        collocations_dic.append(diccionario_collocations[i]['RAIZ_COLLOCATION'])

    for i in range(len(dic_equiv_collocations)):
        collocations_equiv.append(dic_equiv_collocations[i]['RAIZ_COLLOCATION'])

    stemmer = SnowballStemmer("spanish")

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
    collocations = []
    for n in [2, 3]:
        collocations.extend(nltk.ngrams(palabras_encontradas, n))

    for coll in collocations:
        if len(coll) == 2:
            coll_final = coll[0] + " " + coll[1]
        if len(coll) == 3:
            coll_final = coll[0] + " " + coll[1] + " " + coll[2]
        coll_sep = coll_final.split(sep=' ')
        coll_def = ""
        for k in range(len(coll_sep)):
            coll_def = coll_def + stemmer.stem(coll_sep[k]).upper() + " "
        coll_def = coll_def[:-1]
        if coll_def in collocations_dic and coll_final not in vector_collocation:
            vector_collocation.append(coll_final)
        elif coll_def in collocations_equiv and coll_final not in vector_collocation:
            vector_collocation.append(coll_final)

    value = {
        "vector_collocation": vector_collocation
    }

    return json.dumps(value)


# # New functions

# In[4]:


import re
from unidecode import unidecode

expections = ["@", r"\."]

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

def get_words_by_text(text):
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
        if len(lema_empleo) > 0:
            final_words.append(lema_empleo[0])
        lema_equivalencias = df_equivalencias[df_equivalencias['FORMA'] == word]['LEMA'].values
        if len(lema_equivalencias) > 0:
            final_words.append(lema_equivalencias[0])
    return final_words

# Change to upper case all stopwords
stopwords = [word.upper() for word in stopwords]

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

def get_collocations(descripcion_oferta):
    # Get all forms from the description
    list_forms = calculate_forms(descripcion_oferta)
    # Find in the list of collocations
    list_collocations_found = [form for form in list_forms if form in list_collocations]
    # Get the LEMA from the collocations
    list_collocations_found = [df_collocations[df_collocations["FORMAS"] == form]["LEMA"].iloc[0] for form in list_collocations_found]
    return list_collocations_found


# # Test

# In[5]:


df_offers = pd.read_json(data_path + "descripcion_ofertas_infojobs_21_23.json")
# Get 100 random samples from the dataset
df_test = df_offers.sample(100)

df_test["PALABRAS_LEGACY"] = df_test["descripcion_oferta"].apply(f_vector_palabras_json)
df_test["COLLOCATIONS_LEGACY"] = df_test["descripcion_oferta"].apply(lambda x: json.loads(f_vector_collocation_json(x))["vector_collocation"])
df_test["PALABRAS_NEW"] = df_test["descripcion_oferta"].apply(get_words_by_text)
df_test["COLLOCATIONS_NEW"] = df_test["descripcion_oferta"].apply(get_collocations)

df_test.to_json(data_path + "descripcion_ofertas_infojobs_21_23_test.json", orient="records")

