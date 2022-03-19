import struct
from unittest import result

def unpack_weather_data(bytes):
    result = struct.unpack('!i i f f f', bytes)
    return result

def pack_id_timestamp(id,timestamp):
    return struct.pack("!i i", id, timestamp)

def unpack_id_timestamp(bytes):
    result = struct.unpack('!i i', bytes)
    return result

def pack_data(data):
    id = data[0]
    timestamp = data[1]
    temperature = data[2]
    pressure = data[3]
    humidity = data[4]
    return struct.pack("!i i f f f", id, timestamp, temperature, pressure, humidity)

def unpack_data_from_Server(bytes):
    result = struct.unpack('!i i i', bytes)
    return result

def pack_data_from_server(id, timestamp, server_time):
    result = struct.pack('!i i i', id, timestamp, server_time)
    return result

def pack_data_for_client(id,client_timestamp, server_timestamp):
    return struct.pack("!i i i", id, client_timestamp, server_timestamp)

