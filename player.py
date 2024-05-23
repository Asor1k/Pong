import socket
import threading
import pygame, sys
import time, math


enemy_address = ("0.0.0.0", 8000)
is_connected = False
is_player_right = False
is_started_game = False

class EnemyData:
    def __init__(self) -> None:
        self.enemyPositiony = float(0)
        self.ballPositionX = float(0)
        self.ballPositionY = float(0)

enemyData = EnemyData()

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []

    def connect(self, peer_host, peer_port):
        connection = socket.create_connection((peer_host, peer_port))
        self.connections.append(connection)
        print(f"Connected to {peer_host}:{peer_port}")
        return connection

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print(f"Listening for connections on {self.host}:{self.port}")

        while True:
            connection, address = self.socket.accept()
            self.connections.append(connection)
            print(f"Accepted connection from {address}")
            threading.Thread(target=self.handle_client, args=(connection, address)).start()
            # Let's say we get this connection from the server. Make dynamic and move elsewhere 
            #self.connect("127.0.0.1", 8002)

    def start_game(self, address):
        self.enemyConnection = self.connect(address[0], 8000)
        print(f"Connected with player on {address[0]}:{address[1]}")
        global is_connected
        is_connected = True


    def handle_data(self, data):
        if data.startswith("START GAME WITH"):
            replaced = data.replace("START GAME WITH", "")
            replaced = replaced.strip()
            global is_player_right
            if replaced[0] == 'R':
                is_player_right = True

            replaced = replaced[1:].strip()

            self.start_game(replaced.split(":"))
            
        if data.startswith("DATA"):
            replaced = data.replace("DATA", "")
            global enemyData
            values = replaced.split(";")
            enemyData.enemyPositiony = float(values[0])
            enemyData.ballPositionX = float(values[1])
            enemyData.ballPositionY = float(values[2])
        if data.startswith("START"):
            global is_started_game
            is_started_game = True
            print("Got start!")

    def send_data(self, data):
        for connection in self.connections:
            try:
                connection.sendall(data.encode())
            except socket.error as e:
                print(f"Failed to send data. Error: {e}")
                self.connections.remove(connection)

    def send_data_to_enemy(self, data):
        try:
            self.enemyConnection.sendall(data.encode())
        except socket.error as e:
            print(f"Failed to send data. Error: {e}")
           # self.connections.remove(self.enemyConnection)



    def handle_client(self, connection, address):
        while True:
            try:
                data = ""
                while True:
                    data += connection.recv(1).decode("utf-8")
                    if data == "" or data[-1:] == "\n" or not data :
                       break

                print(f"Received data from {address}: {data}")
                self.handle_data(data)
            except socket.error:
                break

        print(f"Connection from {address} closed.")
        self.connections.remove(connection)
        connection.close()

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()


size = width, height = 1024, 512
black = 0,0,0
server_host = "26.49.11.40"
server_port = 8002


class Ball:
    def __init__(self, model, velocity):
        self.model = model
        self.model = pygame.transform.scale(self.model, (25, 25))
        self.transform = self.model.get_rect()
        self.accumulated_speed = (0.0, 0.0)
        self.velocity = velocity
        self.speed = (0, 0)

    def move(self):
        self.accumulated_speed = (self.accumulated_speed[0] + self.speed[0], self.accumulated_speed[1] + self.speed[1])

        step_move_speed = (int(self.accumulated_speed[0]), int(self.accumulated_speed[1]))

        self.accumulated_speed = (self.accumulated_speed[0] - step_move_speed[0], self.accumulated_speed[1] - step_move_speed[1])

        self.transform = self.transform.move(step_move_speed)

    def reset(self):
        self.transform.center = (width/2, height/2)
        self.speed = (-self.velocity, 0)



class Player:
    def __init__(self, model):
        self.model = model
        self.model = pygame.transform.scale(self.model, (25, 100))
        self.transform = self.model.get_rect()
        self.player_velocity = 5
    def move(self, speed):
        self.transform = self.transform.move(speed)


def get_score_text(x,y):
    return f"{x} : {y}"


class Client:
    def __init__(self, port):
        self.node = Peer("0.0.0.0", port)
        self.node.start()
        self.start_game()

    def start_game(self):
        pygame.init()
        pygame.font.init() 
        pygame.display.set_caption('Pong')

        my_font = pygame.font.SysFont('Futura', 60)
        screen = pygame.display.set_mode(size)

        while True:
            clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True
                    break
            if clicked:
                break
            screen.fill(black)
            hello_text_surface = my_font.render("WELCOME TO PONG!", False, (255, 255, 255))
            hello_text_surface2 = my_font.render("PRESS ANY MOUSE BUTTON", False, (255, 255, 255))
            hello_text_surface3 = my_font.render("TO CONNECT TO WAITING QUEUE", False, (255, 255, 255))

            screen.blit(hello_text_surface, (width / 2 - 200, height / 2 - 50))
            screen.blit(hello_text_surface2, (width / 2 - 250, height / 2))
            screen.blit(hello_text_surface3, (width / 2 - 300, height / 2 + 50))
            pygame.display.flip()

        print("Connecting to the server...")
        try:
            self.node.connect(server_host, server_port)
            time.sleep(1)
        except socket.error as err:
            print("Unable to connect to the server! " + str(err))
            exit()

        time.sleep(1)
        print("Connected to the server!")

        screen.fill(black)
        pygame.display.flip()
        hello_message = "HELLO\n"
        self.node.send_data(hello_message)

        while True:
            if is_connected:
                break
            time.sleep(1)
            print("Waiting in the queue...")

        print("Connected!")
        time.sleep(3)

        ball_speed = 5
        MAX_BOUNCE_ANGLE = 5 * 3.14 / 12
        paddle_height = 100

        ball = Ball(pygame.image.load("ball.jpg"), ball_speed)
        ball.reset()
        player = Player(pygame.image.load("player.jpg"))
        enemy = Player(pygame.image.load("player.jpg"))

        if not is_player_right:
            player.transform.center = (0, height/2)
            enemy.transform.center = (width, height/2)
        else:
            enemy.transform.center = (0, height/2)
            player.transform.center = (width, height/2)

        fps = 60
        start_time = time.time()
        colided_time = 0
        score = (0, 0)
        send_wait_time = time.time()
        text_surface = my_font.render(get_score_text(0,0), False, (255, 255, 255))

        self.node.send_data_to_enemy("START\n")
        global is_started_game
        while not is_started_game:
            continue

        player_moving_up = False
        player_moving_down = False
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        player_moving_up = True
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        player_moving_down = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        player_moving_up = False
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        player_moving_down = False                

            if time.time() - colided_time > 0.4:

                leftTransform = enemy.transform if is_player_right else player.transform
                rightTransform = player.transform if is_player_right else enemy.transform

                if ball.transform.colliderect(leftTransform):
                    relativeIntersectY = ball.transform.centery - leftTransform.centery
                    normalizedRelativeIntersectionY = (relativeIntersectY / (paddle_height / 2))
                    bounceAngle = normalizedRelativeIntersectionY * MAX_BOUNCE_ANGLE
                    ball.speed = (ball.velocity * math.cos(bounceAngle), ball.velocity * math.sin(bounceAngle))
                    ball.accumulated_speed = (0, 0)
                    ball.move()
                    colided_time = time.time()

                if ball.transform.colliderect(rightTransform):
                    relativeIntersectY = ball.transform.centery - rightTransform.centery
                    normalizedRelativeIntersectionY = (relativeIntersectY / (paddle_height / 2))
                    bounceAngle = 3.14 - normalizedRelativeIntersectionY * MAX_BOUNCE_ANGLE
                    ball.speed = (ball.velocity * math.cos(bounceAngle), ball.velocity * math.sin(bounceAngle))
                    ball.accumulated_speed = (0, 0)
                    ball.move()
                    colided_time = time.time()


                if (ball.transform.top <= 0 or ball.transform.bottom >= height):
                    ball.accumulated_speed = (0, 0)
                    ball.speed = (ball.speed[0], -ball.speed[1])
                    ball.move()
                    colided_time = time.time()

                if ball.transform.centerx >= width:
                    # Player left scored a point
                    score = (score[0] + 1, score[1])
                    colided_time = time.time()
                    time.sleep(0.2)
                    ball.reset()

                if ball.transform.centerx <= 0:
                    # Player right scored a point
                    score = (score[0], score[1] + 1)
                    colided_time = time.time()
                    time.sleep(0.2)
                    ball.reset()

            # ownPosition;ballPositionX;ballPositionY

            #enemy.transform = enemy.transform.move((enemy.transform.centerx - enemy.transform.centerx, enemy.transform.centery - enemyData.enemyPositiony))
            enemy.transform.center = (enemy.transform.centerx, float(enemyData.enemyPositiony))
            
            text_surface = my_font.render(get_score_text(score[0], score[1]), False, (255, 255, 255))

            if time.time() - send_wait_time >= 0.5 / fps:
                if is_player_right:
                    self.node.send_data_to_enemy(f"DATA {player.transform.centery};-1;-1\n")
                else:
                    self.node.send_data_to_enemy(f"DATA {player.transform.centery};{ball.transform.centerx};{ball.transform.centery}\n")
                send_wait_time = time.time()

            if time.time() - start_time >= 1.0 / fps:
                if is_player_right:
                    ball.transform.center = (enemyData.ballPositionX, float(enemyData.ballPositionY))
                    #ball.transform = ball.transform.move((ball.transform.centerx - enemyData.ballPositionX, ball.transform.centery - enemyData.ballPositionY))
                else:
                    ball.move()

                if player_moving_up:
                    player.move((0, player.player_velocity))
                if player_moving_down:
                    player.move((0, -player.player_velocity))

                start_time = time.time()
            

           # ball.move([1,1])
            screen.fill(black)
            screen.blit(ball.model, ball.transform)
            screen.blit(player.model, player.transform)
            screen.blit(enemy.model, enemy.transform)
            screen.blit(text_surface, (width / 2 - 60, 0))

            clock.tick(fps)
            pygame.display.flip()



# Example usage:
if __name__ == "__main__":

    client = Client(8000)

    time.sleep(5)

    # Let's say we get this connection from the server. Make dynamic and move elsewhere 
    #client.node.connect("127.0.0.1", 8001)


    print("Can start second node")
    # Give some time for nodes to start listening
    import time

    #node2 = Peer("0.0.0.0", 8003)
    #node2.start()

    #node2.connect("127.0.0.1", 8000)
    #time.sleep(1)  # Allow connection to establish
    #node2.send_data("Hello from node2!")
