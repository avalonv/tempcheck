# modified from: http://kookye.com/2017/06/01/desgin-a-temperature-detector-through-raspberry-pi-and-ds18b20-temperature-sensor/

from os import system
import glob
import time

try:
    system('modprobe w1-gpio')
    system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]  # wildcard match
    device_file = device_folder + '/w1_slave'
except (IndexError):
    print("Couldn't locate device to read from")
    exit(1)


def read_temp_raw():
    with open(device_file, 'r') as f:
        lines = f.readlines()
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


if __name__ == "__main__": # if calling directly print temperature
    while True:
        print('C = %3.3f' % read_temp())
        time.sleep(2)
