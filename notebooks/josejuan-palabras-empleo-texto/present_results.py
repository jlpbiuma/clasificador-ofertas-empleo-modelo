import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

def read_csv(file_path):
    return pd.read_csv(file_path)

@app.route('/')
def index():
    print("Enters")
    csv_data = read_csv('./data/results.csv')  # Replace with your actual CSV file path
    return render_template('index.html', data=csv_data.to_html(classes='table table-striped', index=False, header=False))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)
