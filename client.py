import socket
import time
import threading
import random
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65222  # The port used by the server
ThreadList = []

import kivy
kivy.require('1.0.7')

from functools import partial
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.textinput import TextInput

sm = ScreenManager()
sm.add_widget(Screen())


Builder.load_string("""
<MainMenu>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                # self here refers to the widget i.e FloatLayout
                pos: self.pos
                size: self.size
        Label:
            font_size: 64
            color: 0, 0, 0, 1
            text: "Rock-Paper-Scissors"
            font_name: "OpenSans-Medium.ttf"
            pos_hint: {'center_x': .5, 'center_y': .75}
        Button:
            border: 5, 5, 5 , 5
            background_color: 0.882, 0.745, 0.905, 1
            text: "Create a game"
            size_hint: (.25, .25)
            pos_hint: {'center_x': .25, 'center_y': .25}
            on_press: root.CreateGameFunction(root.manager)
        Button:
            background_color: 0.882, 0.745, 0.905, 1
            size_hint: (.25, .25)
            pos_hint: {'center_x': .75, 'center_y': .25}
            text: "Join a game"
            on_press: root.JoinGameFunction(root.manager)

<CreateGame>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                # self here refers to the widget i.e FloatLayout
                pos: self.pos
                size: self.size
        Label:
            id: waitinglabel
            font_size: 64
            text: root.label1text[0]
            font_name: "OpenSans-Medium.ttf"
            color: 0, 0, 0, 1
            pos_hint: {"center_x": 0.5, 'center_y': .5}
            size_hint_x: None
            size_hint_y: None

<CreateSocket>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                # self here refers to the widget i.e FloatLayout
                pos: self.pos
                size: self.size
        Label:
            id: waitinglabel
            font_size: 64
            text: root.label1text[0]
            font_name: "OpenSans-Medium.ttf"
            color: 0, 0, 0, 1
            pos_hint: {"center_x": 0.5, 'center_y': .5}
            size_hint_x: None
            size_hint_y: None


<JoinGame>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                # self here refers to the widget i.e FloatLayout
                pos: self.pos
                size: self.size
        Label:
            id: Joininglabel
            font_size: 64
            text: "Join a game by putting in a 5 digit code"
            font_name: "OpenSans-Medium.ttf"
            color: 0, 0, 0, 1
            pos_hint: {"center_x": 0.5, 'center_y': .75}
            text_size: self.width, None
            size_hint: 1, None
            height: self.texture_size[1]
            halign: 'center'
        TextInput:
            id: textinputcode
            font_size: 32
            pos_hint: {"center_x": 0.5, 'center_y': .25}
            size_hint: (None, None)
            multiline: False
            height: self.minimum_height
            on_text: root.handletextinput(root, self.text)
            on_text_validate: root.entertextinput(root, self.text)
        Label:
            id: TooShort
            font_size: 16
            text: "input too short"
            font_name: "OpenSans-Medium.ttf"
            color: 1, 0, 0, 0
            pos_hint: {"center_x": 0.5, 'center_y': .10}
            size_hint_x: None
            size_hint_y: None
        Label:
            id: NoSession
            font_size: 16
            text: "id doesn't exist"
            font_name: "OpenSans-Medium.ttf"
            color: 1, 0, 0, 0
            pos_hint: {"center_x": 0.5, 'center_y': .10}
            size_hint_x: None
            size_hint_y: None



<CreatedGame>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                # self here refers to the widget i.e FloatLayout
                pos: self.pos
                size: self.size
        Label:
            id: Createdgame
            font_size: 64
            text: "Game created"
            font_name: "OpenSans-Medium.ttf"
            color: 0, 0, 0, 1
            pos_hint: {"center_x": 0.5, 'center_y': .75}
            size_hint_x: None
            size_hint_y: None
        Label:
            id: gameid
            font_size: 64
            text: "Join id:" 
            font_name: "OpenSans-Medium.ttf"
            color: 0, 0, 0, 1
            pos_hint: {"center_x": 0.5, 'center_y': .25}
            size_hint_x: None
            size_hint_y: None
<GameScreen>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                # self here refers to the widget i.e FloatLayout
                pos: self.pos
                size: self.size
        Label:
            id: GameMainText
            font_size: 64
            text: "Waiting to start"
            font_name: "OpenSans-Medium.ttf"
            color: 0, 0, 0, 1
            pos_hint: {"center_x": 0.5, 'center_y': .75}
            size_hint_x: None
            size_hint_y: None

        Button:
            opacity: 0
            id: PaperButton
            background_color: 0, 0, 0, 1
            size_hint: (.25, .25)
            pos_hint: {'center_x': .25, 'center_y': .25}
            background_normal: ''
            disabled: True
            on_press: root.RockPaperScissorAction("paper", root)
            text: "Paper"
        Button:
            opacity: 0
            id: RockButton
            background_color: 0, 0, 0, 1
            size_hint: (.25, .25)
            pos_hint: {'center_x': .5, 'center_y': .25}
            background_normal: ''
            disabled: True
            on_press: root.RockPaperScissorAction("rock", root)
            text: "Rock"

        Button:
            opacity: 0
            id: ScissorsButton
            background_color: 0, 0, 0, 1
            size_hint: (.25, .25)
            pos_hint: {'center_x': .75, 'center_y': .25}
            background_normal: ''
            disabled: True
            on_press: root.RockPaperScissorAction("scissors", root)
            text: "Scissors"



<ResultsScreen>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                # self here refers to the widget i.e FloatLayout
                pos: self.pos
                size: self.size
        Label:
            id: ResultMainText
            font_size: 64
            text: "Results"
            font_name: "OpenSans-Medium.ttf"
            color: 0, 0, 0, 1
            pos_hint: {"center_x": 0.5, 'center_y': .75}
            size_hint_x: None
            size_hint_y: None
        Label:
            font_size: 24
            text: "Outcome: "
            font_name: "OpenSans-Medium.ttf"
            color: 0, 0, 0, 1
            pos_hint: {"center_x": 0.25, 'center_y': .35}
            size_hint_x: None
            size_hint_y: None
        Label:
            font_size: 24
            text: "Your Move: "
            font_name: "OpenSans-Medium.ttf"
            color: 0, 0, 0, 1
            pos_hint: {"center_x": 0.5, 'center_y': .35}
            size_hint_x: None
            size_hint_y: None
        Label:
            font_size: 24
            text: "Opponent's Move: "
            font_name: "OpenSans-Medium.ttf"
            color: 0, 0, 0, 1
            pos_hint: {"center_x": 0.75, 'center_y': .35}
            size_hint_x: None
            size_hint_y: None
        Label:
            id: WinnerLabel
            font_size: 16
            text: "Waiting for opponent"
            font_name: "OpenSans-Medium.ttf"
            color: 0, 0, 0, 1
            pos_hint: {"center_x": 0.25, 'center_y': .25}
            size_hint_x: None
            size_hint_y: None
        Label:
            id: YourmoveLabel
            font_size: 16
            text: "Waiting for opponent"
            font_name: "OpenSans-Medium.ttf"
            color: 0, 0, 0, 1
            pos_hint: {"center_x": 0.5, 'center_y': .25}
            size_hint_x: None
            size_hint_y: None
        Label:
            id: OpponentMoveLabel
            font_size: 16
            text: "Waiting for opponent"
            font_name: "OpenSans-Medium.ttf"
            color: 0, 0, 0, 1
            pos_hint: {"center_x": 0.75, 'center_y': .25}
            size_hint_x: None
            size_hint_y: None

        Button:
            background_color: 0.5, 0.5, 0.5, 1
            size_hint: (.2, .1)
            pos_hint: {'center_x': .5, 'center_y': .10}
            text: "Exit"
            background_normal: ''
            on_press: root.exitgame()

""")

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


def ConnectionThread(ConnectionStatus):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for i in range(10):
        try:
            s.connect((HOST, PORT))    
            ConnectionStatus[0] = "success"
            break
        except:
            pass
        time.sleep(0.5)
    if ConnectionStatus[0] == "waiting":
        ConnectionStatus[0] = "failed"
    elif ConnectionStatus[0] == "success":
        global socketforgame
        socketforgame = s

def WaitForMessageThread(message):
    global socketforgame
    data = socketforgame.recv(1024)
    datastring = str(data, "utf8")
    message[0] = datastring


def JoiningStatus(self, dt):
    global GameSessionObject
    if GameSessionObject.latestmessage == "2ndPlayerMissing":
        try:
            GameSessionObject.socket.close()
            GameSessionObject = None
        except:
            GameSessionObject = None
            pass
        self.manager.current = "menu"
        return False
    if GameSessionObject.latestmessage == "Accepted":
        try:
            GameSessionObject.socket.sendall(bytes("ok", 'utf8'))
            self.manager.current = "gamescreen"
        except:
            print("Failed to send ok")
        GameSessionObject.latestmessage = None
        return False
    if GameSessionObject.latestmessage == "SessionNotExist":
        self.ids.NoSession.color = (1, 0, 0, 1)
        GameSessionObject.latestmessage = None
        return False
        
def ConnectStatus(connectionstatus, goal, self, dt):
    global GameSessionObject
    if GameSessionObject.sessionstatus == "CreatingSocket":
        pass
    if GameSessionObject.sessionstatus == "SocketCreated":
        if GameSessionObject.role == "Create":
            self.manager.current = "createdgame"
        if GameSessionObject.role == "Join":
            self.manager.current = "joingame"
        return False
    elif GameSessionObject.sessionstatus == "FailedSocketCreation":
        self.manager.current = "menu"
        GameSessionObject = None
        return False
    if self.label1text[0] == "Waiting...":
        self.label1text[0] = "Waiting."
    elif self.label1text[0] == "Waiting.":
        self.label1text[0] = "Waiting.."
    elif self.label1text[0] == "Waiting..":
        self.label1text[0] = "Waiting..."
    self.ids.waitinglabel.text = self.label1text[0]


class MainMenu(Screen):
    def on_enter(self):
        global GameSessionObject
        gameSessionObject = None
    def CreateGameFunction(self, sm):
        global goalofplayer
        goalofplayer = "Create"
        sm.current = "createsocket"
    def JoinGameFunction(self, sm):
        global goalofplayer
        goalofplayer = "Join"
        sm.current = "createsocket"
    pass

def GameStatus(self, dt):
    global GameSessionObject
    if GameSessionObject.latestmessage == "test":
        try:
            GameSessionObject.socket.sendall(bytes("test", 'utf8'))
            GameSessionObject.latestmessage = None
            GameSessionObject.ReceiveAMessage()
        except:
            print("Failed to send test")
    if GameSessionObject.latestmessage == "start":        
        self.ids.GameMainText.text = "Select one action"
        self.ids.RockButton.opacity = 1
        self.ids.ScissorsButton.opacity = 1
        self.ids.PaperButton.opacity = 1
        self.ids.PaperButton.disabled = False
        self.ids.RockButton.disabled = False
        self.ids.ScissorsButton.disabled = False
        GameSessionObject.latestmessage = None
        GameSessionObject.ReceiveAMessage()
    if GameSessionObject.latestmessage == "movereceived":   
        self.manager.current = "resultsscreen"
        GameSessionObject.latestmessage = None
        return False
    if GameSessionObject.latestmessage == "timeout":   
        self.ids.GameMainText.text = "Input too late"
        self.ids.RockButton.opacity = 0
        self.ids.ScissorsButton.opacity = 0
        self.ids.PaperButton.opacity = 0
        self.ids.PaperButton.disabled = True
        self.ids.RockButton.disabled = True
        self.ids.ScissorsButton.disabled = True
        self.manager.current = "resultsscreen"
        GameSessionObject.latestmessage = None
        return False


def ResultsStatus(self, dt):
    global GameSessionObject
    if GameSessionObject.latestmessage != None:
        message = list(str(GameSessionObject.latestmessage).split(","))
        if message[0] == "0":
            self.ids.WinnerLabel.text = "Draw"
        elif message[0] == "1":
            if GameSessionObject.role == "Join":
                self.ids.WinnerLabel.text = "Lose"
            if GameSessionObject.role == "Create":
                self.ids.WinnerLabel.text = "Win"
        elif message[0] == "2":
            if GameSessionObject.role == "Join":
                self.ids.WinnerLabel.text = "Win"
            if GameSessionObject.role == "Create":
                self.ids.WinnerLabel.text = "Lose"
        if GameSessionObject.role == "Join":
            if message[1] == "1":
                self.ids.OpponentMoveLabel.text = "Scissors"    
            elif message[1] == "2":
                self.ids.OpponentMoveLabel.text = "Paper"    
            elif message[1] == "3":
                self.ids.OpponentMoveLabel.text = "Rock"    
            if message[2] == "1":
                self.ids.YourmoveLabel.text = "Scissors"    
            elif message[2] == "2":
                self.ids.YourmoveLabel.text = "Paper"    
            elif message[2] == "3":
                self.ids.YourmoveLabel.text = "Rock"    
        elif GameSessionObject.role == "Create":
            if message[2] == "1":
                self.ids.OpponentMoveLabel.text = "Scissors"    
            elif message[2] == "2":
                self.ids.OpponentMoveLabel.text = "Paper"    
            elif message[2] == "3":
                self.ids.OpponentMoveLabel.text = "Rock"    
            if message[1] == "1":
                self.ids.YourmoveLabel.text = "Scissors"    
            elif message[1] == "2":
                self.ids.YourmoveLabel.text = "Paper"    
            elif message[1] == "3":
                self.ids.YourmoveLabel.text = "Rock"   
        GameSessionObject.latestmessage = None
        return False


class ResultsScreen(Screen):
    def on_enter(self):
        global GameSessionObject
        if not GameSessionObject:
            self.manager.current = "menu"
        else:
            try:
                GameSessionObject.socket.sendall(bytes("GiveResults", 'utf8'))
                GameSessionObject.ReceiveAMessage()
                event = Clock.schedule_interval(partial(ResultsStatus, self), 0.1)
            except: 
                print("Couldn't request results")

    def exitgame(self):
        global GameSessionObject
        GameSessionObject = None
        self.manager.current = "menu"

class GameScreen(Screen):
    def RockPaperScissorAction(self, action, root):
        global GameSessionObject
        if action == "rock":
            try:     
                GameSessionObject.socket.sendall(bytes("rock", 'utf8'))
                root.ids.PaperButton.opacity = 0
                root.ids.ScissorsButton.opacity = 0
                root.ids.PaperButton.disabled = True
                root.ids.RockButton.disabled = True
                root.ids.ScissorsButton.disabled = True
            except: 
                print("Failed")
        elif action == "paper":
            try:     
                GameSessionObject.socket.sendall(bytes("paper", 'utf8'))
                root.ids.RockButton.opacity = 0
                root.ids.ScissorsButton.opacity = 0
                root.ids.PaperButton.disabled = True
                root.ids.RockButton.disabled = True
                root.ids.ScissorsButton.disabled = True
            except: 
                print("Failed")        
        elif action == "scissors":
            try:     
                GameSessionObject.socket.sendall(bytes("scissors", 'utf8'))
                root.ids.PaperButton.opacity = 0
                root.ids.RockButton.opacity = 0
                root.ids.PaperButton.disabled = True
                root.ids.RockButton.disabled = True
                root.ids.ScissorsButton.disabled = True
            except: 
                print("Failed")


    def on_enter(self):
        global GameSessionObject
        GameSessionObject.ReceiveAMessage()
        event = Clock.schedule_interval(partial(GameStatus, self), 0.1)
    pass


class JoinGame(Screen):
    def handletextinput(self, root, text):
        if len(text) >= 1: 
            if text[-1] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                root.ids.textinputcode.text = text[:-1]
        if len(text.strip()) >= 6: 
            root.ids.textinputcode.text = text[0:5]
    def entertextinput(self, root, text):
        if len(text.strip()) < 5: 
            root.ids.NoSession.color = (1, 0, 0, 0)
            root.ids.TooShort.color = (1, 0, 0, 1)
        else:
            global GameSessionObject
            socketforgame = GameSessionObject.socket
            root.ids.TooShort.color = (1, 0, 0, 0)
            root.ids.NoSession.color = (1, 0, 0, 0)
            try:
                socketforgame.sendall(bytes(str(text), 'utf8'))
            except:
                print("failedtosendid")
            GameSessionObject.ReceiveAMessage()
            event = Clock.schedule_interval(partial(JoiningStatus, self,), 0.5)
    pass


class CreatedGame(Screen):
    def on_enter(self):
        global GameSessionObject
        GameSessionObject.socket.sendall(bytes(str(1), 'utf8') )
        try:
            data = GameSessionObject.socket.recv(1024)
            datastring = str(data, "utf8")
        except:
            print("Failed")
            GameSessionObject = None
            self.manager.current = "menu"
        self.ids.gameid.text = "Join id: " + str(datastring)
        GameSessionObject.ReceiveAMessage()
        event = Clock.schedule_interval(partial(JoiningStatus, self,), 0.5)
    pass


class CreateSocket(Screen):
    label1text = ["Waiting..."]
    def on_enter(self):
        global GameSessionObject
        GameSessionObject = ClientsideSession("host")
        global goalofplayer
        GameSessionObject.role = goalofplayer
        event = Clock.schedule_interval(partial(ConnectStatus, GameSessionObject.sessionstatus, goalofplayer, self), 0.3)


class CreateGame(Screen):
    label1text = ["Waiting..."]
    def on_enter(self):
        SessionObject = ClientsideSession("host")
        global GameSessionObject
        GameSessionObject = SessionObject
        event = Clock.schedule_interval(partial(ConnectStatus, SessionObject.sessionstatus, self), 0.3)

    pass

class RockPaperScissorsApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name="menu"))
        sm.add_widget(JoinGame(name="joingame"))
        sm.add_widget(CreateGame(name="creategame"))
        sm.add_widget(CreatedGame(name="createdgame"))
        sm.add_widget(CreateSocket(name="createsocket"))
        sm.add_widget(GameScreen(name="gamescreen"))
        sm.add_widget(ResultsScreen(name="resultsscreen"))
        return(sm)

def main():
    RockPaperScissorsApp().run()

main()