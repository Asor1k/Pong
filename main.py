import pygame, sys
import time, math

size = width, height = 1024, 512

class Ball:
    def __init__(self, model):
        self.model = model
        self.model = pygame.transform.scale(self.model, (25, 25))
        self.transform = self.model.get_rect()
        self.speed = (-1.5, 0)
        self.accumulated_speed = (0.0, 0.0)

    def move(self):
        self.accumulated_speed = (self.accumulated_speed[0] + self.speed[0], self.accumulated_speed[1] + self.speed[1])

        step_move_speed = (int(self.accumulated_speed[0]), int(self.accumulated_speed[1]))

        self.accumulated_speed = (self.accumulated_speed[0] - step_move_speed[0], self.accumulated_speed[1] - step_move_speed[1])

        self.transform = self.transform.move(step_move_speed)


class Player:
    def __init__(self, model):
        self.model = model
        self.model = pygame.transform.scale(self.model, (25, 100))
        self.transform = self.model.get_rect()
    def move(self, speed):
        self.transform = self.transform.move(speed)



def main():
    pygame.init()
    size = width, height = 1024, 512
    black = 0,0,0
    ball_speed = 1.5
    MAX_BOUNCE_ANGLE = 5 * 3.14 / 12
    paddle_height = 100
    screen = pygame.display.set_mode(size)

    ball = Ball(pygame.image.load("ball.jpg"))
    player1 = Player(pygame.image.load("player.jpg"))
    player2 = Player(pygame.image.load("player.jpg"))


    ball.transform.center = (width/2, height/2)
    player1.transform.center = (0, height/2)
    player2.transform.center = (width, height/2)

    fps = 60
    start_time = time.time()
    colided_time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player1.move((0, 5))
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player1.move((0, -5))

        if ball.transform.colliderect(player1.transform) and time.time() - colided_time > 1 :
            relativeIntersectY = ball.transform.centery - player1.transform.centery
            normalizedRelativeIntersectionY = (relativeIntersectY / (paddle_height / 2))
            bounceAngle = normalizedRelativeIntersectionY * MAX_BOUNCE_ANGLE
            ball.speed = (ball_speed * math.cos(bounceAngle), ball_speed * math.sin(bounceAngle))
            ball.accumulated_speed = (0, 0)
            print(ball.speed)
            print(bounceAngle)
            ball.move()
            colided_time = time.time()


        if time.time() - start_time >= 1.0 / fps:
            ball.move()
            start_time = time.time()

       # ball.move([1,1])
        screen.fill(black)
        screen.blit(ball.model, ball.transform)
        screen.blit(player1.model, player1.transform)
        screen.blit(player2.model, player2.transform)


        pygame.display.flip()
            


    return
    

if __name__ == '__main__':
    main()