import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def createVocabulary(df):
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df["palabras_empleo_texto"]).todense()
    vocab = tfidf.vocabulary_
    longitud = len(vocab)
    # Cast the keys of the dictionary to list of strings
    vocab = list(map(str, vocab.keys()))
    return vocab, longitud

def main():
    df = pd.read_csv("data/above_90/dataframe_procesado.csv")
    vocab = createVocabulary(df)
    print(vocab)

if __name__ == "__main__":
    main()