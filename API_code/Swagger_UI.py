import pandas as pd
import re
import csv
from flask import Flask, request, jsonify, Response
from flasgger import Swagger,swag_from 
import io
import sqlite3

app = Flask(__name__)
Swagger(app)
# Load the abusive and normalization CSV files
abusive_dict = pd.read_csv('abusive.csv', encoding='latin-1')
normalization_dict = pd.read_csv('normalization.csv', encoding='latin-1')


def clean_input_text(input_data):
    # Remove special characters and convert to lowercase
    cleansed_data = re.sub(r"[^a-zA-Z0-9\s]", "", input_data)
    cleansed_data = cleansed_data.lower()

    # Remove unnecessary char
    cleansed_data = re.sub(r"\n", "", cleansed_data)

    # Remove retweet symbol
    cleansed_data = re.sub(r"rt", "", cleansed_data)

    # Remove every username
    cleansed_data = re.sub(r"user", "", cleansed_data)

    # Remove URL
    cleansed_data = re.sub(r"http\S+", "", cleansed_data)

    # Split a String
    cleansed_data = re.sub(r"\s+", " ", cleansed_data)

    return cleansed_data.strip()


def clean_csv_file(input_file):
    csv_data = input_file.read().decode("latin-1")

    rows = []
    reader = csv.reader(csv_data.splitlines())
    header = next(reader)

    for row in reader:
        cleansed_row = [clean_input_text(value) for value in row]
        rows.append(cleansed_row)

    output_csv = [header] + rows

    # Create a pandas DataFrame from the cleansed CSV data
    df = pd.DataFrame(output_csv)

    # Convert the DataFrame to a CSV string
    input_csv = df.to_csv(index=False, header=False)

    return input_csv


@swag_from("gold/text_processing.yml", methods=["POST"])
@app.route("/clean_text", methods=["POST"])
def clean_text():
    # Retrieve the input text from the request form data
    input_data = request.form.get("input_text_data")

    # Check if the input data is provided
    if input_data is None:
        # Return an error message with HTTP status code 400
        return "Please provide input data.", 400

    try:
        # Call the clean_input_text function to perform the cleansing operations
        clean_text = clean_input_text(input_data)

        # Prepare the JSON response
        json_response = {"cleansed_text": clean_text}

        # Return the JSON response with HTTP status code 200
        return jsonify(json_response), 200

    except Exception as i:
        # Return an error message with HTTP status code 500 if an exception occurs
        return str(i), 500

def save_data_to_database(input_csv, cleaned_csv):
    conn = sqlite3.connect('cleansed_data.db')
    cursor = conn.cursor()

    # Create a table to store the input and cleaned CSV data
    cursor.execute('''CREATE TABLE IF NOT EXISTS csv_data (
                        id INTEGER PRIMARY KEY,
                        input_text TEXT,
                        cleaned_text TEXT
                    )''')

    # Insert the input and cleaned CSV data into the table
    cursor.execute("INSERT INTO csv_data (input_text, cleaned_text) VALUES (?, ?)",
                   (input_csv, cleaned_csv))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

@swag_from("gold/clean_csv.yml", methods=["POST"])
@app.route("/clean_csv", methods=["POST"])
def clean_csv():
    input_file = request.files.get("input_csv_file")

    if input_file and input_file.filename.endswith('.csv'):
        input_csv = clean_csv_file(input_file)
        df = pd.read_csv(io.StringIO(input_csv))

        replacements = zip(normalization_dict['TEXT'], normalization_dict['NORMALIZATION'])
        abusive_words = abusive_dict['ABUSIVE']

        for typo, rev in zip(normalization_dict['TEXT'], normalization_dict['NORMALIZATION']):
            df['Tweet'] = df['Tweet'].str.replace(r'\b{}\b'.format(typo), rev, regex=True)

        for abusive_word in abusive_dict['ABUSIVE']:
            df['Tweet'] = df['Tweet'].str.replace(r'\b{}\b'.format(abusive_word), '', regex=True)

        # Save the cleaned DataFrame to a new CSV file
        cleaned_csv_file = io.StringIO()
        df.to_csv(cleaned_csv_file, index=False)
        cleaned_csv_file.seek(0)
        cleaned_csv = cleaned_csv_file.getvalue()

        # Save the input and cleaned CSV data to the database
        save_data_to_database(input_csv, cleaned_csv)

        # Prepare the response to return the CSV file for download
        return Response(
            cleaned_csv_file,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=cleaned_data.csv"}
        )
    
    
    else:
    # Return an error message with HTTP status code 400 if there is no input file
     return "Please provide an input CSV file.", 400

if __name__ == "__main__":
    app.run(debug=True)