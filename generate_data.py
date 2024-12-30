import google.generativeai as genai
import os
import pandas as pd
import json

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

if __name__ == "__main__":
    data = generate_data_from_ddl("test.sql")
    print(data)