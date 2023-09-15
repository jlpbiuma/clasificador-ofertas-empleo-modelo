from collections import Counter
import matplotlib.pyplot as plt

def clean_descripcion(df):
    # Get the column descripcion_oferta which is a string delete additional spaces and split it into a list of words for each register
    # Access the "descripcion_oferta" column and apply the desired transformations
    df['descripcion_oferta'] = df['descripcion_oferta'].str.strip()  # Remove leading/trailing spaces
    df['descripcion_oferta'] = df['descripcion_oferta'].str.replace(r'\s+', ' ')  # Remove additional spaces
    df['descripcion_oferta'] = df['descripcion_oferta'].str.replace('.', ' ')  # Replace "." with " "

    # Split the cleaned text into a list of words using both " " and "." as separators
    df['descripcion_oferta_words'] = df['descripcion_oferta'].str.split('[ .]')
    # Delete all '' elements inside the list of words
    df['descripcion_oferta_words'] = df['descripcion_oferta_words'].apply(lambda x: list(filter(None, x)))
    # Delete all ' ' elements inside the list of words
    df['descripcion_oferta_words'] = df['descripcion_oferta_words'].apply(lambda x: list(filter(lambda a: a != ' ', x)))
    # Delete all the elements inside the elements of the list of words that are not letters mayus or minus
    df['descripcion_oferta_words'] = df['descripcion_oferta_words'].apply(lambda x: list(filter(lambda a: a.isalpha(), x)))
    # Cast every word to lowercase
    df['descripcion_oferta_words'] = df['descripcion_oferta_words'].apply(lambda x: list(map(lambda a: a.lower(), x)))
    return df

def create_words_count_fulldataset(df):
    # Now create a dict which key is the word and the value is the number of times that word appears in the dataset
    # Create a list of all the words in the dataset
    words = []
    for i in range(df.shape[0]):
        words.extend(df['descripcion_oferta_words'].iloc[i])
    # Create a dict with the number of times each word appears in the dataset
    words_dict = {}
    for word in words:
        if word in words_dict:
            words_dict[word] += 1
        else:
            words_dict[word] = 1
    return words_dict

def create_words_count_groupdataset(df):
    # Group by 'id_puesto_esco_ull' and concatenate the lists within each group
    df_grouped = df.groupby('id_puesto_esco_ull')['descripcion_oferta_words'].apply(lambda x: [word for words in x for word in words])
    # Create a dictionary to store the word frequencies for each group
    result_dict = {}
    # Iterate through the groups and count word frequencies
    for group, row in df_grouped.items():
        word_freq = Counter(row)
        result_dict[group] = dict(word_freq)
    return result_dict

def filter_stop_words(words, stop_words):
    for stop_word in stop_words:
        if stop_word in words:
            del words[stop_word]
    return words


def filter_stop_words_grouped(words_group, stop_words):
    # Now delete all the grouped_words which are in the stop_words list (the first keys are the id_puesto_esco_ull)
    for key in words_group.keys():
        words_group[key] = filter_stop_words(words_group[key], stop_words)
    return words_group

def plot_words_count(words, N=50):
    # Sort the 'words' dictionary by count in descending order
    sorted_words = dict(sorted(words.items(), key=lambda item: item[1], reverse=True))

    # Take the top 50 most repeated words
    top_N_words = dict(list(sorted_words.items())[:N])

    # Extract the words and counts for plotting
    top_N_words_list = list(top_N_words.keys())
    top_N_counts_list = list(top_N_words.values())

    # Create a horizontal bar plot
    plt.figure(figsize=(8, 12))
    plt.barh(top_N_words_list, top_N_counts_list, color='skyblue')
    plt.xlabel('Count')
    plt.ylabel('Word')
    plt.title('Top ' + str(N) + ' Most Repeated Words')
    plt.gca().invert_yaxis()  # Invert the Y-axis to have the most repeated words at the top
    plt.tight_layout()
    plt.show()
    
def plot_words_count_grouped(words_group, id, N=50):
    try:
        plot_words_count(words_group[id], N)
    except:
        print('The id ' + str(id) + ' is not in the dataset')