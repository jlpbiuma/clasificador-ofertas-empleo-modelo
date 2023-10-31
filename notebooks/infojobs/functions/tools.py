from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import json
import pandas as pd

columns = ['SUBCATEGORIA', 'PALABRAS_EMPLEO_TEXTO', 'CATEGORIA']

encoding = 'utf-8'

def load_json(path):
    # Initialize an empty list to store the JSON objects
    data = []

    # Open the JSON file and read each line as a separate JSON object
    with open(path, encoding='utf-8') as json_file:
        for line in json_file:
            try:
                json_data = json.loads(line)
                data.append(json_data)
            except json.JSONDecodeError as e:
                print(f"Error reading JSON: {e}")
                # Handle the error as needed
    return data


def count_words(df):
    # Count the number of words in the column PALABRAS_EMPLEO_TEXTO
    # df['NUM_WORDS'] = df['PALABRAS_EMPLEO_TEXTO'].apply(lambda x: len(x.split(" ")) - 1)
    df['NUM_WORDS'] = df['PALABRAS_EMPLEO_TEXTO'].apply(lambda x: len(x.split(" ")))
    return df['NUM_WORDS']


def convert_TEST_to_vector(df_test, vocabularies):
    for column in vocabularies.keys():
        vocab = vocabularies[column]
        df_test[f'vector_{column}'] = df_test[column].apply(lambda x: np.array(
            [1 if word.lower() in x.lower().split(" ") else 0 for word in vocab]))

    vector_columns = [f'vector_{column}' for column in vocabularies.keys()]
    df_test['vector'] = df_test[vector_columns].apply(
        lambda x: np.concatenate(x.values), axis=1)
    return df_test['vector']


def create_vector_columns(df_train):
    columns = ['SUBCATEGORIA', 'PALABRAS_EMPLEO_TEXTO', 'CATEGORIA']
    vocabularies = {}
    for column in columns:
        df_train[column] = df_train[column].astype(str)

        # Define a custom analyzer that splits on spaces but keeps multi-word phrases
        tfidf = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
        tfidf.fit_transform(df_train[column]).todense()

        vocabularies[column] = list(map(str, tfidf.vocabulary_.keys()))

    return vocabularies
    # df_train[f'vector_{column}'] = df_train[column].apply(lambda x: np.array(
    #     [1 if word.lower() in x.lower().split(" ") else 0 for word in vocabularies[column]]))

    # vector_columns = [f'vector_{column}' for column in columns]
    # df_train['vector'] = df_train[vector_columns].apply(
    #     lambda x: np.concatenate(x.values), axis=1)
    # return df_train['vector'], vocabularies


def load_vector_columns(path_vector, vocabulary_path):
    try:
        vector = pd.read_pickle(path_vector)
        vocabularies = load_vocabulary(vocabulary_path)
    except:
        return None, None
    return vector, vocabularies


def save_vector_columns(vector, path_vector):
    vector.to_pickle(path_vector)


def load_vocabulary(vocabulary_path):
    # Verify if the vocabulary exists
    with open(vocabulary_path, 'r', encoding=encoding) as fp:
        vocabularies = json.load(fp)
    return vocabularies


def save_vocabulary(vocabularies, vocabulary_path):
    with open(vocabulary_path, 'w', encoding=encoding) as fp:
        json.dump(vocabularies, fp)


def get_vocabulary_dimension(vocabulary):
    # Get the total dimension of the vocabulary on each column
    dimension = 0
    for column in columns:
        dimension += len(vocabulary[column])
    return dimension


def get_dimension_labels(dict_label_ids):
    return len(dict_label_ids)
