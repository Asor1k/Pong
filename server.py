import socket
import threading
import os

def get_computer_remote_ip():
    #Hack to get local IP of this PC if the server is launched localy
    return [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]


class Player:
    def __init__(self, connection, address, port) -> None:
        self.address = address
        self.port = port
        self.connection = connection



# GET - HELLO\n



# SEND - FOUND ENEMY {IP}:{PORT}\n 


class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.players = []


    def connect(self, peer_host, peer_port):
        connection = socket.create_connection((peer_host, peer_port))

        self.connections.append(connection)
        print(f"Connected to {peer_host}:{peer_port}")
        return connection

    # Send messages to two players to start the game
    def start_fight(self, player1, player2):
        message1 = f"START GAME WITH L {player2.address}:{player2.port}\n"
        message2 = f"START GAME WITH R {player1.address}:{player1.port}\n"
        
        player1.connection.sendall(message1.encode())
        player2.connection.sendall(message2.encode())

     # Listen for incoming connections
    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print(f"Listening for connections on {self.host}:{self.port}")

        while True:
            connection, address = self.socket.accept()
            
            self.connections.append(connection)
            print(f"Accepted connection from {address}")
            #Connect back to player
            #self.connect(address[0], address[1])
            threading.Thread(target=self.handle_client, args=(connection, address)).start()
            
    # Send data to all connected clients
    def send_data(self, data):
        for connection in self.connections:
            try:
                connection.sendall(data.encode())
            except socket.error as e:
                print(f"Failed to send data. Error: {e}")
                self.connections.remove(connection)

    def handle_data(self, data, address):
        if data.startswith("HELLO"):
            connect_address = address[0]
            if connect_address.startswith("127."):
                connect_address = get_computer_remote_ip()
            # If no players are connected, connect to the new player
            if len(self.players) == 0:
                connection = self.connect(connect_address, 8000)
                time.sleep(1)
                connection.sendall("HELLO YOU TOO\n".encode())
             # If a player is already connected, start a game between the new and existing player
            if len(self.players) >= 1:
                connection = self.connect(connect_address, 8000)
                time.sleep(1)
                connection.sendall("HELLO YOU TOO\n".encode())
                self.start_fight(self.players[-1], Player(connection, connect_address, address[1]))
                self.players.remove(self.players[-1])
            self.players.append(Player(connection, connect_address, address[1]))

    # Handle communication with a connected client
    def handle_client(self, connection, address):
        while True:
            try:
                data = ""
                while True:
                    data += connection.recv(1).decode("utf-8")
                    if data == "" or data[-1:] == "\n" or not data :
                       break

                print(f"Received data from {address}: {data}")
                self.handle_data(data, address)

            except socket.error as inst:
                print(inst)
                break

        print(f"Connection from {address} closed.")
        self.connections.remove(connection)
        connection.close()
        
     # Start the listening thread
    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()
    

if __name__ == "__main__":

    import time
    time.sleep(2)

    node2 = Peer("0.0.0.0", 8002)
    node2.start()
   

#rd_2gpj0qyZlza1whSoCwo0TQ7jyNf
#included-serval-amazingly.ngrok-free.app

    #node2.connect("127.0.0.1", 8000)
    time.sleep(1)  # Allow connection to establish
    #node2.send_data("Hello from node2!\n")
