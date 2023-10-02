import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
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
    conjugations = {}  # verbs_df to store conjugations
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
    conjugations = unidecode(re.sub(' +', ' ', conjugations))
    if "Imperativo" in mode:
        # Remove "no", "-" and " " from the conjugations
        conjugations = conjugations.replace("no", "").replace("-", "").replace(" ", "")
        result = conjugations.strip().split("\n")
    else:
        result = conjugations.strip().split("\n ")
    return result
        
def cast_dict_to_df(conjugations_verb):
    # Define the mode prefixes
    mode_prefixes = {
        'Indicativo': 'Indicativo_',
        'Subjuntivo': 'Subjuntivo_',
        'Imperativo': 'Imperativo_',
        'Infinitivo': 'Infinitivo_',
        'Gerundio': 'Gerundio_',
        'Participio': 'Participio_'
    }

    # Initialize an empty dictionary to store the modified conjugations
    modified_conjugations = {}

    # Loop through the original conjugations
    for mode, mode_conjugations in conjugations_verb.items():
        # Get the appropriate prefix for the mode
        mode_prefix = mode_prefixes.get(mode, '')

        # Initialize an empty dictionary for the mode's conjugations
        modified_mode_conjugations = {}

        # Loop through the tense and conjugation data for the mode
        for tense, tense_conjugations in mode_conjugations.items():
            # Add the tense with the prefix to the modified conjugations
            modified_tense = mode_prefix + tense
            modified_mode_conjugations[modified_tense] = tense_conjugations

        # Add the modified mode and its conjugations to the result
        modified_conjugations.update(modified_mode_conjugations)

    # Create a DataFrame from the modified conjugations
    df = pd.DataFrame([modified_conjugations])

    # Return the DataFrame
    return df

def scrape_verb_conjugations(verb):
    try:
        # URL of the website to scrape
        url = f"https://www.conjugacion.es/del/verbo/{unidecode(verb)}.php"
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
                conjugations_verb = initialize_dict_mode_time(gauche_div)
                index = 0
                for tense_div in gauche_div.find_all("div", class_="tempstab"):
                    # Inference the mode with the current index of the loop
                    mode = get_mode_by_index(index)
                    # Get time
                    time = get_time(tense_div)
                    # Add the verb time and its conjugations to the verbs_df
                    conjugations_verb[mode][time] = get_conjugations(tense_div, mode)
                    # Add 1 to the index
                    index += 1
                # Stablish infinitive
                return cast_dict_to_df(conjugations_verb)
        # If any errors occur, return an empty DataFrame
        return pd.DataFrame()
    except Exception as e:
        # Handle the exception (e.g., log it) and return an empty DataFrame
        print(f"Error: {str(e)}")
        return pd.DataFrame()

def move_inf_first_column(verbs_df_conjugated):
    # Move the column "Infinitivo_Simple" to the first position
    if 'Infinitivo_Simple' in verbs_df_conjugated.columns:
        infinitivo_simple = verbs_df_conjugated.pop('Infinitivo_Simple')
        verbs_df_conjugated.insert(0, 'Infinitivo_Simple', infinitivo_simple.str[0])
    return verbs_df_conjugated

def read_verbs(verbs_path):
    # Read txt file with verbs
    with open(verbs_path, "r", encoding="utf-8") as f:
        verbs = f.readlines()
        # Remove "\n" from the end of each verb
        verbs = [verb.strip() for verb in verbs]
    return verbs

def read_dictionary(dictionary_path):
    # Read pandas csv file with verbs
    try:
        verbs_df = pd.read_csv(dictionary_path)
        return verbs_df
    except:
        return pd.DataFrame()
    
def create_dictionary(verbs, verbs_df_prev):
    verbs_df_conjugated = pd.DataFrame()
    errors = []
    pbar = tqdm(verbs, total=len(verbs))
    if not verbs_df_prev.empty:
        prev_verbs = verbs_df_prev["Infinitivo_Simple"].values
    else:
        prev_verbs = []
    # Loop through the verbs you want to scrape
    for verb in pbar:
        # Verify if the verb is not already in the verbs_df_conjugated
        if verb in prev_verbs:
            continue
        last_chars = verb[-2:]
        if last_chars in ["ar", "er", "ir"]:
            pbar.set_description(f"Processing {verb}")
            time.sleep(0.5)
            conjugation_data = scrape_verb_conjugations(verb)
            # Vefiy conjugation_data dataframe is not empty
            if not conjugation_data.empty:
                # Convert conjugation_data (a dictionary) to a DataFrame
                conjugation_df = pd.DataFrame.from_dict(conjugation_data)
                # Add the new conjugation DataFrame to verbs_df_conjugated
                verbs_df_conjugated = pd.concat([verbs_df_conjugated, conjugation_df], ignore_index=True)
            else:
                errors.append(verb)
                continue
    verbs_df_conjugated = move_inf_first_column(verbs_df_conjugated)
    return verbs_df_conjugated, errors

def write_dictionary(verbs_df, dictionary_path):
    # Save .csv of the verbs_df
    verbs_df.to_csv(dictionary_path, index=False)
        
def create_all_conjugations_list(verbs_df):
    all_conjugations = []
    # Now loop over rows
    for index, row in verbs_df.iterrows():
        for column in verbs_df.columns:
            if column == "Infinitivo_Simple":
                # Is just a string, simply append it
                all_conjugations.append(row[column])
            else:
                all_conjugations.extend(row[column])
    return all_conjugations


def get_infinitive(verbs_df, range_index):
    return verbs_df[range_index]['Infinitivo_Simple'][0]

def verify_is_verb(word, all_conjugations, verbs_df):
    # Find word in all_conjugations and get the infinitive
    try:
        index = all_conjugations.index(unidecode(word.lower()))
        if index != -1:
            infinitive = get_infinitive(verbs_df, index)
            return infinitive
        else:
            return ""
    except:
        return ""