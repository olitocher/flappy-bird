import time
import pygame
import os
import random

pygame.init()

FPS = 30
WIDTH, HEIGHT = 300, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
VEL = 4
pygame.display.set_caption('Flappy Bird')

comic_sans = pygame.font.SysFont('Comic Sans MS', 30)
BLACK = (0, 0, 0)

class Bird(object):
    bird_img = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bird1.png')), (30, 30))

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = self.y
        self.velocity = 0
        self.counter = 0

    def jump(self):
        self.velocity = -8
        self.counter = 0
        #height keeps track of where bird was before jump
        self.height = self.y

    def move(self):
        self.counter += 1

        d = self.velocity*self.counter + 1.5*self.counter**2

        #terminal velocity
        if d>= 16:
            d = 16

        if d < 0:
            d -= 2


        self.y = self.y + d

    def draw(self, WIN):
        WIN.blit(self.bird_img, (self.x, self.y))

    def mask(self):
        return pygame.mask.from_surface(self.bird_img)

class Pipe(object):
    pipe_img = pygame.image.load(os.path.join('assets', 'pipe.png'))
    top_pipe = pygame.transform.flip(pipe_img, False, True)
    gap = 150

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.top = y - self.gap - self.top_pipe.get_height()
        self.velocity = VEL

    def move(self):
        self.x -= self.velocity

    def draw(self, WIN):
        WIN.blit(self.pipe_img, (self.x, self.y))
        WIN.blit(self.top_pipe, (self.x, self.top))

    def collide(self, bird):
        bird_mask = bird.mask()
        top_mask = pygame.mask.from_surface(self.top_pipe)
        bottom_mask = pygame.mask.from_surface(self.pipe_img)

        top_offset = int(self.x - bird.x), int(self.top - round(bird.y))
        bottom_offset = int(self.x - bird.x), int(self.y - round(bird.y))

        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_point = bird_mask.overlap(top_mask, top_offset)

        if top_point or bottom_point:
            return True

        return False

class Background:
    bg_load = pygame.image.load(os.path.join('assets', 'background.png'))
    bg = pygame.transform.scale(bg_load, (WIDTH, HEIGHT))
    width = bg.get_width()

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.width
        self.velocity = VEL

    def move(self):
        self.x1 -= self.velocity
        self.x2 -= self.velocity
        if self.x1 < self.width * - 1:
            self.x1 = self.width
        if self.x2 < self.width * - 1:
            self.x2 = self.width

    def draw(self, WIN):
        WIN.blit(self.bg, (self.x1, self.y))
        WIN.blit(self.bg, (self.x2, self.y))

clock = pygame.time.Clock()

def redraw_window(WIN, bird, pipes, background, score):
    background.draw(WIN)
    bird.draw(WIN)
    for pipe in pipes:
        pipe.draw(WIN)

    text = comic_sans.render(str(score), False, BLACK)
    WIN.blit(text, (WIDTH/2, 50))

    pygame.display.update()

def start(background, bird):

    text = comic_sans.render('Start Game', False, BLACK)

    start_screen = True

    while start_screen:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        background.draw(WIN)
        bird.draw(WIN)
        WIN.blit(text, (WIDTH / 3 - 20, 100))
        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            start_screen = False

def game_over(background):
    text = comic_sans.render('Game Over', False, BLACK)
    start_time = time.time()
    seconds = 2

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        background.draw(WIN)

        WIN.blit(text, (WIDTH/4, 100))

        pygame.display.update()

        if elapsed_time > seconds:
            break

def main():
    background = Background(0)
    bird = Bird(150, 200)

    first_pipe = Pipe(WIDTH, HEIGHT/2)
    pipes = [first_pipe]

    start(background, bird)

    score = 0

    checked = False

    run = True
    while run:

        clock.tick(FPS)
        background.move()
        bird.move()
        redraw_window(WIN, bird, pipes, background, score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird):
                game_over(background)
                run = False

        rand_y = random.randint(HEIGHT-Pipe.pipe_img.get_height(), Pipe.pipe_img.get_height() + Pipe.gap)


        if pipes[-1].x < WIDTH/5:
            pipes.append(Pipe(WIDTH, rand_y))
            checked = False

        if not checked:
            if pipes[-1].x < bird.x:
                score += 1
                checked = True

        #key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bird.jump()

    main()

if __name__ == '__main__':
    main()