
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
        return jsonify({"error": str(e)})

@app.route("/")
def index():
    files = [f for f in os.listdir(FILES_FOLDER) if f.endswith(".csv")]
    function_files = [f for f in os.listdir(FUNCTIONS_FOLDER) if f.endswith(".py")]
    functions = {file: list(load_functions(file).keys()) for file in function_files}
    return render_template('index.html', files=files, functions=functions)

@app.route("/execute", methods=["POST"])
def execute():
    data = request.json
    filename = data.get("filename")
    selected_function = data.get("functions", [])
    function_file = data.get("function_file")
    args_map = data.get("args", {})

    filepath = os.path.join(FILES_FOLDER, filename)

    if not os.path.isfile(filepath):
        return jsonify({"error": f"File {filename} not found"})

    df = load_csv_file(filepath)
    if df is None:
        return jsonify({"error": f"Plik '{filename}' nie został znaleziony."})

    functions_in_file = load_functions(function_file)
    if not functions_in_file:
        return jsonify({"error": f"Function file {function_file} not found or failed to load."})

    results = {}
    for func_name in selected_function:
        function = functions_in_file.get(func_name)
        if function:
            try:
                args = args_map.get(func_name, [])
                results[func_name] = function(df, *args)
            except Exception as e:
                results[func_name] = {"error": str(e)}
        else:
            results[func_name] = {"error": f"Function {func_name} not found in {function_file}"}

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
