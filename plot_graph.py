import matplotlib.pyplot as plt
import matplotlib.dates as md
from datetime import datetime as dt
import csv

timestamps = []  # x
temps = [] # y


def read_history():
    global timestamps, temps
    with open('history.csv', 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        next(rows, None)  # skip header
        for row in rows:
            try:
                timestamps.append(int(row[0]))
                temps.append(float(row[2]))
            except (IndexError):
                break


def draw_plot():
    read_history()

    dates = []
    for ts in timestamps:
        dates.append(dt.fromtimestamp(ts))

    ax = plt.gca()  # get current axes instance
    xfmt = md.DateFormatter('%H:%M:%S')  # x (timestamps) formatting
    ax.xaxis.set_major_formatter(xfmt)
    ax.grid() # add a grid

    # set how the plot values are displayed
    plt.subplots_adjust(bottom=0.2)
    plt.xticks(rotation=25)

    # set labels
    plt.xlabel('Horário')
    plt.ylabel('Temperatura °C')
    # plt.title('temperatura')

    plt.plot(dates,temps)  # create plot

    plt.savefig("test.png")
    plt.show()

draw_plot()
