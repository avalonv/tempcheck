#!/usr/bin/python3
# modified from: http://kookye.com/2017/06/01/desgin-a-temperature-detector-through-raspberry-pi-and-ds18b20-temperature-sensor/

from os import system
from log_csv import write_rows
import glob
import time
import locale

# to configure pt_BR locale run 'sudo dpkg-reconfigure locales'
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
system('modprobe w1-gpio')
system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]  # wildcard match
device_file = device_folder + '/w1_slave'

max_temp = 10
last_warn = 0
cooldown = 6000
refresh_time = 2


def send_email(temp):
    current_date = time.strftime('%c')
    msg_body = f"\'{temp} is above {max_temp}\n{current_date}\'"
    msg_subject = "Alerta de temperatura"
    msg_recipient = "avalonvales@protonmail.com"
    # system(f"echo {body} | s-nail -s '{subject}' '{recipient}'")


def log_temperature(temp):
    global last_warn
    time_now = int(time.time())  # unix timestamp
    time_str = time.strftime("%r")  # human readable time
    write_rows(time_now, time_str, temp, 1000)
    if (last_warn + cooldown) < time_now:
        send_email(temp)
        last_warn = time_now


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    # [-3:] = slice starts at the last 3 chracters until the end
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:  # if equals_pos is not the last character
        temp_string = lines[1][equals_pos+2:]  # everything after 't='
        temp_c = float(temp_string) / 1000.0
        return temp_c


while True:
    current_temp = read_temp()
    # print('C = %3.3f' % current_temp)
    if current_temp > max_temp:
        log_temperature(current_temp)
    time.sleep(refresh_time)
