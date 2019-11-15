import matplotlib.pyplot as plt
import matplotlib.dates as md
from datetime import datetime as dt
from log_csv import read_rows


def draw_line_graph(show_fig=False):
    rows = read_rows()
    timestamps = []
    dates = [] # x
    temps = [] # y

    for row in rows:
        timestamps.append(int(row[0]))
        temps.append(float(row[2]))

    for ts in timestamps:
        dates.append(dt.fromtimestamp(ts))

    fig, ax = plt.subplots(1,1)
    ax.plot(dates,temps)

    # x (date) formatting
    xfmt = md.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)

    # add a grid
    ax.grid()

    # set labels
    plt.xlabel('Horário')
    plt.ylabel('Temperatura °C')
    # plt.title('temperatura nas últimas três horas')

    # set how the plot labels are displayed
    plt.subplots_adjust(bottom=0.2)
    plt.xticks(rotation=50)

    plt.savefig("test.png")

    if show_fig is True:
        plt.show()


if __name__ == "__main__": # if calling directly show graph
    draw_line_graph(True)
