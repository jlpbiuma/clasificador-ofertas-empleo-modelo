from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

correct_name = 'df_corrects_julio_agosto_no_filtro_no_asunto.csv'
error_name = 'df_errors_julio_agosto_no_filtro_no_asunto.csv'
# Load your DataFrame
df_aciertos = pd.read_csv('templates/' + correct_name).sort_values(by="PROBABILITY", ascending=False)
# df_aciertos = pd.read_csv('templates/df_corrects_julio_agosto_no_filtro_no_asunto.csv').sort_values(by="PROBABILITY", ascending=False)
df_errores = pd.read_csv('templates/' + error_name).sort_values(by="PROBABILITY", ascending=False)
probabilities = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

df_aciertos_filter = pd.read_csv('templates/df_corrects_julio_agosto_filtro_no_asunto.csv').sort_values(by="PROBABILITY", ascending=False)
df_errores_filter = pd.read_csv('templates/df_errors_julio_agosto_filtro_no_asunto.csv').sort_values(by="PROBABILITY", ascending=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/filter', methods=['POST'])
def filter():
    probability_distribution_image_url = 'distribution_filtro.png'
    precision_image_url = 'all_filtro.png'
    total_ofertas = df_aciertos_filter.shape[0] + df_errores_filter.shape[0]
    print(total_ofertas)
    return render_template('filter.html', total_ofertas=total_ofertas, probability_distribution_image_url=probability_distribution_image_url, precision_image_url=precision_image_url)

@app.route('/filter/aciertos', methods=['POST'])
def aciertos_filter():
    enumerated_data = list(enumerate(df_aciertos_filter.to_dict('records')))
    image_url = 'correct_filtro.png'  # Set the image URL here
    return render_template('listado.html', name="aciertos", enumerated_data=enumerated_data, image_url=image_url, probabilities=probabilities)

@app.route('/filter/errores', methods=['POST'])
def errores_filter():
    enumerated_data = list(enumerate(df_errores_filter.to_dict('records')))
    image_url = 'errors_filtro.png'  # Set the image URL here
    return render_template('listado.html', name="errores", enumerated_data=enumerated_data, image_url=image_url, probabilities=probabilities)


@app.route('/no_filter', methods=['POST'])
def no_filter():
    probability_distribution_image_url = 'distribution.png'
    precision_image_url = 'all.png'
    total_ofertas = df_aciertos.shape[0] + df_errores.shape[0]
    return render_template('no_filter.html', total_ofertas=total_ofertas, probability_distribution_image_url=probability_distribution_image_url, precision_image_url=precision_image_url)

@app.route('/no_filter/aciertos', methods=['POST'])
def aciertos_no_filter():
    enumerated_data = list(enumerate(df_aciertos.to_dict('records')))
    image_url = 'correct.png'  # Set the image URL here
    return render_template('listado.html', name="aciertos", enumerated_data=enumerated_data, image_url=image_url, probabilities=probabilities)

@app.route('/no_filter/errores', methods=['POST'])
def errores_no_filter():
    enumerated_data = list(enumerate(df_errores.to_dict('records')))
    image_url = 'errors.png'  # Set the image URL here
    return render_template('listado.html', name="errores", enumerated_data=enumerated_data, image_url=image_url, probabilities=probabilities)

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
