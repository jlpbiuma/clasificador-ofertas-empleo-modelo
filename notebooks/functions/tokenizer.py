def custom_tokenizer_category_subcategory(text):
    # this functions returns a list with the text with underscores instead of spaces
    text_with_underscores = text.replace(' ', '_')
    return [text_with_underscores]


def custom_tokenizer_palabras_empleo_texto(text):
    # This function returns a list with the text splitted by spaces
    elements = text.strip().split(" ")
    return elements
