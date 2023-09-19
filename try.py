import pandas as pd
import spacy
import nltk
from nltk.stem import WordNetLemmatizer
from notebooks.functions.tools import load_json

# Download the NLTK data for Spanish
nltk.download('wordnet')

# Load your JSON data here
# Replace 'your_data.json' with the actual path to your JSON file
data = load_json('./data/train/train_descripcion_accents.json')

# Now cast data to a DataFrame
df = pd.DataFrame(data)

print("Before: " + str(df['descripcion_oferta'].iloc[0]))

# Load the Spanish language model for spaCy
nlp = spacy.load("es_core_news_sm")

# Create a lemmatizer using NLTK
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    # Process the text using spaCy
    doc = nlp(text)
    
    # Lemmatize the verbs to their infinitive form using NLTK
    cleaned_tokens = [lemmatizer.lemmatize(token.text, 'v') if token.pos_ == 'VERB' else token.text for token in doc]
    
    # Join the cleaned tokens back into a text
    cleaned_text = ' '.join(cleaned_tokens)
    return cleaned_text

# Apply the clean_text function to the 'descripcion_oferta' column
# Take the first 10 records of the df
new_df = df['descripcion_oferta'].iloc[:11]
examples = new_df.apply(clean_text)
print("After: " + examples[0])
