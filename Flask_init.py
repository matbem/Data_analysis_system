
from flask import Flask, render_template, request, jsonify, send_file
import os
import importlib.util
import pandas as pd
from Analysis.data_loader import load_csv_file
import Functions.analysys_functions
import Functions.plotting_functions
import pandas as pd
from fpdf import FPDF


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    functions = {**Functions.analysys_functions.get_all_functions(), **Functions.plotting_functions.get_all_functions()}
    uploaded_file = None
    columns = []

    if request.method == "POST":
        file = request.files.get("selected_file")
        if file:
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)
            uploaded_file = filename
            df = load_csv_file(uploaded_file)
            columns = df.columns.tolist()

    return render_template('index.html', functions=functions , columns=columns, uploaded_file=uploaded_file)

@app.route("/execute", methods=["POST"])
def execute():
    functions = {**Functions.analysys_functions.get_all_functions(), **Functions.plotting_functions.get_all_functions()}
    filename = request.form.get("uploaded_file")
    selected_function = request.form.getlist("functions")
    print(selected_function)
    args_map = {}

    for func in selected_function:
        args = request.form.getlist(f"args_{func}[]")
        print(args)
        args_map[func] = args
    print(args_map)
    df = load_csv_file(filename)
    if df.empty:
        print("No data found")

    results = {}
    for func_name, args in args_map.items():
        if func_name in functions:
            func = functions[func_name]
            try:
                results[func_name] = [func(df, *args_map[func_name]), *args_map[func_name]]
            except Exception as e:
                results[func_name] = f"Error executing {func_name}: {str(e)}"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Results of data analysis", ln=True, align="C")
    for func_name, result in results.items():
        pdf.cell(200, 10, txt=f"{func_name} of column: {result[1]}: {result[0]}", ln=True, align="L")

    pdf_path = os.path.join(UPLOAD_FOLDER, "results.pdf")
    pdf.output(pdf_path)

    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
