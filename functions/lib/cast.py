import pandas as pd

def castFromTupleToDict(data):
    return [dict(zip(['id', 'asunto'], row)) for row in data]

def castFromDictToDataFrame(data):
    return pd.DataFrame(data)

def castFromDataframeToDict(dataframe):
    # Get all the columns of the dataframe
    columns = dataframe.columns
    # Create a dictionary with the columns as keys
    dataframe = dataframe.to_dict('list')
    # Create a list of dictionaries with the columns as keys
    dicts = [dict(zip(columns, row)) for row in zip(*dataframe.values())]

    return dicts

def tupleToDataframe(data, columns):
    df = pd.DataFrame(data, columns=columns)
    return df
