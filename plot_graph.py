import matplotlib
# force matplotlib to not use any Xwindows backend.
# see https://stackoverflow.com/a/4706614/8225672 for why
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from datetime import datetime as dt
from log_csv import read_csv

title= 'Temperatura'
date_label = 'Horário'
temp_label = 'Temperatura °C'
date_fmt = '%H:%M:%S'
temp_interval = 2

def draw_line_graph(plot_gaussian=False):
    rows = read_csv()
    timestamps = []
    dates = [] # x
    temps = [] # y

    for row in rows:
        timestamps.append(int(row[0]))
        temps.append(float(row[2]))

    for ts in timestamps:
        dates.append(dt.fromtimestamp(ts))

    fig, ax = plt.subplots(1,1)
    ax.plot(dates,temps, alpha=0.8, linewidth=0.9, label="Binominal")

    # also plot gaussian (normal) distribution
    if plot_gaussian is True:
        temps_smooth = gaussian_filter1d(temps, sigma=30)
        ax.plot(dates, temps_smooth, color='red',
                linestyle='dashed', linewidth=1.5, label="Gaussian")

        # put a legend
        plt.legend(loc='best')

    # x (date) formatting
    xfmt = md.DateFormatter(date_fmt)
    ax.xaxis.set_major_formatter(xfmt)

    # manually set temp tick interval
    if abs(min(temps) - max(temps)) > 2:
        plt.yticks(np.arange(min(temps), max(temps)+1, temp_interval))

    # increase frequency of date tick interval
    loc = md.AutoDateLocator(minticks=20, maxticks=30, interval_multiples=True)
    ax.xaxis.set_major_locator(loc)

    # add a grid
    ax.grid()

    # set labels
    plt.xlabel(date_label)
    plt.ylabel(temp_label)
    plt.title(title)

    # set how the plot labels are displayed
    plt.subplots_adjust(bottom=0.2)
    plt.xticks(rotation=50)

    # set the figure size to 1920x1080
    fig.set_size_inches(19.2, 10.8)
    plt.savefig("test.png")


if __name__ == "__main__": # if calling directly show graph
    from os import system
    draw_line_graph()
    system('pqiv test.png')
