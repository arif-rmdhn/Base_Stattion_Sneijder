import socket

class Client:

    def __init__(self, host_ip="", port=0):
        self.host_ip = host_ip
        self.port = port
    
    def mulai_koneksi(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host_ip, self.port))  # cari cara biar dapat host ip
        client.send(f"{socket.gethostname()} terkoneksi".encode('utf-8'))