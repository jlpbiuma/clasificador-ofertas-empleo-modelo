import pandas as pd
from notebooks.functions.signature import create_diccionario_ocupaciones, get_offers_signature_relative, show_signature_by_occupation, delete_offers_same_occupation_by_signature
df_train = pd.read_json("./data/train/TRAIN.json", encoding='utf-8')
# Convert the name of the columns to uppercase
df_train.columns = map(str.upper, df_train.columns)
# Drop the null register if the PALABRAS_EMPLEO_TEXTO or CATEGORIA or SUBCATEGORIA is null
print("Before:" + str(df_train.shape))
df_train = df_train.dropna(subset=['PALABRAS_EMPLEO_TEXTO', 'CATEGORIA', 'SUBCATEGORIA'])
print("After:" + str(df_train.shape))
df_train['NUM_WORDS'] = df_train['PALABRAS_EMPLEO_TEXTO'].apply(lambda x: len(x.split(" ")) - 1)
# Shuffle the dataframe
df_train = df_train.sample(frac=1).reset_index(drop=True)
df_train.head(2)



print("Before: ", df_train.shape[0])
diccionario_ocupaciones = create_diccionario_ocupaciones(df_train)
df_train['RELATIVE_SIGNATURE'] = get_offers_signature_relative(df_train, diccionario_ocupaciones, precision=2)
df_signature = delete_offers_same_occupation_by_signature(df_train[df_train['ID_PUESTO_ESCO_ULL'] == 1607], maxOffers=200, totalOffers=200, precision=2)
print("After: ", df_signature.shape[0])