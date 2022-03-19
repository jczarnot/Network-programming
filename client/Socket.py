import socket
import select


class Socket:

    def __init__(self,ip_version=4,HOST=None,port=None):
        self.ip_version = ip_version
        self.family = self.set_family()
        if HOST == None:
            self.HOST = self.set_host_addr()
        else:
            self.HOST = HOST
        if port == None:
            self.port = self.set_port()
        else:
            self.port = port
        
    def set_host_addr(self):
        if self.ip_version == 6:
            self.HOST = "::1"
        else:
            self.HOST = "127.0.0.1"
        return self.HOST

    def set_port(self):
        if self.ip_version == 6:
            self.port = 8001
        else:
            self.port = 8000
        return self.port

    def set_family(self):
        if self.ip_version == 6:
            self.family = socket.AF_INET6
        else:
            self.family = socket.AF_INET
        return self.family
        
    def create_socket(self):
        self.s = socket.socket(self.family, socket.SOCK_DGRAM)


    def set_timeout(self, time):
        self.s.settimeout(time)

    def connect_to_server(self):
        try:
            self.s.connect((self.HOST,self.port))
        except socket.timeout as msg:
            print("Caught exception socket.timeout : %s" % msg)
            self.s.close()

    def send(self,data):
        num_sent = 0
        while num_sent < len(data):
            current_sent = self.s.send(data[num_sent:])
            if current_sent == 0:
                raise RuntimeError("Couldn't send data")
            num_sent += current_sent
        return num_sent

    def sendto(self,data,address):
        num_sent = 0
        while num_sent < len(data):
            current_sent = self.s.sendto(data[num_sent:],address)
            if current_sent == 0:
                raise RuntimeError("Couldn't send data")
            num_sent += current_sent
        return num_sent


    def recvfrom(self,buf_size):
        return self.s.recvfrom(buf_size)

    def close(self):
        self.s.close()

    def bind(self):
        self.s.bind((self.HOST,self.port))
    
    


