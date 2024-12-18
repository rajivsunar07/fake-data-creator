import os
import pandas as pd
from flask import Flask, request, render_template, send_file, redirect, url_for

import json
import google.generativeai as genai
import os



# Your function to generate the DataFrame
def generate_data_from_ddl(ddl_file_path):
    """
    Placeholder function that reads a DDL file and generates a DataFrame.
    Replace this with your actual function.
    """

    genai.configure(api_key=os.getenv("api_key"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    with open(ddl_file_path, 'r') as f:
        ddl = f.readlines()
    response = model.generate_content(f"""I have this ddl I want to create 10 rows of data from this ddl. 
    Please do not output anything else.
    Just the data will be enough in JSON format, do not write anything except for the data.
    I also do not want json to be written at the front of the response.
    {ddl}""")
    data = pd.DataFrame(json.loads(response.text))
    return data

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    # Save uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Generate DataFrame and save to CSV
    try:
        df = generate_data_from_ddl(file_path)
        output_csv = os.path.join(app.config['UPLOAD_FOLDER'], 'output.csv')
        df.to_csv(output_csv, index=False)
    except Exception as e:
        return f"Error processing file: {e}"

    return send_file(output_csv, as_attachment=True)
