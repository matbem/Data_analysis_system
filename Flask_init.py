from flask import Flask, render_template, request, jsonify
import os
import importlib.util
import csv

app = Flask(__name__)

FILES_FOLDER = 'CSV_FILES'  #CSV FILES
FUNCTIONS_FOLDER = 'Functions'  # FUNCTION FILES

def load_functions(filename):
    filepath = os.path.join(FUNCTIONS_FOLDER, filename) # route to our function

    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File {filename} not found")

    spec = importlib.util.spec_from_file_location("module", filepath)
    module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)
        print(f"Loaded functions: {module.__dict__.keys()}") # print loaded functions
        return { name: func for name, func in module.__dict__.items() if callable(func)}
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)})

@app.route("/")
def index():
    files = [f for f in os.listdir(FILES_FOLDER) if f.endswith(".csv") ]
    function_files = [f for f in os.listdir(FUNCTIONS_FOLDER) if f.endswith(".py")]
    functions = {file: load_functions(file) for file in function_files}
    return render_template('index.html', files=files, functions=functions)

@app.route("/execute", methods=["POST"])
def execute():
    data=request.json
    filename=data.get("filename")
    selected_function=data.get("functions" , [])
    function_file = data.get("function_file")
    filepath = os.path.join(FILES_FOLDER, filename)



if __name__ == '__main__':
    app.run(debug=True)
