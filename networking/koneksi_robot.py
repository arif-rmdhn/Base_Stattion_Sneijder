import socket
from client import Client

host_ip = socket.gethostname()  # nanti ganti agar bisa dapat ip host dari hostnya sendir
port = 1234

client = Client(host_ip, port)
client.mulai_koneksi()