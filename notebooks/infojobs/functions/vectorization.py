import numpy as np
import json
import pandas as pd
from functions.tokenizer import custom_tokenizer_category_subcategory, custom_tokenizer_palabras_empleo_texto
from functions.vocabulary import get_vocabulary_dimension
# from notebooks.functions.vocabulary import get_vocabulary_dimension
# from notebooks.functions.tokenizer import custom_tokenizer_category_subcategory, custom_tokenizer_palabras_empleo_texto


def get_vertical_index(vocabularies, column, text):
    if column == 'CATEGORIA':
        return vocabularies[column].index(text)
    elif column == 'SUBCATEGORIA':
        return vocabularies[column].index(text) + len(vocabularies['CATEGORIA'])
    elif column == 'PALABRAS_EMPLEO_TEXTO':
        return vocabularies[column].index(text) + len(vocabularies['CATEGORIA']) + len(vocabularies['SUBCATEGORIA'])


def one_on_feature(text, column, index, offset, vocabularies, matrix):
    # This function returns the modified matrix in the position of the text
    # If the text is in the vocabulary, it will return a 1 in the position of the text
    if text in vocabularies[column]:
        horizontal_index = index - offset
        vertical_index = get_vertical_index(vocabularies, column, text)
        matrix[horizontal_index][vertical_index] = 1
    return matrix


def create_vectorize_dataframe(df_train_subset, vocabularies):
    columns = ['CATEGORIA', 'SUBCATEGORIA', 'PALABRAS_EMPLEO_TEXTO']
    # Get the total size of vocabulary
    total_size = get_vocabulary_dimension(vocabularies)
    # total_size = len(vocabularies)
    # Create a matrix of zeros with the shape of the length of the subset and the total size of the vocabulary
    matrix = np.zeros((len(df_train_subset), total_size))
    # Get the offset of the index if the dataframe is a subset
    offset = df_train_subset.index[0]
    # Iterate over the subset (the offers)
    for index, row in df_train_subset.iterrows():
        # Iterate over the columns
        for column in columns:
            if column == 'CATEGORIA':
                text = custom_tokenizer_category_subcategory(
                    row[column].lower())[0]
                matrix = one_on_feature(
                    text, column, index, offset, vocabularies, matrix)
            elif column == 'SUBCATEGORIA':
                text = custom_tokenizer_category_subcategory(
                    row[column].lower())[0]
                matrix = one_on_feature(
                    text, column, index, offset, vocabularies, matrix)
            elif column == 'PALABRAS_EMPLEO_TEXTO':
                # Split the text by spaces
                texts = custom_tokenizer_palabras_empleo_texto(
                    row[column].lower())
                # Iterate over the splitted text
                for text in texts:
                    matrix = one_on_feature(
                        text, column, index, offset, vocabularies, matrix)
    return matrix


def save_vectorized_dataframe(vectorized_dataframe, vectorized_dataframe_path):
    # This function saves the vectorized dataframe in a file
    np.save(vectorized_dataframe_path, vectorized_dataframe)


def load_vectorized_dataframe(vectorized_dataframe_path):
    # This function loads the vectorized dataframe from a file
    vectorized_dataframe = np.load(vectorized_dataframe_path)
    return vectorized_dataframe
