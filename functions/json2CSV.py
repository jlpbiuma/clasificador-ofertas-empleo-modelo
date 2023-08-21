import pandas as pd
import json

def main():
    file_path = "data/no_categorization/export_TRAIN.json"
    with open(file_path, encoding="windows-1252") as f:
        data = json.load(f)
        # Cast to pandas dataframe
        df = pd.DataFrame(data["items"])

    # Save to csv
    df.to_csv("data/no_categorization/dataframe_TRAIN.csv", index=False, encoding='windows-1252')
    file_path = "data/no_categorization/export_TEST.json"
    with open(file_path, encoding="windows-1252") as f:
        data = json.load(f)
        # Cast to pandas dataframe
        df = pd.DataFrame(data["items"])

    # Save to csv
    df.to_csv("data/no_categorization/dataframe_TEST.csv", index=False, encoding='windows-1252')


if __name__ == "__main__":
    main()