import os
import pandas as pd
from flask import Flask, request, render_template, send_file, redirect, url_for

import json
import os
from generate_data import generate_data_from_ddl

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
