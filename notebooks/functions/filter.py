import pandas as pd

def drop_randomly_most_offers(df, maxOffers=1000, totalOffers=1000):
    # Get the value counts for 'ID_PUESTO_ESCO_ULL'
    value_counts = df['ID_PUESTO_ESCO_ULL'].value_counts()

    # Identify values with more than 1000 records
    values = value_counts[value_counts > maxOffers].index

    # Find the rows where 'ID_PUESTO_ESCO_ULL' is in values
    df_train_filter = df[df['ID_PUESTO_ESCO_ULL'].isin(values)]

    # Now delete randomly the register until the number of registers is 1000 for each 'ID_PUESTO_ESCO_ULL'
    df_train_filter = df_train_filter.groupby('ID_PUESTO_ESCO_ULL').apply(lambda x: x.sample(totalOffers)).reset_index(drop=True)

    # Drop the Registers that have more than 1000 registers in the original dataframe
    df = df[~df['ID_PUESTO_ESCO_ULL'].isin(values)]

    # Now join both dataframes
    df = pd.concat([df, df_train_filter], ignore_index=True)

    # Shuffle the positions of rows randomly
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df

def delete_offers_with_less_words(df, value):
    return df[df['NUM_WORDS'] > value]