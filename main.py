import random
import pygame
from pygame.locals import *
import time

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (5, 9, 38)
RED = (200, 0, 0)
SIZE = 40


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.png").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, WIDTH / SIZE - 1) * SIZE
        self.y = random.randint(0, HEIGHT / SIZE - 1) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'right'
        self.length = length
        self.x = [SIZE] * length
        self.y = [SIZE] * length

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_right(self):
        self.direction = 'right'

    def move_left(self):
        self.direction = 'left'

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        self.parent_screen.fill(BLUE)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.mixer.init()
        self.play_bg_music()
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play_bg_music(self):
        pygame.mixer.music.load("resources/bg_music.wav")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("bite_sound.mp3")
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("hiss.wav")
                raise "Game Over"

        # snake colliding with border
        if not (0 <= self.snake.x[0] <= WIDTH and 0 <= self.snake.y[0] <= HEIGHT):
            self.play_sound("crash.mp3")
            raise "Game Over"

    def show_game_over(self):
        self.surface.fill(BLUE)
        font = pygame.font.SysFont("monospace", 70, "bold")
        line1 = font.render(f"Game over!", True, RED)
        self.surface.blit(line1, (WIDTH / 4.3, HEIGHT / 3))
        font = pygame.font.SysFont("monospace", 20)
        line2 = font.render(f"Your score is : {self.snake.length}", True, WHITE)
        self.surface.blit(line2, (WIDTH / 2.8, HEIGHT / 2))
        line3 = font.render(f"To play again press Enter, To exit press Escape!", True, WHITE)
        self.surface.blit(line3, (WIDTH / 6.5, HEIGHT / 1.8))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def display_score(self):
        font = pygame.font.SysFont("monospace", 20)
        score = font.render(f"score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (WIDTH - 150, 10))

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_LEFT:
                            self.snake.move_left()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.15)


if __name__ == "__main__":
    game = Game()
    game.run()
