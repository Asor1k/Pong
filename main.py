import pygame, sys

size = width, height = 1024, 512

class Ball:
    def __init__(self, model):
        self.model = model
        self.model = pygame.transform.scale(self.model, (64, 64))
        self.transform = self.model.get_rect()
        self.speed = [1,1]

    def move(self):
        self.transform = self.transform.move(self.speed)
        if self.transform.left < 0 or self.transform.right > width:
            self.speed[0] = -self.speed[0]
        if self.transform.top < 0 or self.transform.bottom > height:
            self.speed[1] = -self.speed[1]

class Player:
    def __init__(self, model):
        self.model = model
        self.model = pygame.transform.scale(self.model, (64, 64))
        self.model = self.model.get_rect()



def main():
    pygame.init()
    size = width, height = 1024, 512
    black = 0,0,0
    speed = [1, 1]

    screen = pygame.display.set_mode(size)

    ball = Ball(pygame.image.load("ball.jpg"))
    player1 = Player(pygame.image.load("player.jpg"))
    player2 = Player(pygame.image.load("player.jpg"))

    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        
        ball.move()
        screen.fill(black)
        screen.blit(ball.model, ball.transform)
        pygame.display.flip()


    return
    

if __name__ == '__main__':
    main()