import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    csv_data = pd.read_csv('./data/descripcion_ofertas_infojobs_21_23_test.csv', sep=';')
    return render_template('index.html', data=csv_data.to_html(classes='table table-striped', index=False, header=False))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)
