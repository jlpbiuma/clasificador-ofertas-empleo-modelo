from sklearn.feature_extraction.text import TfidfVectorizer
import json
from functions.tokenizer import *


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
    columns = ['CATEGORIA', 'SUBCATEGORIA', 'PALABRAS_EMPLEO_TEXTO']
    vocabularies = {}
    for column in columns:
        df_train[column] = df_train[column].astype(str)
        if column == 'CATEGORIA' or column == 'SUBCATEGORIA':
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
    return len(vocabulary['CATEGORIA']) + len(vocabulary['SUBCATEGORIA']) + len(vocabulary['PALABRAS_EMPLEO_TEXTO'])
