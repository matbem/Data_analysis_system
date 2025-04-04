import matplotlib.pyplot as plt
import numpy as np

def linear_plot(x, y, xlabel, ylabel, title, grid):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    if grid:
        ax.grid()
    return fig

def scatter_plot(x, y, xlabel, ylabel, title, grid):
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    if grid:
        ax.grid()
    return fig

