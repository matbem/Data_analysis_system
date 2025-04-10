import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from functools import reduce
import scipy.stats as stats

def compute_mean(df, column_name):
    return sum(df[column_name])/len(df[column_name])

def compute_std(df, column_name):
    return compute_variance(df, column_name)**0.5

def compute_median(df, column_name):
    return ((lambda sorted_col:
                sorted_col[len(sorted_col)//2]
                if len(sorted_col) % 2 == 1
                else (sorted_col[len(sorted_col)//2] + sorted_col[len(sorted_col)//2 - 1]) / 2)
            (sorted(df[column_name])))

def compute_percentiles(df, column_name, percentile):
    sorted_col = sorted(df[column_name])
    index = int(percentile / 100 * (len(sorted_col) - 1))
    return sorted_col[index]  # ta funkcje troche zmienilem bo mi wywalalo blad przez nia


def compute_squared_difference(df,column_name):
    return list(map(lambda x: (x - compute_mean(df, column_name))**2, df[column_name]))

def compute_variance(df, column_name):
    return np.sum(compute_squared_difference(df, column_name))/len(df[column_name]) #alright it works

def compute_covariance(df, column_name1, column_name2):
    if len(df[column_name1]) != len(df[column_name2]) or len(df[column_name1]) < 2:
        return None
    return reduce(
            lambda acc, xy: acc + (xy[0] - compute_mean(df[column_name1])) * (xy[1] - compute_mean(df[column_name2])),
            zip(df[column_name1], df[column_name2]),
            0
        ) / (len(df[column_name1]) - 1)

def factorial_column(df, column_name):
    if df[column_name].empty:
        return df[column_name]
    return df[column_name].apply(lambda x: math.factorial(int(x)) if x >= 0 else None) # i tutaj zmienilem ta koncowke po .apply

def recursive_sum(df, column_name):
    return lambda: 0 if df.empty else df[column_name].iloc[0] + recursive_sum(df.iloc[1:], column_name)()

def compute_corelation(df, column_name1, column_name2):
    if len(df[column_name1]) != len(df[column_name2]) or len(df[column_name1]) < 2:
        return None
    return compute_covariance(df, column_name1, column_name2)/(compute_std(df[column_name1]) * compute_std(df[column_name2]))

def get_all_functions():
     return {
        "Mean": compute_mean,
        "Standard deviation": compute_std,
        "Median": compute_median,
        "Percentiles": compute_percentiles,
        "Squared difference": compute_squared_difference,
        "Variance": compute_variance,
        "Covariance": compute_covariance,
        "Factorial": factorial_column,
        "Recursive_sum": recursive_sum,
        "Correlation": compute_corelation
    }
