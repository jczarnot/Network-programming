from Device import *

def generate_devices(num):
    devices = []
    for i in range(0,num):
        d = Device()
        devices.append(d)
    return devices

def read_data_from_device(device):

    id = device.get_id()
    timestamp = int(device.get_time())
    temp = device.generate_temperature()
    pressure = device.generate_pressure()
    humidity = device.generate_humidity()
    return (id, timestamp, temp, pressure, humidity)

def read_info_from_stations(devices):
    data = []
    messages = []
    for device in devices: 
        data.append(read_data_from_device(device))
    return data





