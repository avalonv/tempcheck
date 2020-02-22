#!/usr/bin/python3

import time
import locale
import threading
from sys import argv
from read_temp_ds18b20 import read_temp
from csv_logger import write_csv
from plot_graph import plot_graph

locale_str = 'pt_BR.utf8'
last_warn = time.time()
last_update = last_warn
refresh_time = 3
history_limit = (None, 720)  # no limit on entries, max 12 hours of history
high_temps = []
warn_threshold = 60  # send a warning if the temperature stays high for a minute

try:
    max_temp = int(argv[1])
except IndexError:
    print("main.py: temperature argument missing.")
    exit(1)
except ValueError:
    print(f"main.py: '{argv[1]}': invalid number.")
    exit(1)

try:
    locale.setlocale(locale.LC_ALL, locale_str)
except (locale.Error):
    print("main.py: unsupported locale")
    print(f"run `sudo dpkg-reconfigure locales` to configure {locale_str} locale")
    exit(1)


def send_email(temp):
    current_date = time.strftime('%c')
    body = f"\'{temp} is above {max_temp}\n{current_date}\'"
    subject = "Alerta de temperatura"
    recipient = "test@example.com"
    print(body)


def update_graph(update_interval=60):
    global last_update
    update_graph_thread = threading.Thread(target=plot_graph)
    if (last_update + update_interval) < time.time():
        if not update_graph_thread.isAlive():
            update_graph_thread.start()
            last_update = time.time()


def warn(warn_interval=600):
    global last_warn
    warn_thread = threading.Thread(target=send_email, args=temp)
    if (last_warn + warn_interval) < time.time():
        if not warn_thread.isAlive():
            warn_thread.start()
            last_warn = time.time()


if __name__ == "__main__":
    while True:
        temp = read_temp()
        date_str = time.strftime("%Y-%m-%d %H:%M:%S").strip(' ')
        write_csv(int(time.time()), date_str, temp, history_limit[0], history_limit[1])
        update_graph()
        if temp > max_temp:
            high_temps.append(time.time())
            # check if the temperature has remained above the max_temp limit
            # for longer than a certain amount of time
            if high_temps[-1] - high_temps[0] > warn_threshold:
                warn()
                # reset high temps
                high_temps = []
        time.sleep(refresh_time)
