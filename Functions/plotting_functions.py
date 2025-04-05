import matplotlib.pyplot as plt
import seaborn as sns

def plot_distribution(df, column_name):
    fig, ax = plt.subplots()
    sns.histplot(df[column_name], kde=True, ax=ax)
    ax.set_title(f"Rozkład kolumny {column_name}")
    return fig

def plot_central_tendency(df, column_name):
    fig, ax = plt.subplots()
    sns.histplot(df[column_name], kde=True, ax=ax)
    ax.axvline(df[column_name].mean(), color='r', linestyle='--', label='Średnia')
    ax.axvline(df[column_name].median(), color='g', linestyle='--', label='Mediana')
    ax.axvline(df[column_name].mode()[0], color='b', linestyle='--', label='Moda')
    ax.set_title(f"Miary tendencji centralnej kolumny {column_name}")
    ax.legend()
    return fig

def plot_spread(df, column_name):
    fig, ax = plt.subplots()
    sns.boxplot(x=df[column_name], ax=ax)
    ax.set_title(f"Rozkład kolumny {column_name}")
    return fig

def plot_outliers(df, column_name):
    fig, ax = plt.subplots()
    sns.boxplot(x=df[column_name], ax=ax)
    ax.set_title(f"Wykrywanie wartości odstających w kolumnie {column_name}")
    return fig

def plot_correlation_matrix(df):
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
    ax.set_title("Macierz korelacji")
    return fig

def plot_trend_over_index(df, column_name):
    fig, ax = plt.subplots()
    sns.lineplot(x=range(len(df[column_name])), y=df[column_name], ax=ax)
    ax.set_title(f"Trend kolumny {column_name}")
    return fig
