import matplotlib.pyplot as plt
import matplotlib.dates as md
from datetime import datetime as dt
from log_csv import read_rows

def draw_plot():
    rows = read_rows()
    timestamps = []
    dates = [] # x
    temps = [] # y

    for row in rows:
        timestamps.append(int(row[0]))
        temps.append(float(row[2]))

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
    # plt.title('temperatura nas últimas três horas')

    plt.plot(dates,temps)  # create plot

    plt.savefig("test.png")
    plt.show()

if __name__ == "__main__":
    draw_plot()
