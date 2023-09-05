import pandas as pd
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.io import output_notebook
import pandas as pd
import numpy as np

def create_diccionario_ocupaciones(df):
    # Get all possible ID_PUESTO_ESCO_ULL
    occupations = df['ID_PUESTO_ESCO_ULL'].unique()
    # Diccionario de ocupaciones
    diccionario_ocupaciones = {}
    # Iterate over all occupations
    for occupation_id in occupations:
        # Get all rows with the current occupation
        occupation_df = df[df['ID_PUESTO_ESCO_ULL'] == occupation_id]
        # Get all words in the current occupation
        diccionario_ocupacion = {}
        # Iterate over all offers
        for oferta in occupation_df['PALABRAS_EMPLEO_TEXTO']:
            # Get all words in the current offer deleting the last space
            for palabra in oferta.split(" ")[:-1]:
                # If the word is not in the dictionary, add it
                if palabra not in diccionario_ocupacion:
                    diccionario_ocupacion[palabra] = 1
                # If the word is in the dictionary, add 1 to the counter
                else:
                    diccionario_ocupacion[palabra] += 1
        # Add the occupation dictionary to the occupations dictionary
        diccionario_ocupaciones[occupation_id] = diccionario_ocupacion
    return diccionario_ocupaciones

def create_diccionario_full_dataset(df):
    # Get all words in the current occupation
    diccionario_ocupacion = {}
    # Iterate over all offers
    for oferta in df['PALABRAS_EMPLEO_TEXTO']:
        # Get all words in the current offer deleting the last space
        for palabra in oferta.split(" ")[:-1]:
            # If the word is not in the dictionary, add it
            if palabra not in diccionario_ocupacion:
                diccionario_ocupacion[palabra] = 1
            # If the word is in the dictionary, add 1 to the counter
            else:
                diccionario_ocupacion[palabra] += 1
    return diccionario_ocupacion

def get_offers_signature_relative(df, diccionario_ocupacion, precision=2):
    # Get all possible ID_PUESTO_ESCO_ULL
    occupations = df['ID_PUESTO_ESCO_ULL'].unique()
    # Create a new column in the dataframe
    df['RELATIVE_SIGNATURE'] = 0.0  # Initialize as float
    # Iterate over all occupations
    for occupation_id in occupations:
        # Get all rows with the current occupation
        occupation_df = df[df['ID_PUESTO_ESCO_ULL'] == occupation_id]
        # Iterate over all offers
        signatures = []
        for oferta in occupation_df['PALABRAS_EMPLEO_TEXTO']:
            # Start the signature as a float
            signature = 0.0
            # Iterate over all words in the current offer
            for word in oferta.split(" ")[:-1]:
                signature += diccionario_ocupacion[occupation_id][word]
            # Add the signature to the list of signatures
            signatures.append(signature)
        # Now for the same occupation divide all signatures by the max signature
        max_signature = max(signatures)
        # Iterate over all signatures and round them to 2 decimals
        for i in range(len(signatures)):
            signatures[i] = round(signatures[i] / max_signature, precision)
        # Add the signatures to the dataframe
        df.loc[df['ID_PUESTO_ESCO_ULL'] == occupation_id, 'RELATIVE_SIGNATURE'] = signatures
    return df['RELATIVE_SIGNATURE']

def delete_offers_same_occupation_by_signature(df, maxOffers=10, totalOffers=10, precision=2):
    # Group by ID_PUESTO_ESCO_ULL
    grouped = df.groupby('ID_PUESTO_ESCO_ULL')
    # Desviation
    sigma = 10 ** -(precision + 1)
    # Calculate step size
    step_size = 10 ** -precision
    # Initialize an empty list to store DataFrames for each relative signature
    array_occupations_ids = []
    # Loop over all occupations
    for occupation_id, occupation_df in grouped:
        for i in np.arange(0, 1 + step_size, step_size):
            # Get all rows with the current relative signature
            print(i - sigma, i + sigma)
            min_lim_condition = occupation_df['RELATIVE_SIGNATURE'] >= i - sigma
            max_lim_condition = occupation_df['RELATIVE_SIGNATURE'] <= i + sigma
            relative_signature_df = occupation_df[min_lim_condition & max_lim_condition]
            if len(relative_signature_df) > maxOffers:
                # If the number of rows is greater than maxOffers, sample randomly to limit to totalOffers
                relative_signature_df = relative_signature_df.sample(n=totalOffers, random_state=42)  # Adjust random_state as needed
            if len(relative_signature_df) > 0:
                # Get the IDs of the offers
                array_occupations_ids.extend(relative_signature_df['ID_OFERTA'].tolist())
    # Convert the array to a DataFrame or Series
    ids = pd.DataFrame(array_occupations_ids, columns=['ID_OFERTA'])
    # Use .isin() to filter rows
    filtered_df = df[df['ID_OFERTA'].isin(ids['ID_OFERTA'])]
    return filtered_df

def show_signature_by_occupation(df, id_ocupacion):
    # Filter and sort the data
    filtered_df = df[df['ID_PUESTO_ESCO_ULL'] == id_ocupacion]
    sorted_df = filtered_df.sort_values(by='RELATIVE_SIGNATURE', ascending=False).reset_index(drop=True)

    # Initialize Bokeh
    output_notebook()

    # Create a ColumnDataSource to store data
    source = ColumnDataSource(sorted_df)

    # Create a figure
    p = figure(
        title='Relative Signature for Occupation ' + str(id_ocupacion),
        x_axis_label='Data Point Index',
        y_axis_label='Relative Signature',
        tools="pan,box_zoom,wheel_zoom,reset,save",
    )

    # Add scatter plot markers
    p.circle(x='index', y='RELATIVE_SIGNATURE', size=8, source=source)

    # Add hover tool to display values on hover
    hover = HoverTool()
    hover.tooltips = [("Value", "@RELATIVE_SIGNATURE"), ("ID_OFERTA", "@ID_OFERTA")]
    p.add_tools(hover)

    # Show the plot
    show(p, notebook_handle=True)
    
def get_offers_by_relative_signature_and_occupation(df, occupation_id, relative_signature):
    # Get all rows with the current occupation
    occupation_df = df[df['ID_PUESTO_ESCO_ULL'] == occupation_id]
    # Get all rows with the current relative signature
    relative_signature_df = occupation_df[occupation_df['RELATIVE_SIGNATURE'] == relative_signature]
    # Return the offers
    return relative_signature_df['ID_OFERTA'].tolist()