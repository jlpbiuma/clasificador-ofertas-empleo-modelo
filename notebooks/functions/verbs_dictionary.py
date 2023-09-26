import json
import time
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
from unidecode import unidecode

modes_index = {
    10: "Indicativo",
    18: "Subjuntivo",
    20: "Imperativo",
    22: "Infinitivo",
    24: "Gerundio",
    25: "Participio"
}

def get_mode_by_index(index):
    for mode_index in modes_index.keys():
        if index < mode_index:
            return modes_index[mode_index]

def initialize_dict_mode_time(gauche_div):
    index = 0
    conjugations = {}  # Dictionary to store conjugations
    for mode in modes_index.values():
        conjugations[mode] = {}
    all_times_modes = gauche_div.find_all("div", class_="tempstab")
    for all_times in all_times_modes:
        all_times = all_times.find_all("h3", class_="tempsheader")
        for time in all_times:
            time = time.text.strip()
            # Get the mode by index
            mode = get_mode_by_index(index)
            conjugations[mode][time] = [] 
        index += 1
    return conjugations

def get_time(tense_div):
    return tense_div.find("h3", class_="tempsheader").text.strip()

def get_conjugations(tense_div, mode):
    # Extract conjugation time for the tense
    html_elements = tense_div.find_all("div", class_="tempscorps")[0]
    # Get all the html elements inside the div and print them
    conjugations = ""
    # Loop over all the elements of the div with class "_tempscorps"
    for element in html_elements:
        # Omit the <br> elements
        if element.name != "br":
            conjugations += element.text
        # Add a new line when the element is <br>
        else:
            conjugations += "\n"
    pronuons = ["yo", "tú", "él", "nosotros", "vosotros", "ellos"]
    # Remove the pronouns from the conjugations
    for pronuon in pronuons:
        conjugations = conjugations.replace(pronuon, "")
    # Remove unnecessary spaces regex
    conjugations = re.sub(' +', ' ', conjugations)
    if "Imperativo" in mode:
        # Remove "no", "-" and " " from the conjugations
        conjugations = conjugations.replace("no", "").replace("-", "").replace(" ", "")
        result = conjugations.strip().split("\n")
    else:
        result = conjugations.strip().split("\n ")
    return result
        

def scrape_verb_conjugations(verb):
    # URL of the website to scrape
    url = f"https://www.conjugacion.es/del/verbo/{verb}.php"
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        # Find the element with id "gauche" that contains verb conjugation data
        gauche_div = soup.find("div", id="gauche")
        if gauche_div is not None:
            # Loop through all conjugation tenses
            total_conjugations = 0
            conjugations_verb = initialize_dict_mode_time(gauche_div)
            index = 0
            for tense_div in gauche_div.find_all("div", class_="tempstab"):
                # Inference the mode with the current index of the loop
                mode = get_mode_by_index(index)
                # Get time
                time = get_time(tense_div)
                # Add the verb time and its conjugations to the dictionary
                conjugations_verb[mode][time] = get_conjugations(tense_div, mode)
                # Add the number of conjugations
                total_conjugations += len(conjugations_verb[mode][time])
                # Add 1 to the index
                index += 1
            # Stablish infinitive
            return conjugations_verb, total_conjugations
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
    dict_verbs= {}
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
    for verb_index in dictionary.keys():
        modes = dictionary[verb_index].keys()
        for mode in modes:
            times = dictionary[verb_index][mode].keys()
            for time in times:
                for conjugation in dictionary[verb_index][mode][time]:
                    all_conjugations.append(unidecode(conjugation))
    return all_conjugations

def get_infinitive(dictionary, range_index):
    return dictionary[range_index]["Infinitivo"]['Simple'][0]

def verify_is_verb(word, all_conjugations, dictionary):
    # Find word in all_conjugations and get the infinitive
    try:
        index = all_conjugations.index(word.lower())
        if index != -1:
            for range_index in dictionary.keys():
                # Verify if the index is smaller than the range index, if yes, return the infinitive
                if index < range_index:
                    return get_infinitive(dictionary, range_index)
        else:
            return ""
    except:
        return ""