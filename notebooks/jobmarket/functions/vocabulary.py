from sklearn.feature_extraction.text import TfidfVectorizer
import json
from functions.tokenizer import *
# from notebooks.functions.tokenizer import *



def load_vocabulary(vocabulary_path):
    # This function loads the vocabulary from a file
    with open(vocabulary_path) as json_file:
        vocabulary = json.load(json_file)
    return vocabulary


def save_vocabulary(vocabulary, vocabulary_path):
    # This function saves the vocabulary in a file
    with open(vocabulary_path, 'w') as fp:
        json.dump(vocabulary, fp)


def create_vocabulary(df_train):
    # This function returns a dictionary with the vocabulary of each column
    # The keys are the columns and the values are the vocabulary of each column
    columns = ['CATEGORY', 'PALABRAS_EMPLEO_TEXTO']
    vocabularies = {}
    for column in columns:
        df_train[column] = df_train[column].astype(str)
        if column == 'CATEGORY':
            tfidf = TfidfVectorizer(
                tokenizer=custom_tokenizer_category_subcategory)
        else:
            tfidf = TfidfVectorizer(
                tokenizer=custom_tokenizer_palabras_empleo_texto)

        tfidf.fit_transform(df_train[column]).todense()
        vocabularies[column] = list(map(str, tfidf.vocabulary_.keys()))
    return vocabularies


def get_vocabulary_dimension(vocabulary):
    # This function returns the total size of the vocabulary (the dimension)
    return len(vocabulary['CATEGORY']) + len(vocabulary['PALABRAS_EMPLEO_TEXTO'])

def filter_vocabulary(vocabulary, vocabulary_delete):
    words = vocabulary_delete.keys()
    # Delete the word in vocabulary['PALABRAS_EMPLEO_TEXTO'] if it is in words
    for word in vocabulary['PALABRAS_EMPLEO_TEXTO']:
        if word.upper() in words:
            vocabulary['PALABRAS_EMPLEO_TEXTO'].remove(word)
    return vocabulary

def setup_vocabulary(vocabulary, df_train):
    new_vocabulary = {}
    new_vocabulary['PALABRAS_EMPLEO_TEXTO'] = vocabulary
    # Get all categories from unique values of CATEGORY in df_train
    new_vocabulary['CATEGORY'] = df_train['CATEGORY'].unique().tolist()
    return new_vocabulary