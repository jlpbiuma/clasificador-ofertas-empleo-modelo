#!/usr/bin/env python
# coding: utf-8

# # Import libraries and models

# In[11]:


from notebooks.functions.verbs_dictionary import *


# # Test

# In[12]:


verbo = "aullar"
conjugations = scrape_verb_conjugations(verbo)
conjugations = move_inf_first_column(conjugations)
conjugations.head()


# In[13]:


import random
verbs = read_verbs("./data/diccionario/verbos-espanol.txt")
# Take 20 random verbs not in order using random.sample
# verbs = random.sample(verbs, 50)
# Take the first 10 verbs
verbs = verbs[:10]
# Read the dictionary
verbs_df = read_dictionary("./data/diccionario/df_structured_verbos.csv")
# Create the dictionary
verbs_df, errores = create_dictionary(verbs, verbs_df)
# Create all conjugations list
all_conjugations = create_all_conjugations_list(verbs_df)
# Write the dictionary
write_dictionary(verbs_df, "./data/diccionario/df_structured_verbos.csv")
# Save all conjugations list
with open("./data/diccionario/all_conjugations.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(all_conjugations))
# Save errors
with open("./data/diccionario/errores.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(errores))


# In[14]:


print(all_conjugations)


# In[15]:


# Verify "abacore" is a verb
verb = "aullando"
# Temporalize the process
start_time = time.time()
# print(verify_is_verb(verb, all_conjugations, diccionario))
# print("--- %s seconds ---" % (time.time() - start_time))

# Create a job offer text
text = "si te critico es porque estas hurtando y criticando a los demás"
verbos = []
start_time = time.time()
for word in text.split(" "):
    verbo = verify_is_verb(word, all_conjugations, dict_verbs)
    if verbo != "":
        verbos.append(verbo)
print(verbos)
print("--- %s seconds ---" % (time.time() - start_time))


# # Main

# In[ ]:


verb = "tener"
conjugation_data, total_conjugations = scrape_verb_conjugations(verb)
# list_times = list(conjugation_data.keys())
# print(list_times)
# conjugation_data['Pretérito perfecto compuesto']
print(conjugation_data)


# In[ ]:


# Abre el archivo en modo lectura
with open('./data/diccionario/verbos-espanol-conjugaciones.txt', 'r') as archivo:
    lineas = archivo.readlines()

# Crea un dict_verbspara almacenar los verbos y sus conjugaciones agrupados por el patrón de infinitivo
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

