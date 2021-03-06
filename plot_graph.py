import matplotlib
# force matplotlib to not use any Xwindows backend.
# see https://stackoverflow.com/a/4706614/8225672 for why
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from datetime import datetime as dt
from csv_logger import read_csv_file

title = 'Temperatura'
date_label = 'Horário'
temp_label = 'Temperatura °C'
date_fmt = '%H:%M:%S'
image_name = '/var/www/html/images/history_graph.png'
resolution = [19.2, 10.8] # set the figure size to 1920x1080
temp_interval = 2

def plot_graph(plot_gaussian=False):
    rows = read_csv_file()
    timestamps = []
    dates = [] # x
    temps = [] # y

    for row in rows:
        timestamps.append(int(row[0]))
        temps.append(float(row[2]))

    for ts in timestamps:
        dates.append(dt.fromtimestamp(ts))

    print("plot_graph.py: creating plot")
    fig, ax = plt.subplots(1,1)
    ax.plot(dates,temps, linewidth=1.0, label="Binominal")

    # also plot gaussian (normal) distribution
    if plot_gaussian is True:
        temps_smooth = gaussian_filter1d(temps, sigma=30)
        ax.plot(dates, temps_smooth, color='red', alpha=0.8,
                linestyle='dashed', linewidth=1.0, label="Gaussian")

        # put a legend
        plt.legend(loc='best')

    # x (date) formatting
    xfmt = md.DateFormatter(date_fmt)
    ax.xaxis.set_major_formatter(xfmt)

    # manually set temp tick interval
    if abs(min(temps) - max(temps)) > 2:
        plt.yticks(np.arange(int(min(temps)), int(max(temps)), 1))

    # increase frequency of date tick interval
    loc = md.AutoDateLocator(minticks=20, maxticks=30, interval_multiples=True)
    ax.xaxis.set_major_locator(loc)

    # add a grid
    ax.grid()

    # set labels
    plt.xlabel(date_label)
    plt.ylabel(temp_label)
    plt.title(f'Última medida: {rows[-1][1]}')

    # set how the plot labels are displayed
    plt.subplots_adjust(bottom=0.2)
    plt.xticks(rotation=50)

    fig.set_size_inches(resolution[0], resolution[1])
    try:
        plt.savefig(image_name, bbox_inches='tight')
    except:
        print("plot_graph.py: could't save file. check if directory exists/permissions")
        exit(2)


    # close figures
    # without this the program will run out of memory in a few hours
    plt.close('all')


if __name__ == "__main__": # if calling directly show graph
    from os import system
    import time
    start = time.time()
    plot_graph(True)
    end = time.time()
    print(f'drew graph in {end - start} seconds')
    system(f"which pqiv && pqiv {image_name}")
