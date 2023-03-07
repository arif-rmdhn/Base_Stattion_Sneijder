import socket


def ReceiveCommand(msg):
    if msg == 'PING':
        Ping(client)
    else:
        print(f"\"{msg}\" Message tidak dimengerti")
        client.send("Message tidak dimengerti".encode('utf-8'))

def Ping(sc):
    print("PING!")
    sc.send(f"PING!".encode('utf-8'))


HOST_IP = ''

# IP = 'localhost'  # Gunakan ini jika ingin mentes di mesin lokal
IP = socket.gethostname()  # gunakan ini jika ini ada di mesin lain
PORT = 1234  # portnya tergantung dari refree boxnya, kalau bisa nanti nanti pastikan mau make port apa

#  buat server dulu agar bisa di konek ke refree box
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))

print("Menunggu koneksi...")
server.listen(1)

# loop server
while True:
    host_socket, address = server.accept()
    HOST_IP = host_socket.recv(1024).decode('utf-8')
    print(f"Connected to {HOST_IP}")
    host_socket.close()
    break

# baru buat koneksi client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST_IP, PORT))

client.send(f"Terkoneksi dengan {IP}".encode('utf-8'))

# loop client
while True:
    try:
        msg = client.recv(1024).decode('utf-8')
        ReceiveCommand(msg)
    except Exception as exc:
        print(f"ERROR: Program di stop tiba-tiba\nexception: {exc}")
        client.close()
        break


client.close()
print("Koneksi berakhir...")