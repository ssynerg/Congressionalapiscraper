from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Path to the processed CSV file
PROCESSED_BILLS_FILE = "bills_with_expenditures.csv"

@app.route('/')
def index():
    """
    Render the main webpage.
    """
    return render_template('index.html')

@app.route('/data')
def get_data():
    """
    Provide data as JSON for the frontend.
    """
    if os.path.exists(PROCESSED_BILLS_FILE):
        df = pd.read_csv(PROCESSED_BILLS_FILE)
        data = df.to_dict(orient='records')
        return jsonify(data)
    else:
        return jsonify({"error": "Processed file not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
