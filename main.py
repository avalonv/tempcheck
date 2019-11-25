#!/usr/bin/python3

import threading
from os import system
from read_temperature import read_temp
from csv_logger import write_csv
from plot_graph import plot_graph
from write_html import write_html
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
    # defining a function that calls both is better than creating
    # two threads since write_html() depends on plot_graph()'s output
    def _call_plot_and_html():
        plot_graph()
        write_html()
    update_graph_thread = threading.Thread(target=_call_plot_and_html)
    if (last_update + update_interval) < time.time():
        if not update_graph_thread.isAlive():
            update_graph_thread.start()
            last_update = time.time()


def warn(warn_interval=600):
    global last_warn
    email_thread = threading.Thread(target=send_email, args=temp)
    if (last_warn + warn_interval) < time.time():
        if not email_thread.isAlive():
            email_thread.start()
            last_warn = time.time()


while True:
    temp = read_temp()
    date_str = time.strftime("%Y-%m-%d %H:%M:%S").strip(' ')
    write_csv(int(time.time()), date_str, temp, history_limit)
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
