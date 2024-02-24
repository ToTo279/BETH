import socket
import os
from threading import Thread
from random import randint
from time import sleep, time
import json
from typing import List
HELP = """help -> displays this message
ls -> lists active satelites
add -> creates a new satelite
<id> rmv -> removes the satelite
<id> msg <msg> -> sends a message to the base"""

IP =  "localhost" #"10.42.0.1" #

class Client:
    def __init__(self, id, host, port):
        self.id = id
        self.host = host
        self.port = port
        self.running = True

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
        except:
            print("Could not make a connection to the server")
            return
                
        #Create new thread to wait for data
        mainThread = Thread(target = self.main)
        mainThread.start()
        self.handshake()
    

    def handshake(self):
        try:
            data = {"id":self.id, "battery_status":87}
            data = json.dumps(data)
            data = str.encode(data)
            self.sock.send(data)
        except Exception as e:
            print(f"Exception: {e}")
            self.running = False
            self.sock.close()

    def handle_command(self, data:str):
        print(f"\n{self.id}<-\x1B[3m{data}\x1B[0m")
        data = json.loads(data)
        if "command" not in data: return
        command = data["command"]
        if command == "start_countdown":
            sleep(3)
            self.send_message('{"command":"start_countdown"}')
        
        elif command == "set_game":
            self.send_message(json.dumps(data))
        
        elif command == "wait_swing":
            x = randint(0,100)
            if x < 15:
                self.send_message(json.dumps({
                "command":"wait_swing",
                "arg1":10.0
                }))
            else:
                time = randint(10,50)/10
                sleep(time)
                self.send_message(json.dumps({
                    "command":command,
                    "arg1":time
                }))
        
        elif command == "stop":
            self.send_message(json.dumps(data))

    def send_message(self, message:str):
        try:
            data = str.encode(message)
            print(f"\t[{self.id}->\x1B[3m{data}\x1B[0m]\n")
            self.sock.send(data)
        except Exception as e:
            print(f"Exception: {e}")
            self.sock.close()
            self.running = False

    def close(self):
        self.sock.close()
        self.running = False

    #Wait for incoming data from server
    #.decode is used to turn the message in bytes to a string
    def main(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
                if data == b'':
                    break
                datas = data.decode("utf-8").split("}")
                for data in datas:
                    if data == "": continue
                    self.handle_command(data+'}')
            except Exception as e:
                print(f"Exception: {e}")    
                print(e)
                print("You have been disconnected from the server")
                self.running = False
                if all([sat.running==False for sat in satelites]):
                    os._exit(1)
                print([sat.running==False for sat in satelites])

satelites:List[Client] = [Client(i, IP, 8888) for i in range(4)]
running = True
def handle_command(cmd:str):
    if cmd == "help":
        return print(HELP)
    elif cmd == "add":
        id = satelites[-1].id +1
        satelites.append(Client(id, IP, 8888))
        return
    elif cmd == "ls":
        out = ""
        for i in satelites:
            out += f"Satelite {i.id}\n"
        return print(out)
    parts = cmd.split()
    try:
        id = int(parts[0])
    except:
        return print("Id not valid, must be int")
    if len(satelites) <= id:
        return print(f"id is not valid, must be between 0 and {len(satelites)-1}") 
    client: Client = satelites[id]
    cmd = parts[1]
    if cmd == "msg":
        data = " ".join(parts[2:])
        client.send_message(data)
    if cmd == "rmv":
        client.close()
        satelites.remove(client)

try:
    while True:
        command = input(" > ")
        handle_command(command)
except Exception as e:
    print(f"Exception:{e}")
    for client in satelites:
        client.close()
except KeyboardInterrupt:
    for client in satelites:
        client.close()
    print("Exiting programm")