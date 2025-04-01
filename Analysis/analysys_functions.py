import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from data_loader import load_csv_file

def compute_mean(df):
    return np.mean(df)

def compute_std(df):
    return np.std(df)

def compute_median(df):
    return np.median(df)

def compute_percentiles(df,column_name,percentiles):
    return np.percentile(df[column_name],percentiles)

def compute_squared_difference(df,column_name):
    return list(map(lambda x: (x - compute_mean(df[column_name]))**2, df[column_name]))

def compute_variance(df, column_name):
    return np.sum(compute_squared_difference(df, column_name))/len(df[column_name]) #alright it works

def factorial_column(series):
    if series.empty:
        return series
    return series.apply


if __name__ == '__main__':
    df = load_csv_file("C:\\Users\\bemma\\University\\JPWP\\data.csv")
    print(compute_variance(df,"Duration"))
    print(np.var(df))