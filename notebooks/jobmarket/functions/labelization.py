import json
import numpy as np
import pandas as pd

encoding = 'utf-8'


def get_dict_dimension(dict_label_ids):
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
        if str(ids[i]) in dict_label_ids:
            labels.append(dict_label_ids[str(ids[i])])
        else:
            labels.append(-1)
    return np.array(labels)


def cast_labels_to_id(labels, dict_label_ids):
    ids = []
    for i in range(len(labels)):
        for key, value in dict_label_ids.items():
            if value == labels[i]:
                ids.append(int(key))
    return ids


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
