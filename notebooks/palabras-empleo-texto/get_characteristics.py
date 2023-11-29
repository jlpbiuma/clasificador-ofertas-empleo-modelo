from functions.characteristics import *

df_offers = pd.read_json("./notebooks/palabras-empleo-texto/data/descripcion_ofertas_infojobs_21_23.json")

def get_characteristics(df_offers, index):
    offer = df_offers.iloc[index]
    # Get the words from the description
    offer["PALABRAS_LEGACY"] = f_vector_palabras_json(offer["descripcion_oferta"])
    offer["COLLOCATIONS_LEGACY"] = json.loads(f_vector_collocation_json(offer["descripcion_oferta"]))["vector_collocation"]
    offer["PALABRAS_NEW"] = get_words_by_text(offer["descripcion_oferta"])
    offer["COLLOCATIONS_NEW"] = get_collocations(offer["descripcion_oferta"])
    return offer.to_dict()

offer = get_characteristics(df_offers, 977)
print(offer)