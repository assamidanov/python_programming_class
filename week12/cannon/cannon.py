import math
import pygame

import random as rnd

from my_colors import *

FPS = 20
GRAVITY_ACCELERATION = 9.8  # Gravitational acceleration for the projectile.
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class Cannon:
    max_velocity = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shell_num = None  #todo - the remaining number of projectiles at the moment
        self.direction = math.pi / 4

    def aim(self, x, y):
        """
        Changes the direction so that it points from the point (self.x, self.y) to the point (x, y).
        :param x: x-coordinate we are aiming at
        :param y: y-coordinate we are aiming at
        :return: None
        """
        pass  #todo

    def fire(self, dt):
        """
        Creates a projectile object (if not all projectiles are used up) 
        flying in the direction of the angle with a velocity depending 
        on the duration of the mouse click.
        :param dt: duration of the mouse click, ms
        :return: an instance of a projectile of type Shell
        """
        pass

    def draw(self):
        pygame.draw.circle(screen, self.color,
                           (int(round(self.x)), int(round(self.y))), self.r)


class Shell:
    standard_radius = 25

    def __init__(self, x, y, Vx, Vy):
        self.x, self.y = x, y
        self.Vx, self.Vy = Vx, Vy
        self.r = Shell.standard_radius

    def move(self, dt):
        """
        Moves the projectile based on its kinematic 
        characteristics and the length of the time 
        quantum dt to a new position, and also changes its velocity.
        :param dt:
        :return:
        """
        ax, ay = 0, GRAVITY_ACCELERATION
        self.x += self.Vx*dt + ax*(dt**2)/2
        self.y += self.Vy*dt + ay*(dt**2)/2
        self.Vx += ax*dt
        self.Vy += ay*dt
        # TODO: Destroy (in the status deleted) the projectile when it touches the ground.

    def draw(self):
        pygame.draw.circle(screen, self.color,
                           (int(round(self.x)), int(round(self.y))), self.r)

    def detect_collision(self, other):
        """
        Checks the fact of contact between the projectile and the other object.
        :param other: an object that should have fields x, y, r
        :return: a boolean value of type bool
        """
        length = ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
        return length <= self.r + other.r


class Target:
    standard_radius = 15

    def __init__(self, x, y, Vx, Vy):
        self.x, self.y = x, y
        self.Vx, self.Vy = Vx, Vy
        self.r = Target.standard_radius
        self.color = COLORS[rnd.randint(0, len(COLORS) - 1)]

    def move(self, dt):
        """
         Moves the target ball based on its kinematic characteristics 
         and the length of the time quantum dt to a new position, and 
         also changes its velocity
        :param dt:
            :return:
        """
        ax, ay = 0, GRAVITY_ACCELERATION
        self.x += self.Vx * dt
        self.y += self.Vy * dt
        self.Vx += ax * dt
        self.Vy += ay * dt
        #todo: Target balls should bounce off the walls.

    def draw(self):
        pygame.draw.circle(screen, self.color,
                           (int(round(self.x)), int(round(self.y))), self.r)

    def collide(self, other):
        """
         Calculation of absolutely elastic collision
        :param other:
        :return:
        """
        pass  #todo

class Bomb:
    pass

def generate_random_targets(number: int):
    targets = []
    for i in range(number):
        x = rnd.randint(0, SCREEN_HEIGHT)
        y = rnd.randint(0, SCREEN_HEIGHT)
        Vx = rnd.randint(-30, +30)
        Vy = rnd.randint(-30, +30)
        target = Target(x, y, Vx, Vy)
        targets.append(target)
    return targets


def game_main_loop():

    targets = generate_random_targets(10)

    clock = pygame.time.Clock()
    finished = False

    while not finished:
        dt = clock.tick(FPS) / 1000
        print(dt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print('Click!')

        pygame.display.update()
        screen.fill(GRAY)

        for target in targets:
            target.move(dt)

        for target in targets:
            target.draw()

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.update()

    game_main_loop()