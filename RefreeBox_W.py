from tkinter import * 
import socket   
from threading import *


"""
 Start Function
"""
def myClick():
    global i
    i+=1
    listR.insert(0,"ARIF RAMADHAN " + str(i))

def deleteR():
	listR.delete(0, END)
def deleteT():
	listT.delete(0, END)

def KickOffMagenta():
    global cs1
    global cs2

    try: cs1 and cs2
    except NameError: listT.insert(0, "Kick Magenta")

    else:
        cs1.sendall(bytes("Kick Off Magenta", "utf-8"))
        cs2.sendall(bytes("Kick Off Magenta", "utf-8"))
        listT.insert(0, "Kick Off Magenta")
         
def KickOffCyan():
    global cs1
    global cs2

    try: cs1 and cs2
    except NameError: listT.insert(0, "Kick Cyan")

    else:
        cs1.sendall(bytes("Kick Off Cyan", "utf-8"))
        cs2.sendall(bytes("Kick Off Cyan", "utf-8"))
        listT.insert(0, "Kick Off Cyan")


def CornerKickMagenta():
    global cs1
    global cs2

    try: cs1 and cs2
    except NameError: listT.insert(0, "Corner Magenta")

    else:
        cs1.sendall(bytes("Corner Kick Magenta", "utf-8"))
        cs2.sendall(bytes("Corner Kick Magenta", "utf-8"))
        listT.insert(0, "Corner Kick Magenta")

def CornerKickCyan():
    global cs1
    global cs2

    try: cs1 and cs2
    except NameError: listT.insert(0, "Corner Cyan")

    else:
        cs1.sendall(bytes("Corner Kick Cyan", "utf-8"))
        cs2.sendall(bytes("Corner Kick Cyan", "utf-8"))
 

def PrintReceiver(msg):
    print(msg)
    listR.insert(0, msg)


def PrintTransreceiver(msg):
    print(msg)
    listT.insert(0, msg)


def HandleClient(client, list_robot_clients):
    client_index = list_robot_clients.index(client)
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            PrintReceiver(f"{client.getpeername()}: {msg}")
        except Exception as exc:
            PrintTransreceiver(f"{list_robot_clients[client_index].getpeername()} disconnected.")
            list_robot_clients.pop(client_index)
            client.close()
            break


def ReceiveConnection(server_socket, list_robotnya):
    while True:
        client_socket, address1 = server_socket.accept()

        msg = client_socket.recv(1024) # Diterima dalam bentuk byte
        listR.insert(0, f"{address1}: {msg.decode('utf-8')}")
        print(f"{address1}: {msg.decode('utf-8')}")
        
        list_robotnya.append(client_socket)
        thread = Thread(target=HandleClient, args=(client_socket, list_robotnya))
        thread.start()
        
        # full_msg = ''
        # full_msg += msg.decode("utf-8") # Dirubah menjadi String
        # full_msg = full_msg.rstrip('\0')
        # full_msg = eval(full_msg)
        # client_socket.sendall(bytes("HAII from client_socket", "utf-8"))


def Receiv1():
    receive_thread = Thread(target=ReceiveConnection,
                            args=(s1, robot_cyan_clients))
    receive_thread.start()


def Receiv2():
    receive_thread = Thread(target=ReceiveConnection,
                            args=(s2, robot_magenta_clients))
    receive_thread.start()


def BroadcastSemua(msg):
    listT.insert(0, msg)
    for client in robot_cyan_clients:
        client.send(msg)
    for client in robot_magenta_clients:
        client.send(msg)


def KonekKeIP():
    # koneksi client ke host referee
    client_ip = Ip_input.get()
    client_port_str = port_input.get()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((client_ip, int(client_port_str))) 
    except Exception as exc:
        PrintTransreceiver("IP atau port salah.")
        print(exc)
        client.close()
        return
    
    PrintTransreceiver(f"Berusaha terkoneksi dengan {client_ip}...")
    client.send(host.encode('utf-8'))
    client.close()


def PingSemuaKoneksi():
    BroadcastSemua('PING'.encode('utf-8'))
        

robot_cyan_clients = []
robot_magenta_clients = []

host = socket.gethostname()
port1 = 1234
port2 = 2023

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s1.bind((host,port1))
s1.listen(5)
s2.bind((host,port2))
s2.listen(5)


root = Tk()
root.title("Refree Box Sneijder")
root.iconbitmap('poliban.ico')
root.geometry('1300x900')


"""
Bagian Lapangan,
- Ukuran Lapangan 600 x 400 | 120cm x 80cm
"""

lapanganImg = PhotoImage(file="wlyh.png")

lapangan = Canvas(root, width=700, height=500)
lapangan.place(x=5,y=0)
lapangan.create_image(0,0,anchor=NW,image=lapanganImg)


"""
Bagian Kanan Atas
- Title
"""
titleBGImg = PhotoImage(file="Frame1.png")

titleBG = Canvas(root, width=580,height=150,bg="#8C98FF")
titleBG.place(x=710,y=0)
# titleBG.create_image(0,0,anchor=NW,image=titleBGImg)

plbnImg = PhotoImage(file="logo.png")

plbn = Canvas(root, width=120,height=120)
plbn.place(x=725,y=17)
plbn.create_image(2,2,anchor=NW,image=plbnImg)

title1 = Label(root, bg="#8C98FF",text="KRSBI BERODA",fg="black",font=("Helvatica",30)).place(x=900, y=20)
title1 = Label(root, bg="#8C98FF",text="SNEIJDER TEAM",fg="black",font=("Helvatica",30)).place(x=890, y=75)


"""
Bagian Bawah Lapangan
- Port Communication | Information
"""
info = Canvas(root, width=700,height=395,bg="#B6B6B6")
info.place(x=5,y=500)

title1 = Label(root, bg="#B6B6B6",text="RECEIVER",fg="black",font=("Helvatica",20)).place(x=20, y=510)
title1 = Label(root, bg="#B6B6B6",text="TRANSCEIVER",fg="black",font=("Helvatica",20)).place(x=380, y=510)


# _____________________ RECEIVER ________________________
myFrameR = Frame(root)
scrollR = Scrollbar(myFrameR, orient=VERTICAL)
listR = Listbox(myFrameR,yscrollcommand=scrollR.set,width=40,height=15,selectmode=MULTIPLE)

scrollR.config(command=listR.yview)
scrollR.pack( side = RIGHT,fill = Y)
myFrameR.place(x= 20,y=550)
listR.pack()

btnR = Button(root, text="Clear Monitor", bd=4,padx=10,pady=5,font=(25),command= deleteR).place(x=20,y=820)

# _____________________ TRANSCEIVER ____________________
i = 0
myFrameT = Frame(root)
scrollT = Scrollbar(myFrameT, orient=VERTICAL)
listT = Listbox(myFrameT,yscrollcommand=scrollT.set,width=40,height=15,selectmode=EXTENDED)

scrollT.config(command=listT.yview)
scrollT.pack( side = RIGHT,fill = Y)
myFrameT.place(x= 380,y=550)
listT.pack()

btnT = Button(root, text="Clear Monitor", bd=4,padx=10,pady=5,font=(25),command= deleteT).place(x=380,y=820)


"""
Bagian Kanan bawah Title
- Koneksi Ke IP
"""
BG_ip = Canvas(root, width=580,height=150,bg="#F8A990")
BG_ip.place(x=710,y=149)

label1 = Label(root, bg="#F8A990",text="IP Address",fg="black",font=("Helvatica",15)).place(x=728, y=165)
Ip_input = Entry(root, width=25,font=(15),bd=4)
Ip_input.place(x=845, y=168)

label1 = Label(root, bg="#F8A990",text="Port IP",fg="black",font=("Helvatica",15)).place(x=730, y=215)
port_input = Entry(root, width=25,font=(15),bd=4)
port_input.place(x=845, y=215)

button_submit = Button(root, text= "Submit",bd=4,padx=20, command=KonekKeIP).place(x=730,y=260)

"""
Cyan Team
"""
wpp = Canvas(root, width=180,height=395,bg="cyan")
wpp.place(x=710,y=301)
Cyan = Label(root, bg="cyan",text="CYAN",fg="black",font=("arial",15,"bold")).place(x=770, y=315)

B_Kick_C = Button(root, text="Kick Off Kanan", bd=5,padx=9,font=("Helvatica",13,"bold"),height=0, command=KickOffCyan).place(x=724,y=360)
B_Corner_C = Button(root, text="Corner Kick Kanan", bd=5,padx=0,font=("Helvatica",13,"bold"),height=0, command=CornerKickCyan).place(x=718,y=405)


'''
B_Goal_C = Button(root, text="Goal", bd=5,padx=30,font=("Helvatica",13,"bold"),height=0).place(x=743,y=360)
B_Kick_C = Button(root, text="Kick Off", bd=5,padx=17,font=("Helvatica",13,"bold"),height=0).place(x=743,y=405)
B_Throw_C = Button(root, text="Throw In", bd=5,padx=14,font=("Helvatica",13,"bold"),height=0).place(x=743,y=450)
B_Corner_C = Button(root, text="Corner", bd=5,padx=21,font=("Helvatica",13,"bold"),height=0).place(x=743,y=495)
B_Free_C = Button(root, text="Free Kick", bd=5,padx=12,font=("Helvatica",13,"bold"),height=0).place(x=743,y=540)
B_Penalty_C = Button(root, text="Penalty", bd=5,padx=19,font=("Helvatica",13,"bold"),height=0).place(x=743,y=585)
B_Repair_C = Button(root, text="Repair", bd=5,padx=23,font=("Helvatica",13,"bold"),height=0).place(x=743,y=630)
'''

"""
Ref Command
"""
wpp = Canvas(root, width=219,height=395,bg="#FF9900")
wpp.place(x=891,y=301)

Ref_Command = Label(root, bg="#FF9900",text="Ref Command",fg="black",font=("arial",15,"bold")).place(x=933, y=315)


B_Start = Button(root, text="Start", bd=5,padx=20,font=("Helvatica",13,"bold"),height=0,bg="#A0FF9E").place(x=900,y=360)
B_Stop = Button(root, text="Stop", bd=5,padx=20,font=("Helvatica",13,"bold"),height=0,bg="#FF5454").place(x=1008,y=360)
B_TendangM = Button(root, text="Tes Penendang M", bd=5,padx=10,font=("Helvatica",13,"bold"),height=0,bg="#FFF854").place(x=912,y=420)
B_TendangC = Button(root, text="Tes Penendang C", bd=5,padx=10,font=("Helvatica",13,"bold"),height=0,bg="#FFF854").place(x=912,y=470)
B_Ping_Semua = Button(root, text="Ping semua", bd=5, padx=10, font=("Helvatica", 13, "bold"), height=0, bg="#FFF854", command=PingSemuaKoneksi).place(x=912, y=520)

"""
Magenta Team
"""
wpp = Canvas(root, width=180,height=395,bg="magenta")
wpp.place(x=1110,y=301)
Magenta = Label(root, bg="magenta",text="MAGENTA",fg="black",font=("arial",15,"bold")).place(x=1149, y=315)

B_Kick_M = Button(root, text="Kick Off Kiri", bd=5,padx=21,font=("Helvatica",13,"bold"),height=0,command=KickOffMagenta).place(x=1124,y=360)
B_Corner_M = Button(root, text="Corner Kick Kiri", bd=5,padx=5,font=("Helvatica",13,"bold"),height=0, command=CornerKickMagenta).place(x=1124,y=405)


'''
B_Goal_M = Button(root, text="Goal", bd=5,padx=30,font=("Helvatica",13,"bold"),height=0).place(x=1143,y=360)
B_Kick_M = Button(root, text="Kick Off", bd=5,padx=17,font=("Helvatica",13,"bold"),height=0).place(x=1143,y=405)
B_Throw_M = Button(root, text="Throw In", bd=5,padx=14,font=("Helvatica",13,"bold"),height=0).place(x=1143,y=450)
B_Corner_M = Button(root, text="Corner", bd=5,padx=21,font=("Helvatica",13,"bold"),height=0).place(x=1143,y=495)
B_Free_M = Button(root, text="Free Kick", bd=5,padx=12,font=("Helvatica",13,"bold"),height=0).place(x=1143,y=540)
B_Penalty_M = Button(root, text="Penalty", bd=5,padx=19,font=("Helvatica",13,"bold"),height=0).place(x=1143,y=585)
B_Repair_M = Button(root, text="Repair", bd=5,padx=23,font=("Helvatica",13,"bold"),height=0).place(x=1143,y=630)
'''

recvThread = Thread(target= Receiv1)
recvThread2 = Thread(target= Receiv2)

# recvThread.daemon = True
# recvThread2.daemon = True

recvThread.start()
recvThread2.start()

root.mainloop()