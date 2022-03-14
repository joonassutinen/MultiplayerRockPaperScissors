import socket
from random import randint
import threading
import time

HOST = "127.0.0.1" 
PORT = 65222
Sessionlist = []
Threadlist = []
AddressList = []

class Session:
    def __init__(self, sessionid, participant, address, threadnumber):
        self.id = sessionid
        self.state = 1
        self.participants = [participant, None]
        self.addresses = [address, None]
        self.threadnumber = threadnumber
        self.statestring = "1PlayerJoined"


def SessionResults(data1, data2):
    if data1 == "scissors" and data2 == "rock":
        return("2,1,3")
    elif data1 == "scissors" and data2 == "paper":
        return("1,1,2")
    elif data1 == "scissors" and data2 == "scissors":
        return("0,1,1")
    elif data1 == "paper" and data2 == "rock":
        return("1,2,3")
    elif data1 == "paper" and data2 == "paper":
        return("0,2,2")
    elif data1 == "paper" and data2 == "scissors":
        return("2,2,1")
    elif data1 == "rock" and data2 == "rock":
        return("0,3,3")
    elif data1 == "rock" and data2 == "paper":
        return("2,3,2")
    elif data1 == "rock" and data2 == "scissors":
        return("1,3,1")


def RockPaperScissors(session):
    while session.state == 1:
        count = 0
        while session.participants[1] == None:
            time.sleep(1)
            count += 1
            if count == 30:
                break
        okcount = 0
        if session.participants[1] != None:
            for i in session.participants:
                i.sendall(bytes("Accepted", "utf8"))
                try:
                    data = i.recv(1024)
                    datastring = str(data, "utf8")
                    if datastring == "ok":
                        okcount += 1
                except:
                    session.statestring = "FailedOk"
            if okcount == 2:
                session.statestring = "BothOk"
                differences = []
                for i in session.participants:
                    currenttime = time.time()
                    receivetime = time.time()
                    i.sendall(bytes("test", "utf8"))   
                    data = i.recv(1024)
                    datastring = str(data, "utf8")
                    if datastring == "test":
                        receivetime = time.time()
                    difference = receivetime - currenttime
                    differences.append(difference)
                for i in session.participants:   
                    i.sendall(bytes("start", "utf8"))  
                possibilities = ["scissors", "paper", "rock"]
                if differences[0] >= differences[1]:
                    try:
                        session.participants[1].settimeout(15)
                        data2 = session.participants[1].recv(1024)
                        session.participants[1].sendall(bytes("movereceived", "utf8")) 
                    except socket.timeout:
                        data2 = bytes(possibilities[randint(0,2)], "utf8")
                        session.participants[1].sendall(bytes("timeout", "utf8")) 
                    try:
                        session.participants[0].settimeout(15 + differences[0] - differences[1])
                        data1 = session.participants[0].recv(1024)
                        session.participants[0].sendall(bytes("movereceived", "utf8")) 
                    except socket.timeout:
                        data1 = bytes(possibilities[randint(0,2)], "utf8")
                        session.participants[0].sendall(bytes("timeout", "utf8")) 
                elif differences[0] < differences[1]:
                    try:
                        session.participants[0].settimeout(15)
                        data1 = session.participants[0].recv(1024)
                        session.participants[0].sendall(bytes("movereceived", "utf8")) 
                    except socket.timeout:
                        data1 = bytes(possibilities[randint(0,2)], "utf8")
                        session.participants[0].sendall(bytes("timeout", "utf8")) 
                    try:
                        session.participants[1].settimeout(15 + differences[1] - differences[0])
                        data2 = session.participants[1].recv(1024)
                        session.participants[1].sendall(bytes("movereceived", "utf8")) 
                    except socket.timeout:
                        data2 = bytes(possibilities[randint(0,2)], "utf8")
                        session.participants[1].sendall(bytes("timeout", "utf8")) 
                resultscount = 0
                data1 = str(data1, "utf8")
                data2 = str(data2, "utf8")
                results = SessionResults(data1, data2)
                for i in session.participants:
                    try:
                        data = i.recv(1024)
                        datastring = str(data, "utf8")
                        if datastring == "GiveResults":
                            i.sendall(bytes(results, "utf8")) 
                    except:
                        pass
                session.state = 0
            else:
                session.state = 0
        else:
            try:
                session.participants[0].sendall(bytes("2ndPlayerMissing", "utf8")) 
            except:
                pass
        session.state = 0
    for index, i in enumerate(Sessionlist):
        try:
            if i == session:
                Sessionlist.pop(index)
        except:
            print("Failed to remove session")

def WaitForCorrect(socket):
    NotJoined = True
    global Sessionlist
    while NotJoined:
        try:
            data = socket.recv(1024)
            datastring = str(data, "utf8")
            codeinlist = False
            for i in Sessionlist:
                if i.id == int(datastring):
                    codeinlist = True
                    if i.participants[1] == None and i.addresses[1] == None:
                        i.participants[1] = socket
                        i.addresses[1] = addr
                        NotJoined = False
                    else:
                        socket.sendall(bytes("Session already full", "utf8"))
            if codeinlist == False:
                try:
                    socket.sendall(bytes("SessionNotExist", "utf8"))
                except:
                    print("fail")
        except:
            print("Closed")
            NotJoined = False
        time.sleep(1)



def JoinOrCreate(socket):
    global Sessionlist
    global Threadlist
    KeepTrying = True
    try:
        while KeepTrying:
            data = socket.recv(1024)
            datastring = str(data, "utf8")

            if int(datastring) == 1:
                TListLength = len(Threadlist)
                randomid = randint(10000,99999)
                socket.sendall(bytes(str(randomid), "utf8"))
                NewSession = Session(randomid, socket, addr, TListLength)
                Sessionlist.append(NewSession)
                x = threading.Thread(target=RockPaperScissors, args=(NewSession,))
                Threadlist.append(x)
                x.start()
                KeepTrying = False

            elif int(datastring) >= 10000 and int(datastring) <= 99999:
                codeinlist = False
                for i in Sessionlist:
                    if i.id == int(datastring):
                        codeinlist = True
                        if i.participants[1] == None and i.addresses[1] == None:
                            i.participants[1] = socket
                            i.addresses[1] = addr
                            i.statestring = "2PlayersJoined"
                            KeepTrying = False
                            break
                        else:
                            socket.sendall(bytes("Session already full", "utf8"))
                if codeinlist == False:
                    try:
                        socket.sendall(bytes("SessionNotExist", "utf8"))
                    except:
                        print("fail")        
    except:
        pass

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.settimeout(30)
    while True:
        print("Listening")
        s.listen()
        conn, addr = s.accept()
        AddressList.append(addr)
        x = threading.Thread(target=JoinOrCreate, args=(conn,))
        Threadlist.append(x)
        x.start()        
  