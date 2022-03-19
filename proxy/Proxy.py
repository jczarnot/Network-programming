from Socket import *
from DataConverter import *
import requests
import time
import json
import os
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
import threading
import ConfigReader


class Proxy:

    def __init__(self, sockets, path_to_config_file):
        self.sockets = sockets

        self.server_url = None
        self.cached_data = {'measurements': []}
        self.max_cached = 0
        self.proper_measurements_values = None
        self.cached_data_file_names = []
        self.data_handling_lock = threading.Lock()
        self.proper_ips = None
        self.device_ids = None
        
        ConfigReader.load_configuration(path_to_config_file, self)
    
    def receive_from_client(self):
        self.read_udp = []
        self.write_udp = []
        self.error_udp = []
        for sock in self.sockets:
            self.socket = sock
            self.socket.create_socket()
            self.socket.bind()
            self.read_udp.append(self.socket.s)
            self.write_udp.append(self.socket.s)
            self.error_udp.append(self.socket.s)
    
    def remove_socket_from_list(self,socket):
        if socket in self.sockets:
            self.sockets.remove(socket)
            self.read_udp.remove(socket.s)
            self.write_udp.remove(socket.s)
            self.error_udp.remove(socket.s)
    
    def add_new_socket_to_list(self,socket):
            self.socket = socket
            self.socket.create_socket()
            self.socket.bind()
            self.read_udp.append(self.socket.s)
            self.write_udp.append(self.socket.s)
            self.error_udp.append(self.socket.s)


    def send_to_server(self, data: dict):
        try:
            r = requests.post(url = self.server_url, json = data, verify=False, auth=HTTPBasicAuth('server', 'pass'))
            if r.status_code == 401:
                print("Wrong login or password, can't authorize to server")

            pastebin_url = r.text
            return pastebin_url
        except HTTPError as http_err:
            return -1
        except ConnectionError as conn_err:
            return -1
        except requests.exceptions.RequestException as e:
            return -1

    def _clear_cache(self):
        self.cached_data = {'measurements': []}

        
    def cache_data(self, data: dict):
        for device in data['measurements']:
            self.cached_data['measurements'].append(device)

            #if we try to overload cache, we save already cached data to file, and clear cached data dict
            if len(self.cached_data['measurements']) >= self.max_cached: 
                file_name = f"{int(time.time())}.json"
                with open(file_name, 'w') as file:
                    json.dump(self.cached_data, file)
                self.cached_data_file_names.append(file_name)
                self._clear_cache()

        return self.cached_data_file_names
    def remove_socket_from_list(self,socket):
        if socket in self.sockets:
            self.sockets.remove(socket)
            self.read_udp.remove(socket.s)
            self.write_udp.remove(socket.s)
            self.error_udp.remove(socket.s)
    
    def add_new_socket_to_list(self,socket):
            self.socket = socket
            self.socket.create_socket()
            self.socket.bind()
            self.read_udp.append(self.socket.s)
            self.write_udp.append(self.socket.s)
            self.error_udp.append(self.socket.s)


    def _send_data_from_files(self):
        for file_name in self.cached_data_file_names:
            with open(file_name, 'r') as file:
                data = json.load(file)
                res = self.send_to_server(data)
            if res != -1:
                os.remove(file_name) 
                self.cached_data_file_names.remove(file_name)

    def _send_cached_data(self):
        res = self.send_to_server(self.cached_data)
        if res != -1:
            self._clear_cache()

    def send_data_after_restored_connection(self):
        self._send_data_from_files()
        self._send_cached_data()

    
    def start_select(self, BUFSIZE = 512, write_udp = [], err_udp = []):
        Work = True
        print('start_select')
        config_time = time.time()
        prev_message = {}
        for id in self.device_ids:
            prev_message[id] = None
        while Work:
            if time.time() > config_time + 10:
                ConfigReader.load_configuration('config.json', self)
                config_time = time.time()
            rec_data = {'measurements': []}
            try:
                ready_read, ready_write, ready_except = select.select( self.read_udp, self.write_udp,  self.error_udp)
            except select.error or socket.error as e:
                print(e)
                break
            for s in ready_read:
                for sock in self.sockets:
                    if s == sock.s:
                        break  
                messFromClient = sock.recvfrom( BUFSIZE) 
                address = messFromClient[1] 
                if address[0] in self.proper_ips:
                    ts = int(time.time())
                    id, timestamp, temp, press, hum = unpack_weather_data(messFromClient[0])
                    peckedId = pack_data_from_server(id,timestamp, ts)
                    sock.sendto(peckedId,address)
                    
                    data = {'device_id' : id, 'time' : timestamp, 'temperature' : temp, 'pressure' : press, 'humidity' : hum}
                    self.add_logs(data)
                    if timestamp != prev_message[id]:
                        prev_message[id] = timestamp
                        rec_data['measurements'].append(data)

            for s in ready_write:
                pass
            for s in ready_except:
                print('socket {s} had error!')

            if len (rec_data['measurements']) > 0:
                rec_thread = threading.Thread(target = self.received_data_handling, args=(rec_data,))
                rec_thread.start()
    
    def delete_innapriopriate_data(self, rec_data: dict):
        to_send = {'measurements': []}
        for data in rec_data['measurements']:
            proper = self.check_if_data_from_device_have_proper_values(data)
            if not proper:
                print(data, 'has invalid values, and wont be send to server')
            else:
                to_send['measurements'].append(data)
            
        return to_send

    def received_data_handling(self, rec_data: dict):
        with self.data_handling_lock:
            to_send = self.delete_innapriopriate_data(rec_data)
            try:
                if len(self.cached_data_file_names) > 0:
                    self._send_data_from_files()
                if len(self.cached_data['measurements']) > 0:
                    self._send_cached_data()
                if len(to_send['measurements']) > 0:
                    res = self.send_to_server(to_send)
                    if res == -1:
                        raise Exception
            except:
                self.cache_data(to_send)
            print('cached data', len(self.cached_data['measurements']), 'files', len(self.cached_data_file_names))



    def add_logs(self, rec_data):
        with open('proxy_logs.json', 'a') as file:
                    act_time = time.time()
                    logs = {act_time: rec_data}
                    json.dump(logs, file)
                    file.write("\n")

    def _check_if_single_measurement_have_proper_value(self, type: str, value):
        if value < self.proper_measurements_values[type]['min'] or value > self.proper_measurements_values[type]['max']:
            print('Measurement:', type, 'has inappropriate value:', value)
            return 0
        if type == 'time': #check if we didint receive data from future
            if value > time.time():
                return 0
        return 1

    def check_if_data_have_proper_values(self, data: dict):
        for device in data['measurements']:
            for type, value in device.items():
                if not self._check_if_single_measurement_have_proper_value(type, value):
                    return 0
        return 1

    def check_if_data_from_device_have_proper_values(self, data: dict):
        for type, value in data.items():
                if not self._check_if_single_measurement_have_proper_value(type, value):
                    return 0
        return 1


    
def create_sockets(num=1,ip_version=4,HOST='127.0.0.1',port=8000):
    socks =[]
    for i in range(num):
        sock = Socket(ip_version=ip_version, HOST=HOST, port = port)
        socks.append(sock)
        port += 1
    return socks



if __name__ == "__main__":
    n_devices = int(input("input number of devices: "))
    config_file = "config.json"

    socks = create_sockets(n_devices)
    proxy = Proxy(socks, config_file)
    proxy.receive_from_client()
    proxy.start_select()



