import socket
import threading


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


    def start_fight(self, player1, player2):
        message1 = f"START GAME WITH {player2.address}:{player2.port}\n"
        message2 = f"START GAME WITH {player1.address}:{player1.port}\n"
        
        player1.connection.sendall(message1.encode())
        player2.connection.sendall(message2.encode())


    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print(f"Listening for connections on {self.host}:{self.port}")

        while True:
            connection, address = self.socket.accept()
            self.connections.append(connection)
            print(f"Accepted connection from {address[0]} {address[1]}")
            #Connect back to player
            #self.connect(address[0], address[1])
            threading.Thread(target=self.handle_client, args=(connection, address)).start()

    def send_data(self, data):
        for connection in self.connections:
            try:
                connection.sendall(data.encode())
            except socket.error as e:
                print(f"Failed to send data. Error: {e}")
                self.connections.remove(connection)


    def handle_data(self, data, address):
        if data.startswith("HELLO"):
            if len(self.players) == 0:
                connection = self.connect(address[0], 8000)
                time.sleep(1)
                connection.sendall("HELLO YOU TOO\n".encode())

            if len(self.players) >= 1:
                connection = self.connect(address[0], 8001)
                time.sleep(1)
                connection.sendall("HELLO YOU TOO\n".encode())
                self.start_fight(self.players[-1], Player(connection, address[0], address[1]))
                self.players.remove(self.players[-1])
            self.players.append(Player(connection, address[0], address[1]))


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

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()


if __name__ == "__main__":


    import time
    time.sleep(2)

    node2 = Peer("0.0.0.0", 8002)
    node2.start()

    #node2.connect("127.0.0.1", 8000)
    time.sleep(1)  # Allow connection to establish
    #node2.send_data("Hello from node2!\n")
