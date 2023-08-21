import json
import os
from lib.cast import castFromTupleToDict, castFromDataframeToDict
import csv

filename_step1 = 'step1.json'
filename_step2 = 'step2.json'
# Get the current working directory
cwd = os.getcwd()
data_folder = os.path.join(cwd, 'data')

def createJSON(step):
    filename = stepToFilenamePath(step)
    if os.path.exists(filename):
        os.remove(filename)
        # else create the file
    with open(filename, 'w') as outfile:
        json.dump([], outfile)
    return

def stepToFilenamePath(step):
    if step == 1:
        return os.path.join(data_folder, filename_step1)
    elif step == 2:
        return os.path.join(data_folder, filename_step2)
    else:
        return None

def readJSON(step):
    filename = stepToFilenamePath(step)
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

def writeJSON(step, data):
    createJSON(step)
    filename = stepToFilenamePath(step)
    with open(filename, 'w') as outfile:
    #  if step == 1 is a list of tuples but if step == 2 is a dataframe
        if step == 1:
            # Transfrom data (array of tuples) to a list of dictionaries
            data = castFromTupleToDict(data)
        json.dump(data, outfile)
    return

def readJSONByFilename(filename):
    filePath = os.path.join(data_folder, filename)
    with open(filePath) as json_file:
        data = json.load(json_file)
    return data

def readCSV(filename):
    data = []
    filePath = os.path.join(data_folder, filename)
    with open(filePath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data
