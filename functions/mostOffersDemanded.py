import pandas as pd
import numpy as np
import json
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def deleteCommasAndLineJumpsFromDescription(df):
    # Delete commas and line jumps from the description column
    for index, row in df.iterrows():
        df.at[index, "descripcion_oferta"] = row["descripcion_oferta"].replace("\\","").replace("/","").replace("\n", " ").replace("\r\n", " ").replace(",", " ").replace("\r","")
    return df

def getPercentil90(df):
    # Get all the registers above the 90th percentile for the column "ID_PUESTO_ESCO"
    # Visualize the number of offers by id_puesto_esco
    most_demanding_50_offers = df["id_puesto_esco"].value_counts()[:50]
    # Now find the 50 most repeated id_puesto_esco in the dataframe and create a new dataframe with them
    df_most_demanding_50_offers = df[df["id_puesto_esco"].isin(most_demanding_50_offers.index)]
    return df_most_demanding_50_offers

def main():
    file_path = "data/full_data/export_6.json"
    with open(file_path, encoding="windows-1252") as f:
        data = json.load(f)
        # Cast to pandas dataframe
        df = pd.DataFrame(data["items"])

    # Inspect the raw data from the "descripcion_oferta" column
    print(df["descripcion_oferta"].iloc[1])

    # Apply data preprocessing functions
    df_most_demanding_50_offers = getPercentil90(df)
    df_most_demanding_50_offers = deleteCommasAndLineJumpsFromDescription(df_most_demanding_50_offers)

    # Save to csv
    df_most_demanding_50_offers.to_csv("data/mostOffers/dataframe_train.csv", index=False, encoding='windows-1252')


if __name__ == "__main__":
    main()