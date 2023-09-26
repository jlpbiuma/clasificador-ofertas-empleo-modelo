import requests
from bs4 import BeautifulSoup
import re
import json
import time
from tqdm import tqdm

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
        # Remove "-" from the string
        verbs = ' '.join(verbs)
        # Delete "-" from the string
        verbs = verbs.replace("-", "")
        # Split by " "
        verb_forms = verbs.strip().split(" ")
        if len(verb_forms) == 10:
            # Join the 0 element with the 1 element and so on
            verb_forms = [verb_forms[i] + verb_forms[i+1] for i in range(0, len(verb_forms), 2)]
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
            # Get the total number of conjugations
            total_conjugations = sum([len(conjugations[form]) for form in conjugations])
            # Stablish infinitive
            conjugations["Infinitivo"] = verb
            return conjugations, total_conjugations
        else:
            return {}
    else:
        return {}
    
def read_verbs(verbs_path):
    # Read txt file with verbs
    with open(verbs_path, "r", encoding="utf-8") as f:
        verbs = f.readlines()
        # Remove "\n" from the end of each verb
        verbs = [verb.strip() for verb in verbs]
    return verbs

def read_dictionary(dictionary_path):
    # This functions allows to read the dictionary
    try:
        with open(dictionary_path, "r", encoding="utf-8") as f:
            dictionary = json.load(f, ensure_ascii=False, indent=4)
        return dictionary
    except:
        return {}

def create_dictionary(verbs, diccionario):
    # This function scrapes the conjugations of the verbs in the list
    verbos_actuales = list(diccionario.keys())
    diccionario = {}
    errores = []
    actual_amount = 0
    pbar = tqdm(verbs, total=len(verbs))
    for verb in pbar:
        last_chars = verb[-2:]
        if last_chars in ["ar", "er", "ir"]:
            pbar.set_description(f"Processing {verb}")
            time.sleep(0.3)
            try:
                conjugation_data, total_conjugations = scrape_verb_conjugations(verb)
                if conjugation_data == {}:
                    continue
                elif verb not in verbos_actuales:
                    actual_amount += total_conjugations
                    # El diccinario se trata de un objeto que tiene como clave el rango numérico de las conjugaciones
                    # y su valor es un objeto que contiene todas las conjugaciones de un verbo
                    diccionario[actual_amount] = conjugation_data
            except:
                # Hay veces que durante el fetch de la página se produce un error, se deben de volver a hacer
                errores.append(verb)
                continue
    return diccionario, errores

def write_dictionary(dictionary, dictionary_path):
    # This function allows to write the dictionary
    with open(dictionary_path, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=4)
        
def create_all_conjugations_list(dictionary):
    # Expand the dictionary to a list of all conjugations
    all_conjugations = []
    for verb in dictionary.keys():
        for conjugation in dictionary[verb].keys():
            all_conjugations.extend(dictionary[verb][conjugation])
    return all_conjugations
    
def verify_is_verb(word, all_conjugations, dictionary):
    # Find word in all_conjugations and get the infinitive
    index = all_conjugations.index(word.lower())
    if index != -1:
        for range_index in dictionary.keys():
            # Verify if the index is smaller than the range index, if yes, return the infinitive
            if index <= range_index:
                return dictionary[range_index]["Infinitivo"]
    else:
        return ""


def main():
    verbs = read_verbs("./data/diccionario/verbos-espanol.txt")
    # Read the dictionary
    diccionario = read_dictionary("./data/diccionario/verbos-espanol.json")
    # Create the dictionary
    diccionario, errores = create_dictionary(verbs, diccionario)
    # Create all conjugations list
    all_conjugations = create_all_conjugations_list(diccionario)
    # Write the dictionary
    write_dictionary(diccionario, "./data/diccionario/verbos-espanol.json")
    # Save all conjugations list
    with open("./data/diccionario/all_conjugations.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_conjugations))
    # Save errors
    with open("./data/diccionario/errores.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(errores))
        
main()