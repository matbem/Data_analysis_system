import matplotlib.pyplot as plt
import seaborn as sns

def plot_distribution(df, column_name):
    fig, ax = plt.subplots()
    sns.histplot(df[column_name], kde=True, ax=ax)
    ax.set_title(f"Distribution of column {column_name}")
    return fig

def plot_central_tendency(df, column_name):
    fig, ax = plt.subplots()
    sns.histplot(df[column_name], kde=True, ax=ax)
    ax.axvline(df[column_name].mean(), color='r', linestyle='--', label='Mean')
    ax.axvline(df[column_name].median(), color='g', linestyle='--', label='Median')
    ax.axvline(df[column_name].mode()[0], color='b', linestyle='--', label='Mode')
    ax.set_title(f"Central tendency measures of column {column_name}")
    ax.legend()
    return fig

def plot_outliers(df, column_name):
    fig, ax = plt.subplots()
    sns.boxplot(x=df[column_name], ax=ax)
    ax.set_title(f"Outlier detection in column {column_name}")
    return fig

def plot_correlation_matrix(df):
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
    ax.set_title("Correlation matrix")
    return fig

def plot_trend_over_index(df, column_name):
    fig, ax = plt.subplots()
    sns.lineplot(x=range(len(df[column_name])), y=df[column_name], ax=ax)
    ax.set_title(f"Trend of column {column_name} over index")
    return fig

def plot_scatter(df, column_name1, column_name2):
    fig, ax = plt.subplots()
    sns.scatterplot(x=df[column_name1], y=df[column_name2], ax=ax)
    ax.set_title(f"Scatter plot of columns {column_name1} and {column_name2}")
    return fig

def plot_violin(df, column_name):
    fig, ax = plt.subplots()
    sns.violinplot(x=df[column_name], ax=ax)
    ax.set_title(f"Violin plot of column {column_name}")
    return fig

def get_all_functions():
    return {
        "Plot distribution": plot_distribution,
        "Plot central tendency": plot_central_tendency,
        "Plot outliers": plot_outliers,
        "Plot correlation_matrix": plot_correlation_matrix,
        "Plot trend over index": plot_trend_over_index,
        "Plot scatter": plot_scatter,
        "Plot violin": plot_violin
    }