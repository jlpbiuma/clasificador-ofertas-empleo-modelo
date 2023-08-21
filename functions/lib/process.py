import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import pandas as pd
import Levenshtein
from lib.cast import castFromDataframeToDict
import re
import es_core_news_md
from nltk.tokenize import word_tokenize
from unidecode import unidecode
import datetime

# NLTK Data
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

# Spacy Data
nlp = es_core_news_md.load()

stop_words = stopwords.words('spanish')

def remove_stopwords(string):
    # Tokenize the string into individual words
    words = word_tokenize(string)
    
    # Remove stopwords from the list of words
    filtered_words = [word for word in words if word.casefold() not in stop_words]
    
    # Join the filtered words back into a string
    filtered_string = ' '.join(filtered_words)
    
    return filtered_string

def get_stems(string):
    stemmer = SnowballStemmer('spanish')
    
    # Tokenize the string into individual words
    words = word_tokenize(string)
    
    # Stem each word
    stems = [stemmer.stem(word) for word in words]
    
    # Join the stems back into a string
    stem_string = ' '.join(stems)
    
    return stem_string

def remove_suffix(string, suffixes):
    pattern = r'\b(?:{})\b'.format('|'.join(suffixes))
    return re.sub(pattern, '', string)

def remove_accents(input_string):
    return unidecode(input_string)

def calculate_jaccard_similarity(string1, string2):
    set1 = set(string1.split())
    set2 = set(string2.split())
    intersection = len(set1.intersection(set2))
    union = len(set1) + len(set2) - intersection
    similarity = intersection / union
    return similarity

def clear_asunto(string, suffixes_to_remove):
    incoming_string = re.sub(r'\d+', '', string)  # Remove numbers from incoming string
    incoming_string = unidecode(incoming_string)  # Remove accents from incoming string
    incoming_string = remove_stopwords(incoming_string)  # Remove stopwords from incoming string
    incoming_string = remove_suffix(incoming_string, suffixes_to_remove)  # Remove specified suffixes
    incoming_string_processed = get_stems(incoming_string).upper() # Get stems from incoming string (los lexemas)
    return incoming_string_processed

def process_data(fuentes, referencias, metric='jaccard', N=1000, start=0, end=54000):
    data = []
    suffixes_to_remove = ['/a', '/as', '/os']
    # Take 1000 random indices from the list of fuentes
    # indices = random.sample(range(0, len(fuentes)), N)
    # Iterate over the indices
    for fuente in fuentes[start:end]:
        incoming_string = fuente['asunto']
        incoming_string_processed = clear_asunto(incoming_string, suffixes_to_remove)
        if metric == 'jaccard':
            best_similarity = 0.0
        elif metric == 'levenshtein':
            best_similarity = float('inf')
        most_similar_string = ""
        most_similar_id = ""
        
        for referencia in referencias:
            reference_string, reference_id = referencia
            if metric == 'jaccard':
                similarity = calculate_jaccard_similarity(incoming_string_processed.lower(), reference_string.lower())
                if similarity > best_similarity:
                    best_similarity = similarity
                    most_similar_string = reference_string
                    most_similar_id = reference_id
            elif metric == 'levenshtein':
                similarity = Levenshtein.distance(incoming_string_processed.lower(), reference_string.lower())
                if similarity < best_similarity:
                    best_similarity = similarity
                    most_similar_string = reference_string
                    most_similar_id = reference_id
        
        data.append({
            'ID': fuente['id'],
            'ASUNTO_INCOMING': fuente['asunto'],
            'ASUNTO_ESCO': most_similar_string,
            'ID_ESCO': most_similar_id
        })
        
    df = pd.DataFrame(data)
    # Save to csv
    df.to_csv('data.csv', index=False)
    return castFromDataframeToDict(df)

def processDataPalabras(data_read, data_real):
    data = []
    for i, row in data_read.iterrows():
        id_oferta = row['ID_OFERTA']
        cadena_read = row['CADENA']

        best_similarity_jaccard = 0.0
        best_similarity_levenshtein = float('inf')
        id_puesto_esco_recomendado_jaccard = ""
        id_puesto_esco_recomendado_levenshtein = ""

        for i, row in data_real.iterrows():
            cadena_real = row['CADENA']
            id_puesto_esco = row['ID_PUESTO_ESCO']

            best_similarity_jaccard, id_puesto_esco_recomendado_jaccard = calculateJaccard(
                cadena_read, cadena_real, id_puesto_esco, best_similarity_jaccard)

            best_similarity_levenshtein, id_puesto_esco_recomendado_levenshtein = calculateLev(
                cadena_read, cadena_real, id_puesto_esco, best_similarity_levenshtein)

        data.append({
            'ID_OFERTA': id_oferta,
            'ID_ESCO_RECOMENDADO_JACCARD': id_puesto_esco_recomendado_jaccard,
            'ID_ESCO_RECOMENDADO_LEVENSHTEIN': id_puesto_esco_recomendado_levenshtein
        })

    df = pd.DataFrame(data)
    # Save to csv
    df.to_csv('data.csv', index=False)

    now = datetime.datetime.now()
    print("Current date and time: ", now.strftime("%Y-%m-%d %H:%M:%S"))

    return

def calculateJaccard(cadena_read, cadena_real, id_puesto_esco, best_similarity_jaccard):
    similarity = calculate_jaccard_similarity(cadena_read.lower(), cadena_real.lower())
    if similarity > best_similarity_jaccard:
        return similarity, id_puesto_esco
    else:
        return best_similarity_jaccard, id_puesto_esco

def calculateLev(cadena_read, cadena_real, id_puesto_esco, best_similarity_levenshtein):
    similarity = Levenshtein.distance(cadena_read.lower(), cadena_real.lower())
    if similarity < best_similarity_levenshtein:
        return similarity, id_puesto_esco
    else:
        return best_similarity_levenshtein, id_puesto_esco

def processPalabrasCos(data_read, data_real):
    data = []
    for i, row in data_read.iterrows():
        id_oferta = row['ID_OFERTA']
        cadena_read = row['CADENA']
        
        for i,row in data_real.iterrows():
            cadena_real = row['CADENA']
            id_puesto_esco = row['ID_PUESTO_ESCO']
            similarity = calculate_cosine_similarity(cadena_read.lower(), cadena_real.lower())
            if similarity > best_similarity:
                best_similarity = similarity
                most_similar_string = reference_string
                most_similar_id = reference_id

        data.append({
            'ID_OFERTA': id_oferta,
            'ID_ESCO_RECOMENDADO_JACCARD': id_puesto_esco_recomendado_jaccard,
            'ID_ESCO_RECOMENDADO_LEVENSHTEIN': id_puesto_esco_recomendado_levenshtein
        })

    df = pd.DataFrame(data)
    # Save to csv
    df.to_csv('dataCoseno.csv', index=False)

    now = datetime.datetime.now()
    print("Current date and time: ", now.strftime("%Y-%m-%d %H:%M:%S"))

    return

def calculate_cosine_similarity(incoming_string, reference_string):
    incoming_string = incoming_string.split()
    reference_string = reference_string.split()
    all_words = set(incoming_string + reference_string)
    incoming_string_vector = [incoming_string.count(word) for word in all_words]
    reference_string_vector = [reference_string.count(word) for word in all_words]
    dot_product = sum(i * j for i, j in zip(incoming_string_vector, reference_string_vector))
    incoming_string_vector_length = math.sqrt(sum([i ** 2 for i in incoming_string_vector]))
    reference_string_vector_length = math.sqrt(sum([i ** 2 for i in reference_string_vector]))
    cosine_similarity = dot_product / (incoming_string_vector_length * reference_string_vector_length)
    return cosine_similarity