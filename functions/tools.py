from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import json
import pandas as pd

columns = ['SUBCATEGORIA', 'PALABRAS_EMPLEO_TEXTO', 'CATEGORIA']

encoding = 'utf-8'

def convert_TEST_to_vector(df_test, vocabularies):
    for column in vocabularies.keys():
        vocab = vocabularies[column]
        df_test[f'vector_{column}'] = df_test[column].apply(lambda x: np.array([1 if word.lower() in x.lower().split(" ") else 0 for word in vocab]))
    
    vector_columns = [f'vector_{column}' for column in vocabularies.keys()]
    df_test['vector'] = df_test[vector_columns].apply(lambda x: np.concatenate(x.values), axis=1)
    return df_test['vector']

def create_vector_columns(df_train):
    vocabularies = {}
    for column in columns:
        df_train[column] = df_train[column].fillna("").astype(str)
        
        tfidf = TfidfVectorizer()
        tfidf.fit_transform(df_train[column]).todense()
        
        vocabularies[column] = list(map(str, tfidf.vocabulary_.keys()))
        
        df_train[f'vector_{column}'] = df_train[column].apply(lambda x: np.array([1 if word.lower() in x.lower().split(" ") else 0 for word in vocabularies[column]]))
    
    vector_columns = [f'vector_{column}' for column in columns]
    df_train['vector'] = df_train[vector_columns].apply(lambda x: np.concatenate(x.values), axis=1)
    return df_train['vector'], vocabularies

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

def load_dict_label_ids(path_ids_labels):
    try:
        with open(path_ids_labels, 'r', encoding=encoding) as fp:
            dict_label_ids = json.load(fp)
    except:
        return None
    return dict_label_ids

def save_dict_label_ids(dict_label_ids, path_ids_labels):
    with open(path_ids_labels, 'w', encoding=encoding) as fp:
        json.dump(dict_label_ids, fp)

def get_vocabulary_dimension(vocabulary):
    # Get the total dimension of the vocabulary on each column
    dimension = 0
    for column in columns:
        dimension += len(vocabulary[column])
    return dimension

def get_dimension_labels(dict_label_ids):
    return len(dict_label_ids)

def create_dict_label_ids(serie):
    dict_label_ids = {}
    count = 0
    serie = np.unique(serie)
    # Iterate over serie
    for i in range(len(serie)):
        # Convert the key to a string
        key = str(serie[i])
        if key not in dict_label_ids:
            dict_label_ids[key] = count
            count += 1
    return dict_label_ids

def cast_id_to_labels(ids, dict_label_ids):
    labels = []
    for i in range(len(ids)):
        labels.append(dict_label_ids[str(ids[i])])
    return labels

def cast_labels_to_id(labels, dict_label_ids):
    ids = []
    for i in range(len(labels)):
        for key, value in dict_label_ids.items():
            if value == labels[i]:
                ids.append(int(key))
    return ids

def get_predictions(model, vector_test_array, dict_label_ids):
    predictions = model.predict(vector_test_array)
    # Get the index of the highest probability for each prediction
    predictions_label = np.argmax(predictions, axis=1)
    # Get the highest probability for each prediction
    probability = np.max(predictions, axis=1)
    # Cast the id to the label
    predictions_id = cast_labels_to_id(predictions_label, dict_label_ids)
    return predictions_id, probability

def get_accuracy(model, vector_test_array, dict_label_ids, real_id):
    predictions_id, probability = get_predictions(model, vector_test_array, dict_label_ids)
    accuracy = sum([1 if predictions_id[i] == real_id[i] else 0 for i in range(len(predictions_id))])/len(predictions_id)
    return accuracy

def get_top_highest_predictions(model, vector_test_array, dict_label_ids, N):
    predictions = model.predict(vector_test_array)
    # Get the top N predictions
    top_predictions = []
    # Do it reverse to get the highest predictions
    for i in range(len(predictions)):
        top_N_predictions = np.argsort(predictions[i])[::-1][:N]
        top_predictions.append(top_N_predictions)
    # Cast the id to the label
    top_predictions_id = []
    for i in range(len(top_predictions)):
        top_predictions_id.append(cast_labels_to_id(top_predictions[i], dict_label_ids))
    return top_predictions_id

def predict_incoming_offer(incoming_offer, vocabulary, model, dict_label_ids):
    incoming_offer = pd.DataFrame.from_dict(incoming_offer, orient='index').T
    incoming_offer['vector'] = convert_TEST_to_vector(incoming_offer, vocabulary)
    incoming_offer = incoming_offer['vector'][0].reshape(1, -1)
    result = model.predict([incoming_offer])
    # Get the highest probability
    probability = np.max(result, axis=1)[0] * 100
    # Get the index of the highest probability
    result_label = np.argmax(result, axis=1)
    # Cast the id to the label
    result_id = cast_labels_to_id(result_label, dict_label_ids)[0]
    return result_id, probability