<<<<<<< HEAD
def calculate_accuracy(predicted_data, real_data):
    total_matches = 0
    total_dismatch = 0
    total_predictions = len(predicted_data)

    # Filter out entries with None in ID_ESCO from real_data
    real_data_filtered = [(real_id, real_esco) for real_id, real_esco in real_data if real_esco is not None]

    for predicted_entry in predicted_data:
        predicted_id = predicted_entry['ID']
        predicted_esco = predicted_entry['ID_ESCO']

        for real_entry in real_data_filtered:
            real_id, real_esco = real_entry
            if predicted_id == real_id and predicted_esco == real_esco:
                total_matches += 1
                break
            if predicted_id == real_id and predicted_esco != real_esco:
                total_dismatch += 1
                break
        else:
            total_predictions -= 1


    accuracy = (total_matches / total_predictions) * 100
    sensibility = (total_dismatch / total_predictions) * 100
    return accuracy, sensibility

def calculate_accuracy_both(predicted_data, real_data):
    total_matches = {"jaccard": 0, "levenshtein": 0}
    total_dismatch = {"jaccard": 0, "levenshtein": 0}
    total_predictions = len(predicted_data)

    # Filter out entries with None in ID_ESCO from real_data
    real_data_filtered = []
    for real_element in real_data:
        real_id, real_esco = real_element
        if real_esco is not None:
            real_data_filtered.append(real_element)

    for predicted_entry in predicted_data:
        predicted_id = predicted_entry['ID_OFERTA']
        predicted_esco_jaccard = predicted_entry['ID_ESCO_RECOMENDADO_JACCARD']
        predicted_esco_levenshtein = predicted_entry['ID_ESCO_RECOMENDADO_LEVENSHTEIN']

        for real_entry in real_data_filtered:
            real_id, real_esco = real_entry
            if predicted_id == real_id:
                if predicted_esco_jaccard == str(real_esco):
                    total_matches["jaccard"] += 1
                else:
                    total_dismatch["jaccard"] += 1
                if predicted_esco_levenshtein == str(real_esco):
                    total_matches["levenshtein"] += 1
                else:
                    total_dismatch["levenshtein"] += 1
                break
        else:
            total_predictions -= 1

    accuracy_jaccard = (total_matches["jaccard"] / total_predictions) * 100
    sensibility_jaccard = (total_dismatch["jaccard"] / total_predictions) * 100
    accuracy_levenshtein = (total_matches["levenshtein"] / total_predictions) * 100
    sensibility_levenshtein = (total_dismatch["levenshtein"] / total_predictions) * 100
    return accuracy_jaccard, sensibility_jaccard, accuracy_levenshtein, sensibility_levenshtein
=======
def calculate_accuracy(predicted_data, real_data):
    total_matches = 0
    total_dismatch = 0
    total_predictions = len(predicted_data)

    # Filter out entries with None in ID_ESCO from real_data
    real_data_filtered = [(real_id, real_esco) for real_id, real_esco in real_data if real_esco is not None]

    for predicted_entry in predicted_data:
        predicted_id = predicted_entry['ID']
        predicted_esco = predicted_entry['ID_ESCO']

        for real_entry in real_data_filtered:
            real_id, real_esco = real_entry
            if predicted_id == real_id and predicted_esco == real_esco:
                total_matches += 1
                break
            if predicted_id == real_id and predicted_esco != real_esco:
                total_dismatch += 1
                break
        else:
            total_predictions -= 1


    accuracy = (total_matches / total_predictions) * 100
    sensibility = (total_dismatch / total_predictions) * 100
    return accuracy, sensibility

>>>>>>> 668e8fa129e1a338a1877c2fbd6badacc592a235
