import pygame, sys
import time, math

size = width, height = 1024, 512

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


def main():
    pygame.init()
    pygame.font.init() 
    size = width, height = 1024, 512
    black = 0,0,0
    ball_speed = 5
    MAX_BOUNCE_ANGLE = 5 * 3.14 / 12
    paddle_height = 100
    screen = pygame.display.set_mode(size)

    my_font = pygame.font.SysFont('Futura', 60)

    
    ball = Ball(pygame.image.load("ball.jpg"), ball_speed)
    ball.reset()
    player1 = Player(pygame.image.load("player.jpg"))
    player2 = Player(pygame.image.load("player.jpg"))

    player1.transform.center = (0, height/2)
    player2.transform.center = (width, height/2)

    fps = 60
    start_time = time.time()
    colided_time = 0
    score = (0, 0)

    text_surface = my_font.render(get_score_text(0,0), False, (255, 255, 255))


    player1_moving_up = False
    player1_moving_down = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player1_moving_up = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player1_moving_down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player1_moving_up = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player1_moving_down = False                

        if time.time() - colided_time > 0.4:
            if ball.transform.colliderect(player1.transform):
                relativeIntersectY = ball.transform.centery - player1.transform.centery
                normalizedRelativeIntersectionY = (relativeIntersectY / (paddle_height / 2))
                bounceAngle = normalizedRelativeIntersectionY * MAX_BOUNCE_ANGLE
                ball.speed = (ball.velocity * math.cos(bounceAngle), ball.velocity * math.sin(bounceAngle))
                ball.accumulated_speed = (0, 0)
                print(ball.speed)
                print(bounceAngle)
                ball.move()
                colided_time = time.time()

            if (ball.transform.top <= 0 or ball.transform.bottom >= height):
                ball.accumulated_speed = (0, 0)
                ball.speed = (ball.speed[0], -ball.speed[1])
                ball.move()
                colided_time = time.time()

            if ball.transform.centerx >= width:
                # Player 1 scored a point
                score = (score[0] + 1, score[1])
                colided_time = time.time()
                ball.reset()



        text_surface = my_font.render(get_score_text(score[0], score[1]), False, (255, 255, 255))

        if time.time() - start_time >= 1.0 / fps:
            ball.move()
            if player1_moving_up:
                player1.move((0, player1.player_velocity))
            if player1_moving_down:
                player1.move((0, -player1.player_velocity))

            start_time = time.time()

       # ball.move([1,1])
        screen.fill(black)
        screen.blit(ball.model, ball.transform)
        screen.blit(player1.model, player1.transform)
        screen.blit(player2.model, player2.transform)
        screen.blit(text_surface, (width / 2 - 60, 0))


        pygame.display.flip()
            


    return
    

if __name__ == '__main__':
    main()