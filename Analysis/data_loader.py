import pandas as pd

def load_csv_file(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return None         #here when do we get none we have to make alert in the web app that file was not found

