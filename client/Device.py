import time
import random


class Device:
    
    id = 0
    def __init__(self):
        self.__id = Device.id
        Device.id += 1

    def get_id(self):
        return self.__id
    
    def get_time(self):
        ts = time.time()
        return ts
    
    def generate_temperature(self, lowest_value=-10, highest_value=40):
        self._temp = random.uniform(lowest_value, highest_value)
        return self._temp

    def generate_pressure(self,lowest_value=970, highest_value=1050):
        self._pressure = random.uniform(lowest_value, highest_value)
        return self._pressure

    def generate_humidity(self,lowest_value=0, highest_value=100):
        self._humidity = random.uniform(lowest_value, highest_value)
        return self._humidity
    

    
