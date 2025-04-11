from flask import Flask, render_template, request, jsonify, send_file
import os
import importlib.util
import pandas as pd
from Analysis.data_loader import load_csv_file
import Functions.analysys_functions
import Functions.plotting_functions
import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt
from sympy.physics.units import coulomb

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
functions = {**Functions.analysys_functions.get_all_functions(), **Functions.plotting_functions.get_all_functions()}


def get_function_args_info():
    args_info = {}
    for func_name, func in functions.items():
        if func.__code__.co_argcount > 2:
            args_info[func_name] = func.__code__.co_argcount-1
        else:
            args_info[func_name] = 1
    return args_info


@app.route("/", methods=["GET", "POST"])
def index():
    uploaded_file = None
    columns = []
    args_info = get_function_args_info()

    if request.method == "POST":
        file = request.files.get("selected_file")
        if file:
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)
            uploaded_file = filename
            df = load_csv_file(uploaded_file)
            columns = df.columns.tolist()

    return render_template('index.html', functions=functions, columns=columns, uploaded_file=uploaded_file, args_info=args_info)


@app.route("/execute", methods=["POST"])
def execute():
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

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Results of data analysis", ln=True, align="C")

    for func_name, args in args_map.items():
        if func_name in functions:
            func = functions[func_name]
            try:
                columns = args_map[func_name]
                result = func(df, *columns)
                if isinstance(result, plt.Figure):
                    fig_path = os.path.join(UPLOAD_FOLDER, f"{func_name}.png")
                    result.savefig(fig_path)
                    plt.close(result)
                    pdf.cell(200, 10, txt=f"{func_name} of column: {', '.join(map(str, columns))}:", ln=True, align="L")
                    pdf.image(fig_path, x=10, y=None, w=180)
                else:
                    pdf.cell(200, 10, txt=f"{func_name} of column: {', '.join(map(str, columns))}: {result}", ln=True, align="L")
            except Exception as e:
                pdf.cell(200, 10, txt=f"Error generating result for {func_name}: {str(e)}", ln=True, align="L")


    pdf_path = os.path.join(UPLOAD_FOLDER, "results.pdf")
    pdf.output(pdf_path)

    return send_file(pdf_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
