from Clients import *
import time


def main(devices):
    data = read_info_from_stations(devices)
    create_threads(send_information_to_station, data)


work = True
n_devices = int(input("input number of devices: "))
devices = generate_devices(n_devices)
while work:
    main(devices)
    time.sleep(10)
