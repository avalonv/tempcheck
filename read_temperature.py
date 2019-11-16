# modified from: http://kookye.com/2017/06/01/desgin-a-temperature-detector-through-raspberry-pi-and-ds18b20-temperature-sensor/

from os import system
from re import search
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
    while True:
        # check 'YES' is at the end of line 1
        if search('YES', lines[0]) is not None:
            # check crc. if all the bytes are 00 the device is not connected
            if search('(00 ){9}', lines[0]) is None:
                break

        time.sleep(0.2)
        lines = read_temp_raw()

    # this pattern matches only the number after t= in
    # the second line, with or without the negative sign
    temp_string = search('(?<=t=)(-){0,1}\d+', lines[1])
    if temp_string:
        temp_c = float(temp_string.group(0)) / 1000.0
        return temp_c


if __name__ == "__main__": # if calling directly print temperature
    while True:
        print('C = %3.3f' % read_temp())
        time.sleep(2)
