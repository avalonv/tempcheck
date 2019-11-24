#!/usr/bin/python3

import threading
from os import system
from read_temperature import read_temp
from csv_logger import write_csv
from plot_graph import draw_line_graph
from write_html import update_webpage
import time
import locale

locale_str = 'pt_BR.utf8'
max_temp = 25
last_warn = 0
last_update = 0
refresh_time = 3
history_limit = 3600 # * 3 = keep around 3 hours of history
high_temps = []
warn_threshold = 60 # send a warning if the temperature stays high for a minute


try:
    locale.setlocale(locale.LC_ALL, locale_str)
except (locale.Error):
    print('unsupported locale')
    print(f"run `sudo dpkg-reconfigure locales` to configure {locale_str} locale")
    exit(1)


def send_email(temp):
    current_date = time.strftime('%c')
    body = f"\'{temp} is above {max_temp}\n{current_date}\'"
    subject = "Alerta de temperatura"
    recipient = "avalonvales@protonmail.com"
    print(body)
    # system(f"echo {body} | s-nail -s '{subject}' '{recipient}'")


def update_graph(update_interval=300):
    global last_update
    graph_thread = threading.Thread(target=draw_line_graph)
    if (last_update + update_interval) < time_now:
        if not graph_thread.isAlive():
            graph_thread.start()
            last_update = time_now
    update_webpage()


while True:
    temp = read_temp()
    time_now = int(time.time())
    date_str = time.strftime("%Y-%m-%d %H:%M:%S").strip(' ')
    write_csv(time_now, date_str, temp, history_limit)
    update_graph()
    if temp > max_temp:
        high_temps.append(time_now)
        # check if the temperature has remained above the max_temp limit
        # for longer than a certain amount of time
        if high_temps[-1] - high_temps[0] > warn_threshold:
            # check if a warning was already sent recently
            if (last_warn + warn_interval) < time_now:
                draw_line_graph()
                send_email(temp)
                last_warn = time_now
            # reset high temps
            high_temps = []
    time.sleep(refresh_time)
