import numpy as np
import pygame as pg
import math
from random import randint, gauss

pg.init()
pg.font.init()

font = pg.font.SysFont("Arial", 40)

WHITE = (255, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SCREEN_SIZE = (800, 600)


def rand_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))


class GameObject:

    def move(self):
        pass

    def draw(self, screen):
        pass


class Shell(GameObject):
    '''
    The ball class. Creates a ball, controls it's movement and implement it's rendering.
    '''

    def __init__(self, coord, vel, rad=20, color=None):
        '''
        Constructor method. Initializes ball's parameters and initial values.
        '''
        self.coord = coord
        self.vel = vel
        if color == None:
            color = rand_color()
        self.color = color
        self.rad = rad
        self.is_alive = True

    def check_corners(self, refl_ort=0.8, refl_par=0.9):
        '''
        Reflects ball's velocity when ball bumps into the screen corners. Implemetns inelastic rebounce.
        '''
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1-i] = int(self.vel[1-i] * refl_par)
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1-i] = int(self.vel[1-i] * refl_par)

    def move(self, time=1, grav=0):
        '''
        Moves the ball according to it's velocity and time step.
        Changes the ball's velocity due to gravitational force.
        '''
        self.vel[1] += grav
        for i in range(2):
            self.coord[i] += time * self.vel[i]
        self.check_corners()
        if self.vel[0]**2 + self.vel[1]**2 < 2**2 and self.coord[1] > SCREEN_SIZE[1] - 2*self.rad:
            self.is_alive = False

    def draw(self, screen):
        '''
        Draws the ball on appropriate surface.
        '''
        pg.draw.circle(screen, self.color, self.coord, self.rad)

class RectangleProjectile(GameObject):
    '''
    The rectangle class. Creates a rectangle, controls it's movement and implement it's rendering.
    '''

    def __init__(self, coord, vel, height=20, width=30, color=None):
        '''
        Constructor method. Initializes rectangle's parameters and initial values.
        '''
        self.coord = coord
        self.vel = vel
        if color == None:
            color = rand_color()
        self.color = color
        self.height = height
        self.width = width
        self.is_alive = True

    def check_corners(self, refl_ort=0.8, refl_par=0.9):
        '''
        Reflects rectangle's velocity when rectangle bumps into the screen corners. Implements inelastic rebounce.
        '''
        for i in range(2):
            if self.coord[i] < self.height:
                self.coord[i] = self.height
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1-i] = int(self.vel[1-i] * refl_par)
            elif self.coord[i] > SCREEN_SIZE[i] - self.height:
                self.coord[i] = SCREEN_SIZE[i] - self.height
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1-i] = int(self.vel[1-i] * refl_par)
        for i in range(2):
            if self.coord[i] < self.width:
                self.coord[i] = self.width
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1-i] = int(self.vel[1-i] * refl_par)
            elif self.coord[i] > SCREEN_SIZE[i] - self.width:
                self.coord[i] = SCREEN_SIZE[i] - self.width
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1-i] = int(self.vel[1-i] * refl_par)

    def move(self, time=1, grav=0):
        '''
        Moves the rectangle according to it's velocity and time step.
        Changes the rectangle's velocity due to gravitational force.
        '''
        self.vel[1] += grav
        for i in range(2):
            self.coord[i] += time * self.vel[i]
        self.check_corners()
        if self.vel[0]**2 + self.vel[1]**2 < 2**2 and self.coord[1] > SCREEN_SIZE[1] - 2*self.height:
            self.is_alive = False
        self.check_corners()
        if self.vel[0]**2 + self.vel[1]**2 < 2**2 and self.coord[1] > SCREEN_SIZE[1] - 2*self.width:
            self.is_alive = False

    def draw(self, screen):
        '''
        Draws the rectangle on appropriate surface.
        '''
        pg.draw.rect(screen, self.color, self.coord, self.height, self.width)


class Cannon(GameObject):
    '''
    Cannon class. Manages it's renderring, movement and striking.
    '''

    def __init__(self, coord, angle, max_pow, min_pow, color):
        '''
        Constructor method. Sets coordinate, direction, minimum and maximum power and color of the gun.
        '''
        self.coord = coord
        self.angle = angle
        self.max_pow = max_pow
        self.min_pow = min_pow
        self.color = color
        self.active = False
        self.pow = min_pow

    def activate(self):
        '''
        Activates gun's charge.
        '''
        self.active = True

    def gain(self, inc=2):
        '''
        Increases current gun charge power.
        '''
        if self.active and self.pow < self.max_pow:
            self.pow += inc

    def strike(self):
        '''
        Creates ball and rectangle, according to gun's direction and current charge power.
        '''
        vel = self.pow
        angle = self.angle
        ball = Shell(list(self.coord), [
                     int(vel * np.cos(angle)), int(vel * np.sin(angle))])
        rectangle = RectangleProjectile(list(self.coord), [
                     int(vel * np.cos(angle)), int(vel * np.sin(angle))])
        self.pow = self.min_pow
        self.active = False
        return ball or rectangle

    def set_angle(self, target_pos):
        '''
        Sets gun's direction to target position.
        '''
        self.angle = np.arctan2(
            target_pos[1] - self.coord[1], target_pos[0] - self.coord[0])

    # handle y movement of cannons
    def move_y_coord(self, inc):
        '''
        Changes vertical position of the gun.
        '''
        if (self.coord[1] > 30 or inc > 0) and (self.coord[1] < SCREEN_SIZE[1] - 30 or inc < 0):
            self.coord[1] += inc
    # handle x movement of cannons
    def move_x_coord(self, inc):
        '''
        Changes horizontal position of the gun.
        '''
        if (self.coord[0] - inc > 0 or inc > 0) and (self.coord[0] < SCREEN_SIZE[0] + inc or inc < 0):
            self.coord[0] += inc
            
    # handle collisions from ball to cannon
    def check_collision(self, ball):
        """
        Checks whether the cannon collides with a ball.
        """
        x_collision = self.coord[0] - ball.rad <= ball.coord[0] <= self.coord[0] + self.coord[0]
        y_collision = self.coord[1] - ball.rad <= ball.coord[1] <= self.coord[1] + self.coord[1]
        return x_collision and y_collision

    def draw(self, screen):
        '''
        Draws the gun on the screen.
        '''
        gun_shape = []
        vec_1 = np.array([int(5*np.cos(self.angle - np.pi/2)),
                         int(5*np.sin(self.angle - np.pi/2))])
        vec_2 = np.array([int(self.pow*np.cos(self.angle)),
                         int(self.pow*np.sin(self.angle))])
        gun_pos = np.array(self.coord)
        gun_shape.append((gun_pos + vec_1).tolist())
        gun_shape.append((gun_pos + vec_1 + vec_2).tolist())
        gun_shape.append((gun_pos + vec_2 - vec_1).tolist())
        gun_shape.append((gun_pos - vec_1).tolist())
        pg.draw.polygon(screen, self.color, gun_shape)
        

'''
This is the original code. However, the class name has changed as there will be more 
targets. Changing the class name will allow for more differntiation and will make it easier 
to program other targets. 
'''
class Circle_Target(GameObject):
    '''
    Target class. Creates target, manages it's rendering and collision with a ball event.
    '''
    def __init__(self, coord=None, color=None, rad=30):
        '''
        Constructor method. Sets coordinate, color and radius of the target.
        '''
        if coord == None:
            coord = [randint(rad, SCREEN_SIZE[0] - rad), randint(rad, SCREEN_SIZE[1] - rad)]
        self.coord = coord
        self.rad = rad

        if color == None:
            color = rand_color()
        self.color = color

    def check_collision(self, ball):
        '''
        Checks whether the ball bumps into target.
        '''
        dist = sum([(self.coord[i] - ball.coord[i])**2 for i in range(2)])**0.5
        min_dist = self.rad + ball.rad
        return dist <= min_dist

    def draw(self, screen):
        '''
        Draws the target on the screen
        '''
        pg.draw.circle(screen, self.color, self.coord, self.rad)

    def move(self):
        """
        This type of target can't move at all.
        :return: None
        """
        pass

'''
Creating rectangular targets. This class will have a standardized color and the target
will constantly be moving, unless hit by projectile. The color of this target will be WHITE to differentiate
itself from the other targets.
'''

class Rect_Target(GameObject):
    '''
    Rectangle Target class. Creates rectangular target, manages it's rendering and collision with a ball event.
    '''
    def __init__(self, coord=None, color=None, width=60, height=30):
        if coord is None:
            coord = [randint(width, SCREEN_SIZE[0] - width), randint(height, SCREEN_SIZE[1] - height)]
        self.coord = coord
        self.width = width
        self.height = height

        if color == None:
            color = rand_color()
        self.color = color

    def check_collision(self, ball):
        '''
        Checks whether the ball bumps into rectangular target.
        '''
        if isinstance(ball, Shell):
            ball_pos = np.array(ball.coord)
            closest_point = np.clip(ball_pos, self.coord - np.array([self.width / 2, self.height / 2]), self.coord + np.array([self.width / 2, self.height / 2]))
            distance = np.linalg.norm(ball_pos - closest_point)
            return distance <= ball.rad
        return False
        
    def draw(self, screen):
        '''
        Draws the target on the screen
        '''
        pg.draw.rect(screen, WHITE, (self.coord[0] - self.width / 2, self.coord[1] - self.height / 2, self.width, self.height))

    def move(self):
        """
        This type of target can't move at all.
        :return: None
        """
        pass

'''
Creating a triangular target that will make it difficult to hit the other targets. Additionally, it will
also make it slightly more easier to hit them as well. The goal is for the projectiles to bounce off/on the 
triangle. The player can use the triangle to reach other targets. Along with this, the triangle's movement will
be in a circular motion which will be implemented in the moving target class. 
'''

class Triangular_Target(GameObject):
    '''
    Target class. Creates triangular target, manages it's rendering and collision with a ball event.
    '''
    def __init__(self, coord=None, color=None, rad=30):
        '''
        Constructor method. Sets coordinate, color and radius of the target.
        '''
        if coord == None:
            coord = [randint(100, SCREEN_SIZE[0]-100), randint(100, SCREEN_SIZE[1]-100)]
        self.coord = coord
        if color == None:
            color = rand_color()
        self.color = color
        self.rad = rad
        self.exists = True

    def check_collision(self, ball):
        '''
        Checks if ball collides with the triangular target. Implements elastic collision.
        '''
        dist = np.sqrt((ball.coord[0] - self.coord[0])**2 + (ball.coord[1] - self.coord[1])**2)
        if dist < self.rad + ball.rad:
            norm_vec = np.array([self.coord[0] - ball.coord[0], self.coord[1] - ball.coord[1]])
            tang_vec = np.array([-norm_vec[1], norm_vec[0]])
            ball_vel = np.array(ball.vel)
            ball_vel_norm = np.dot(norm_vec, ball_vel) / np.linalg.norm(norm_vec)
            ball_vel_tang = np.dot(tang_vec, ball_vel) / np.linalg.norm(tang_vec)
            ball_vel_norm_new = - ball_vel_norm
            ball_vel_new = ball_vel_norm_new * norm_vec / np.linalg.norm(norm_vec) + ball_vel_tang * tang_vec / np.linalg.norm(tang_vec)
            ball.vel = ball_vel_new.astype(int)

    def draw(self, screen):
        '''
        Draws the target on the screen.
        '''
        if self.exists:
            vertices = [(self.coord[0], self.coord[1] - self.rad), 
                 (self.coord[0] - self.rad, self.coord[1] + self.rad), 
                 
                 (self.coord[0] + self.rad, self.coord[1] + self.rad)]
        pg.draw.polygon(screen, self.color, vertices)



#These classes will control the movements of the targets.
class MovingTargets_Circle(Circle_Target):
     def __init__(self, coord=None, color=None, rad=30):
         super().__init__(coord, color, rad)
         self.vx = randint(-2, +2)
         self.vy = randint(-2, +2)
    
     def move(self):
         self.coord[0] += self.vx
         self.coord[1] += self.vy

#controls the moving rectangles. Will also bounce off of the screen, similar to the projectiles. 
class MovingTargets_Rect(Rect_Target):
     def __init__(self, coord=None, color=None, rad=30):
         super().__init__(coord, color, rad)
         self.vx = randint(-2, +2)
         self.vy = randint(-2, +2)
    
     def move(self):
        self.coord[0] += self.vx
        self.coord[1] += self.vy

        '''
        This set of if statements are used to control the motion of the target. It will match its 
        coordinates to those of the screen's edges and corners so that when it reaches it, it will
        bounce off instead of falling off the screen. 
        '''
        if self.coord[0] < self.width / 2 or self.coord[0] > SCREEN_SIZE[0] - self.width / 2:
            self.vx = -self.vx
        if self.coord[1] < self.height / 2 or self.coord[1] > SCREEN_SIZE[1] - self.height / 2:
            self.vy = -self.vy
            
        '''
        COMMENT AND UNCOMMENT AS NEEDED - BUGGY CODE
        '''
        # # Draw the circle dropped from the target
        # # Position below the target
        # circle_pos = (self.coord[0], self.coord[1] + self.rad + 10)
        # circle_radius = 5  # Radius of the circle
        # circle_color = (255, 0, 0)  # Color of the circle (red)
        # pg.draw.circle(screen, circle_color, circle_pos, circle_radius)
        '''
        END BUGGY CODE
        '''

'''
Controls the movement of the triangular target. This target differs from the other targets as
it follows a circular motion. This is implemented using cos and sin functions that follow the 
motions of a circle.
'''
class MovingTargets_Tri(Triangular_Target):
    def __init__(self, coord=None, color=None, rad=30, radius=100, speed=0.05):
        super().__init__(coord, color, rad)
        self.radius = radius
        self.angle = 0
        self.speed = speed

    def move(self):
        self.coord[0] = self.radius * np.cos(self.angle) + SCREEN_SIZE[0] // 2
        self.coord[1] = self.radius * np.sin(self.angle) + SCREEN_SIZE[1] // 2
        self.angle += self.speed

class ScoreTable:
    '''
    Score table class.
    '''

    def __init__(self, t_destr=0, b_used=0):
        self.t_destr = t_destr
        self.b_used = b_used
        self.font = pg.font.SysFont("dejavusansmono", 25)

    def score(self):
        '''
        Score calculation method.
        '''
        return self.t_destr - self.b_used

    def draw(self, screen):
        score_surf = []
        score_surf.append(self.font.render(
            "Destroyed: {}".format(self.t_destr), True, WHITE))
        score_surf.append(self.font.render(
            "Balls used: {}".format(self.b_used), True, WHITE))
        score_surf.append(self.font.render(
            "Total: {}".format(self.score()), True, RED))
        for i in range(3):
            screen.blit(score_surf[i], [310, 10 + 30*i])


class Manager:
    '''
    Class that manages events' handling, ball's motion and collision, target creation, etc.
    '''

    def __init__(self, n_targets=1):
        self.balls = []
        # create losing bool and losing_timer num
        self.losing = False
        self.losing_timer = None
        # create player and enemy cannon
        self.player = Cannon([30, SCREEN_SIZE[1]//2],
                             angle=0, max_pow=50, min_pow=10, color=RED)
        self.enemy = Cannon([770, SCREEN_SIZE[1]//2],
                            angle=0, max_pow=50, min_pow=10, color=BLUE)
        self.targets = []
        self.score_t = ScoreTable()
        self.n_targets = n_targets
        self.new_mission()

    def new_mission(self):
        '''
        Adds new targets. Only 3 of the MovingTargets classes are used. This is because the only moving targets
        will be the moving circular targets provided by the original code, the white rectangles that will bounce
        off of the screen, and the triangle target that moves in a cirle. 
        '''
        for i in range(self.n_targets):
            #adds the moving circle, rectangle, and triangle targets into the game
            self.targets.append(MovingTargets_Circle(rad=randint(max(1, 30 - 2*max(0, self.score_t.score())),
                30 - max(0, self.score_t.score()))))
            self.targets.append(MovingTargets_Rect(coord=[randint(30, SCREEN_SIZE[0] - 30),
                 randint(30, SCREEN_SIZE[1] - 30)]))
            self.targets.append(MovingTargets_Tri(coord=[randint(30, SCREEN_SIZE[0] - 30),
                 randint(30, SCREEN_SIZE[1] - 30)]))

            #adds the still circle targets into the game
            self.targets.append(Circle_Target(rad=randint(max(1, 30 - 2*max(0, self.score_t.score())),
                 30 - max(0, self.score_t.score()))))
            
    # function for rendering loser screen
    def render_lose_text(self):
        text_surface = font.render("YOU LOSE!", True, RED)
        text_rect = text_surface.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
        screen.blit(text_surface, text_rect)

    def process(self, events, screen):
        '''
        Runs all necessary method for each iteration. Adds new targets, if previous are destroyed.
        '''
        done = self.handle_events(events)
        
        # if collide makes losing true
        if self.losing:
            # load in loser screen
            screen.fill(BLACK)
            self.render_lose_text()
            pg.display.update()
            
            # allow a 2 second timer for it to run before quitting the game
            if self.losing_timer is None:
                self.losing_timer = pg.time.get_ticks()
            if pg.time.get_ticks() - self.losing_timer >= 2000:
                return True
            
            return False

        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.player.set_angle(mouse_pos)

        self.move()
        self.collide()
        self.draw(screen)

        if len(self.targets) == 0 and len(self.balls) == 0:
            self.new_mission()

        return done

    def handle_events(self, events):
        '''
        Handles events from keyboard, mouse, etc.
        '''
        done = False

        # prep enemy tank
        self.enemy.set_angle([90,0])
        self.enemy.activate()
        self.enemy.gain()

        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.player.activate()
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.balls.append(self.player.strike())
                    self.score_t.b_used += 1
            # once the player shots, the enemy will too
            if event.type == pg.MOUSEBUTTONUP:
                    self.balls.append(self.enemy.strike())

        # player and enemy movement
        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_UP]:
            self.player.move_y_coord(-5)
            self.enemy.move_y_coord(-5)
        elif key_pressed[pg.K_DOWN]:
            self.player.move_y_coord(5)
            self.enemy.move_y_coord(5)
        elif key_pressed[pg.K_LEFT]:
            self.player.move_x_coord(-5)
        elif key_pressed[pg.K_RIGHT]:
            self.player.move_x_coord(5)

        return done

    def draw(self, screen):
        '''
        Runs balls', gun's, targets' and score table's drawing method.
        '''
        for ball in self.balls:
            ball.draw(screen)
        for target in self.targets:
            target.draw(screen)
        # draw player and enemy cannon
        self.player.draw(screen)
        self.enemy.draw(screen)
        
        self.score_t.draw(screen)

    def move(self):
        '''
        Runs balls' and gun's movement method, removes dead balls.
        '''
        dead_balls = []
        for i, ball in enumerate(self.balls):
            ball.move(grav=2)
            if not ball.is_alive:
                dead_balls.append(i)
        for i in reversed(dead_balls):
            self.balls.pop(i)
        for i, target in enumerate(self.targets):
            target.move()
        self.player.gain()

    def collide(self):
        '''
        Checks whether balls bump into targets, sets balls' alive trigger.
        '''
        collisions = []
        targets_c = []
        for i, ball in enumerate(self.balls):
            for j, target in enumerate(self.targets):
                if target.check_collision(ball):
                    collisions.append([i, j])
                    targets_c.append(j)
        targets_c.sort()
        for j in reversed(targets_c):
            self.score_t.t_destr += 1
            self.targets.pop(j)
            
        # Checks collisions between enemy's shells and player's cannon
        player_collisions = []
        player_cannon = self.player
        for i, ball in enumerate(self.balls):
            if player_cannon.check_collision(ball):
                player_collisions.append(i)
        
        # handle enemy cannon shell hitting player
        player_collisions.sort()
        for i in reversed(player_collisions):
            self.losing = True
            self.balls.pop(i)
            
        '''
        COMMENT AND UNCOMMENT AS NEEDED - BUGGY CODE
        '''
        # # check collision between player cannon and moving bomb target (MovingTarget)
        # for j, target in enumerate(self.targets):
        #     if player_cannon.check_collision(target):
        #         self.losing = True
        #         break
        '''
        END BUGGY CODE
        '''

screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("Cannon Game")

done = False
clock = pg.time.Clock()

mgr = Manager(n_targets=3)

while not done:
    clock.tick(15)
    screen.fill(BLACK)

    done = mgr.process(pg.event.get(), screen)

    pg.display.flip()


pg.quit()
