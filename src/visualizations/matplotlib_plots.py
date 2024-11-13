import seaborn as sns
import matplotlib.pyplot as plt


def set_plot_style(style="whitegrid"):
    """
    Set the style for the plots.

    Parameters:
    style (str): The style to use for the plots. Default is 'whitegrid'.
    """
    sns.set_style(style)


def plot_histogram(
    data, bins=10, title="Histogram", xlabel="Values", ylabel="Frequency"
):
    """
    Plot a histogram of the data.

    Parameters:
    data (array-like): The data to plot.
    bins (int): The number of bins to use for the histogram. Default is 10.
    title (str): The title of the plot. Default is 'Histogram'.
    xlabel (str): The label for the x-axis. Default is 'Values'.
    ylabel (str): The label for the y-axis. Default is 'Frequency'.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=bins, edgecolor="black")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def plot_scatter(x, y, title="Scatter Plot", xlabel="X-axis", ylabel="Y-axis"):
    """
    Plot a scatter plot of the data.

    Parameters:
    x (array-like): The data for the x-axis.
    y (array-like): The data for the y-axis.
    title (str): The title of the plot. Default is 'Scatter Plot'.
    xlabel (str): The label for the x-axis. Default is 'X-axis'.
    ylabel (str): The label for the y-axis. Default is 'Y-axis'.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, edgecolor="black")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def plot_line(x, y, title="Line Plot", xlabel="X-axis", ylabel="Y-axis"):
    """
    Plot a line plot of the data.

    Parameters:
    x (array-like): The data for the x-axis.
    y (array-like): The data for the y-axis.
    title (str): The title of the plot. Default is 'Line Plot'.
    xlabel (str): The label for the x-axis. Default is 'X-axis'.
    ylabel (str): The label for the y-axis. Default is 'Y-axis'.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker="o")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def plot_boxplot(data, title="Box Plot", xlabel="Categories", ylabel="Values"):
    """
    Plot a box plot of the data.

    Parameters:
    data (array-like): The data to plot.
    title (str): The title of the plot. Default is 'Box Plot'.
    xlabel (str): The label for the x-axis. Default is 'Categories'.
    ylabel (str): The label for the y-axis. Default is 'Values'.
    """
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
