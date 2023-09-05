import pandas as pd
import numpy as np
from functions.labelization import cast_labels_to_id
from functions.vectorization import create_vectorize_dataframe

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
    """
    This function returns the accuracy of the model
    :param model: The model to evaluate, it must be a keras model
    :param vector_test_array: The vectorized test array, it must be the test offers vectorized
    :param dict_label_ids: The dictionary to cast from returning labels to id
    :param real_id: The real id of the test offers
    """
    predictions_id, probability = get_predictions(
        model, vector_test_array, dict_label_ids)
    accuracy = sum([1 if str(predictions_id[i]) == str(real_id[i]) else 0 for i in range(
        len(predictions_id))])/len(predictions_id)
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
        top_predictions_id.append(cast_labels_to_id(
            top_predictions[i], dict_label_ids))
    return top_predictions_id

def predict_incoming_offer(incoming_offer, vocabulary, model, dict_label_ids):
    incoming_offer = pd.DataFrame.from_dict(incoming_offer, orient='index').T
    incoming_offer['vector'] = create_vectorize_dataframe(
        incoming_offer, vocabulary)
    incoming_offer = incoming_offer['vector'][0].reshape(1, -1)
    result = model.predict([incoming_offer])
    # Get the highest probability
    probability = np.max(result, axis=1)[0] * 100
    # Get the index of the highest probability
    result_label = np.argmax(result, axis=1)
    # Cast the id to the label
    result_id = cast_labels_to_id(result_label, dict_label_ids)[0]
    return result_id, probability