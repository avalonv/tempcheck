#!/usr/bin/python3

from os import system
from read_temperature import read_temp
from log_csv import write_csv
import time
import locale

max_temp = 40
last_warn = 0
warn_interval = 600 # 10 minutes
refresh_time = 3
locale_str = 'pt_BR.utf8'
history_limit = 3600 # * 3 = keep around 3 hours of history

try:
    locale.setlocale(locale.LC_ALL, locale_str)
except (locale.Error):
    print('unsupported locale')
    print(f"run 'sudo dpkg-reconfigure locales' to configure {locale_str} locale")
    exit(1)


def send_email(temp):
    current_date = time.strftime('%c')
    body = f"\'{temp} is above {max_temp}\n{current_date}\'"
    subject = "Alerta de temperatura"
    recipient = "avalonvales@protonmail.com"
    print(body)
    # system(f"echo {body} | s-nail -s '{subject}' '{recipient}'")


def log_temperature(temp):
    global last_warn
    time_now = int(time.time())  # unix timestamp
    date_str = time.strftime("%Y-%m-%d %H:%M:%S").strip(' ')  # human readable date
    write_csv(time_now, date_str, temp, history_limit)
    if current_temp > max_temp:
        if (last_warn + warn_interval) < time_now:
            send_email(temp)
            last_warn = time_now


while True:
    current_temp = read_temp()
    log_temperature(current_temp)
    time.sleep(refresh_time)
