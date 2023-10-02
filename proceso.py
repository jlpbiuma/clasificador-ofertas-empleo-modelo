from notebooks.functions.verbs_dictionary import *
# Read all the verbs
verbs = read_verbs("./data/diccionario/verbos-espanol.txt")
# Read the dictionary
verbs_df = read_dictionary("./data/diccionario/df_structured_verbos.csv")
# Create the dictionary
verbs_df, errores = create_dictionary(verbs, verbs_df)
# Create all conjugations list
all_conjugations = create_all_conjugations_list(verbs_df)
# Write the dictionary
write_dictionary(verbs_df, "./data/diccionario/df_structured_verbos.csv")
# Save all conjugations list
with open("./data/diccionario/all_conjugations.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(all_conjugations))
# Save errors
with open("./data/diccionario/errores.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(errores))