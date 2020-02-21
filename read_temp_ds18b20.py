# modified from: http://kookye.com/2017/06/01/desgin-a-temperature-detector-through-raspberry-pi-and-ds18b20-temperature-sensor/

from os import system
from re import search
import glob
import time

last_temp = 0

try:
    system('modprobe w1-gpio')
    system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]  # wildcard match
    device_file = device_folder + '/w1_slave'
except:
    print("read_temp_ds18b20.py: couldn't locate device to read from")
    exit(2)


def read_temp_raw():
    with open(device_file, 'r') as f:
        lines = f.readlines()
        return lines


def read_temp():
    global last_temp
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
        # when the sensor is reconnected, it seems to always report 85.0 C
        # this is a false reading and should be dropped
        if temp_c != 85.0 or None:
            last_temp = temp_c
            return temp_c
        return last_temp


if __name__ == "__main__": # if calling directly print temperature
    while True:
        print('C = %3.3f' % read_temp())
        time.sleep(2)
