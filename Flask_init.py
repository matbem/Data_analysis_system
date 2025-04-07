
from flask import Flask, render_template, request, jsonify
import os
import importlib.util
import pandas as pd
from Analysis.data_loader import load_csv_file


app = Flask(__name__)

FILES_FOLDER = 'CSV_FILES'  # CSV FILES
FUNCTIONS_FOLDER = 'Functions'  # FUNCTION FILES

def load_functions(filename):
    filepath = os.path.join(FUNCTIONS_FOLDER, filename)  # route to our function

    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File {filename} not found")

    spec = importlib.util.spec_from_file_location("module", filepath)
    module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)
        print(f"Loaded functions: {module.__dict__.keys()}")  # print loaded functions
        return {name: func for name, func in module.__dict__.items() if callable(func)}
    except Exception as e:
        print(e)


@app.route("/", methods=["GET", "POST"])
def index():
    files = [f for f in os.listdir(FILES_FOLDER) if f.endswith(".csv")]
    function_files = [f for f in os.listdir(FUNCTIONS_FOLDER) if f.endswith(".py")]
    functions = {file: list(load_functions(file).keys()) for file in function_files}

    selected_file = request.form.get("selected_file")
    columns = []

    if selected_file:
        file_path = os.path.join(FILES_FOLDER, selected_file)
        df = load_csv_file(file_path)
        if not df.empty:
            columns = df.columns.tolist()



    return render_template('index.html', files=files, functions=functions , columns=columns)

@app.route("/execute", methods=["POST"])
def execute():
    filename = request.form.get("selected_file")
    selected_function = request.form.get("functions")
    args_map={}

    for func in selected_function:
        args = request.form.getlist(f"args[{func}][]")
        args_map[func] = args
    file_path = os.path.join(FILES_FOLDER, filename)
    df = load_csv_file(file_path)
    if df is None or df.empty:
        return render_template("result.html",results={}, error="No data found")

    function_file = [f for f in os.listdir(FUNCTIONS_FOLDER) if f.endswith(".py")][0]
    functions = load_functions(function_file)

    results = {}
    for func in selected_function:
        try:
            results[func] = functions[func](df, *args_map[func])
        except Exception as e:
            results[func] = str(e)


    return render_template("result.html", results=results)






if __name__ == '__main__':
    app.run(debug=True)
