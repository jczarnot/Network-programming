
from time import sleep
from Device import *
import struct
from Socket import *
from threading import Thread
from DataConverter import *
from DeviceOperation import *

def create_conection(port=8000, ip_version=4, HOST='127.0.0.1'):
    s1 = Socket(ip_version=ip_version, HOST=HOST, port = port)
    s1.create_socket()
    s1.connect_to_server()
    return s1

def send_information_to_station(dat, s1):
    mess = pack_data(dat)
    send = True
    while send:
        s1.send(mess)
        send = recive_info_from_station(s1,dat)
    s1.close()

def recive_info_from_station(s1,send_data):
    try:
        messFromServer = s1.recvfrom(512)
        send = check_recv_data(send_data,messFromServer[0])
    except socket.timeout as msg:
        send = check_message_timestamp(send_data)
        if send:
            print("nie dostałem potwierdzenia wysyłam jeszcze raz dane")
    return send

def check_recv_data(send_data, recv_data, sending_time=10):
    id, mess_timestamp, server_timestamp = unpack_data_from_Server(recv_data)
    #sychronizacja czasu 
    if id == send_data[0] and mess_timestamp == send_data[1]:
        print("Wiadomość wysłana do serwera i potwierdzona")
        send = False
        return send
    else:
        send = check_message_timestamp(send_data, sending_time)
        if send:
            print("wiadomość potwierdzona nie moim id wysyłam dalej")
    return send

def check_message_timestamp(send_data, sending_time=10):
    ts = int(time.time())
    if send_data[1] + sending_time < ts:
        print("Zaczynam nadawać nową wiadomość chociaż stara nie dotarła do serwera")
        send = False
    else:
        send = True
    return send

def create_threads(func, data):
    threads = []
    port = 8000
    for dat in data:
        s1 = create_conection(port)
        threads.append(Thread(target=func, args=(dat,s1, )))
        # port += 1

    for t in threads:
        t.start()
    for t in threads:
        t.join()




