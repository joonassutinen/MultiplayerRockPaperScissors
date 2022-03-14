import socket
import time
import threading
import random
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65222  # The port used by the server
ThreadList = []



GameSessionObject = None
socketforgame = None
goalofplayer = None


class ClientsideSession():
    def __init__(self, role):
        self.sessionstatus = None
        self.socket = None
        self.latestmessage = None
        self.role = role
        self.localthreadlist = []
        y = threading.Thread(target=self.CreateASocket)
        y.start()

    def CreateASocket(self):
        self.sessionstatus = "CreatingSocket"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for i in range(10):
            try:
                s.connect((HOST, PORT))    
                self.sessionstatus = "SocketCreated"
                break
            except:
                print("Failed to create socket")
                pass
            time.sleep(0.5)
        if self.sessionstatus == "CreatingSocket":
            self.sessionstatus = "FailedSocketCreation"
        elif self.sessionstatus == "SocketCreated":
            self.socket= s

    def ReceiveAMessage(self):
        try:
            x = threading.Thread(target=self.ReceiveAMessageThread)
            self.localthreadlist.append(x)
            x.start()
        except:
            print("Failed to create message receiving thread")

    def ReceiveAMessageThread(self):
        data = self.socket.recv(1024)
        datastring = str(data, "utf8")
        self.latestmessage = datastring


def main():
    timeatstart = time.time()
    listofsessions = []
    listofclients = []
    listofcodes = []
    for i in range(100):
        GameSessionObject = ClientsideSession("Create")
        listofsessions.append(GameSessionObject)
    for i in listofsessions:
        i.socket.sendall(bytes(str(1), 'utf8') )
        try:
            data = i.socket.recv(1024)
            datastring = str(data, "utf8")
            listofcodes.append(datastring)
        except:
            print("Failed")
    for i in range(100):
        GameSessionObject = ClientsideSession("Join")
        listofclients.append(GameSessionObject)    
    for integer, i in enumerate(listofclients):
        try:
            i.socket.sendall(bytes(str(listofcodes[integer]), 'utf8'))
            print(socket)
        except:
            print("failedtosendid")
    for integer, i in enumerate(listofsessions):
        try:
            data = i.socket.recv(1024)
            datastring = str(data, "utf8")
        except:
            print("failedtogetaccept")
        if "Accepted" in datastring:
            try:
                i.socket.sendall(bytes(str("ok"), 'utf8'))
            except:
                print("failedtosendok")
    for integer, i in enumerate(listofclients):
        try:
            data = i.socket.recv(1024)
            datastring = str(data, "utf8")
        except:
            print("failedtogetaccept")
        if "Accepted" in datastring:
            try:
                i.socket.sendall(bytes(str("ok"), 'utf8'))
            except:
                print("failedtosendok")
    for integer, i in enumerate(listofsessions):
        try:
            data = i.socket.recv(1024)
            datastring = str(data, "utf8")
        except:
            print("failedtogettest")
        if "test" in datastring:
            try:
                i.socket.sendall(bytes(str("test"), 'utf8'))
            except:
                print("Failsd")
    for integer, i in enumerate(listofclients):
        try:
            data = i.socket.recv(1024)
            datastring = str(data, "utf8")
        except:
            print("failedtogettest")
        if "test" in datastring:
            try:
                i.socket.sendall(bytes(str("test"), 'utf8'))
            except:
                print("Failsd")
    for integer, i in enumerate(listofsessions):
        try:
            data = i.socket.recv(1024)
            datastring = str(data, "utf8")
        except:
            print("failedtogetstart")
        if datastring == "start":
            try:
                i.socket.sendall(bytes(str("rock"), 'utf8'))
            except:
                print("Failedtosendaction")
    for integer, i in enumerate(listofclients):
        try:
            data = i.socket.recv(1024)
            datastring = str(data, "utf8")
        except:
            print("failedtogetstart")
        if datastring == "start":
            try:
                i.socket.sendall(bytes(str("paper"), 'utf8'))
            except:
                print("Failedtosendaction")


    for integer, i in enumerate(listofsessions):
        try:
            data = i.socket.recv(1024)
            datastring = str(data, "utf8")
        except:
            print("failedtogetreceivedorfail")
        if datastring == "movereceived" or datstring == "timeout":
            try:
                i.socket.sendall(bytes(str("GiveResults"), 'utf8'))
            except:
                print("Failedtosendgiveresults")
    for integer, i in enumerate(listofclients):
        try:
            data = i.socket.recv(1024)
            datastring = str(data, "utf8")
        except:
            print("failedtogetreceivedorfail")
        if datastring == "movereceived" or datstring == "timeout":
            try:
                i.socket.sendall(bytes(str("GiveResults"), 'utf8'))
            except:
                print("Failedtosendgiveresults")

    for integer, i in enumerate(listofsessions):
        try:
            data = i.socket.recv(1024)
            datastring = str(data, "utf8")
        except:
            print("Failedtoreceivedata")
        print(datastring)
    for integer, i in enumerate(listofclients):
        try:
            data = i.socket.recv(1024)
            datastring = str(data, "utf8")
        except:
            print("Failedtoreceivedata")
        print(datastring)
    timeatend = time.time()
    print("100 sessions took", (timeatend -timeatstart))

main()