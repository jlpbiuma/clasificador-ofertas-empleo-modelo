import requests
from bs4 import BeautifulSoup
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
        verb_time = verb.replace("no ", " ").replace("-", "").strip().split(" ")
    else:
        # Remove "-" from the string
        verbs = ' '.join(verbs)
        # Delete "-" from the string
        verbs = verbs.replace("-", "")
        # Split by " "
        verb_time = verbs.strip().split(" ")
        if len(verb_time) == 10:
            # Join the 0 element with the 1 element and so on
            verb_time = [verb_time[i] + verb_time[i+1] for i in range(0, len(verb_time), 2)]
    return verb_time

def clasify_verb_form(verbs, form, actual_time):
    if "Simple" == form:
        verb = ''.join(verbs)
        if "Simple" not in actual_time:
            form = "Infinitivo simple"
            verb_time = [verb]
        else:
            form = "Gerundio simple"
            verb_time = [verb]
    elif "Compuesto" == form:
        verb = ''.join(verbs)
        # Remove additional spaces with regex
        verb = re.sub(' +', ' ', verb)
        if "Compuesto" not in actual_time:
            form = "Infinitivo compuesto"
            verb_time = [verb]
        else:
            form = "Gerundio compuesto"
            verb_time = [verb]
    elif "Imperativo" in form:
        verb_time = get_conjugation_imperative_list(verbs, form)
    else:
        # Create list of verbs with their conjugations
        verb_time = get_conjugation_list(verbs)
    return form, verb_time

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
            mode = gauche_div.find("h2", class_="mode").text.strip()  # Get the tense name
            for tense_div in gauche_div.find_all("div", class_="tempstab"):
                # Get the h2 inside tense_div
                # Verb time
                time = tense_div.find("h3", class_="tempsheader").text.strip()  # Get the tense name
                # Eliminar el imperativo negativo ya que se repite
                # Extract conjugation time for the tense
                verbs = tense_div.find_all("div", class_="tempscorps")[0].stripped_strings
                # Classify the verb form
                form, verb_time = clasify_verb_form(verbs, form, conjugations.keys())
                # Add the verb form and its conjugations to the dictionary
                conjugations[mode][form] = verb_time
            # Get the total number of conjugations
            total_conjugations = sum([len(conjugations[form]) for form in conjugations])
            # Stablish infinitive
            conjugations["Infinitivo"] = verb
            return conjugations, total_conjugations
        else:
            return {}
    else:
        return {}
    
verbo = "aullar"
conjugations, total_conjugations = scrape_verb_conjugations(verbo)