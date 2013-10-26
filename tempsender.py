import os
import glob
import time
from nimbits import Nimbits, NimbitsError
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
    
while True:
    temperature = read_temp()[0]
    nimbits_client = Nimbits('a.stagi@atooma.com', 'andrea22!!')
    entity = "SampleValue"
    millis = int(round(time.time() * 1000))
    print nimbits_client.set_value(entity, d=temperature, t=millis) 
    time.sleep(10)