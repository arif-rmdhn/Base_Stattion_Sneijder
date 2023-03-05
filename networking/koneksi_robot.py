import socket

#  buat server dulu agar bisa di konek ke refree box
HOST_IP = ''

#IP = 'localhost'  # Gunakan ini jika ingin mentes di mesin lokal
IP = socket.gethostname()
PORT = 1234  # portnya tergantung dari refree boxnya, kalau bisa nanti nanti pastikan mau make port apa

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))

server.listen(1)

while True:
    host_socket, address = server.accept()
    HOST_IP = host_socket.recv(1024).decode('utf-8')
    print(f"Connected to {HOST_IP}")
    host_socket.close()
    break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST_IP, PORT))

client.send(f"Terkoneksi dengan robot".encode('utf-8'))