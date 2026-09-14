import pygame
import math

pygame.init()

width = 1000
height = 800
screen = pygame.display.set_mode([width, height])

fps = 60
timer = pygame.time.Clock()

gravity = 0.6
bounce_stop = 0.2

mouse_trajectory = []

class Ball:
    def __init__(self,x_pos, y_pos, radius, colour, mass, retention,y_speed, x_speed, id, friction):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.colour = colour
        self.mass = mass
        self. retention = retention
        self.y_speed = y_speed
        self.x_speed = x_speed
        self.id = id
        self.circle = ""
        self.selected = False
        self.friction = friction
        

    def draw(self):
        self.circle = pygame.draw.circle(screen, self.colour, (self.x_pos,self.y_pos), self.radius)

    def gravity_check(self):
        if not self.selected:    
            if self.y_pos < self.radius and self.y_speed < 0:
                self.y_pos = self.radius 
                self.y_speed *= -1 * self.retention

            if self.y_pos < height - self.radius:
                self.y_speed += gravity

            else:
                self.y_pos = height - self.radius

                if self.y_speed > bounce_stop:
                    self.y_speed = self.y_speed * -1 * self.retention
                else: 
                    if abs(self.y_speed) <= bounce_stop:
                        self.y_speed = 0
                
            if (self.x_pos < self.radius and self.x_speed < 0):
                self.x_pos = self.radius
                self.x_speed *= -1 * self.retention
                if abs(self.x_speed) < bounce_stop:
                    self.x_speed = 0

            elif (self.x_pos > width - self.radius and self.x_speed > 0):
                self.x_pos = width - self.radius
                self.x_speed *= -1 * self.retention
                if abs(self.x_speed) < bounce_stop:
                    self.x_speed = 0

            
            if self.y_speed == 0 and self.x_speed != 0:
                if self.x_speed >0:
                    self.x_speed -= self.friction
                elif self.x_speed < 0:
                    self.x_speed += self.friction
        else:
            self.x_speed = x_push
            self.y_speed = y_push  

        return self.y_speed
    
    def update_pos(self, mouse):

        if not self.selected:    
            self.y_pos += self.y_speed
            self.x_pos += self.x_speed

        else:
            self.x_pos = mouse[0]
            self.y_pos = mouse[1]


    def check_select(self, pos):
        
        self.selected = False
        if self.circle.collidepoint(pos):
            self.selected = True
        
        return self.selected

    
    def collision_check(self, ball_1, ball_2):
        
        dx = ball_1.x_pos - ball_2.x_pos
        dy = ball_1.y_pos - ball_2.y_pos

        cdist = math.sqrt(dx**2 + dy**2) #distance bettween the center of the two balls using distance formula

        r = ball_1.radius + ball_2.radius

        if cdist == 0:
            return

        if cdist < r:
            
            overlap = r - cdist
            
            xp = dx/cdist #we are finding the direction of the collision here by finding the unit vector
            yp = dy/cdist #it is a pixel of magnitude one that only points towards the direciton of collision
            
            ball_1.x_pos += xp*(overlap/2)
            ball_1.y_pos += yp*(overlap/2)

            ball_2.x_pos -= xp*(overlap/2)
            ball_2.y_pos -= yp*(overlap/2)

            re_x = ball_1.x_speed - ball_2.x_speed
            re_y = ball_1.y_speed - ball_2.y_speed#relative velocity

            v_uvector = (re_x * xp) + (re_y * yp)
            #here we are finding the dot product of the relative velocity with unit vector to find out what the speed along the line of collision is
            
            if v_uvector > 0:
                return
            
            e = min(ball_1.retention, ball_2.retention)

            m1 = 1/(ball_1.mass)
            m2 = 1/(ball_2.mass)

            m1 = 0 if ball_1.selected else (1 / ball_1.mass)
            m2 = 0 if ball_2.selected else (1 / ball_2.mass)
            
            if m1 + m2 == 0:
                return
            
            re_m = m1 + m2 

            impulse = (1 + e) * abs(v_uvector) / re_m

            ball_1.x_speed += (impulse * m1) * xp
            ball_1.y_speed += (impulse * m1) * yp

            ball_2.x_speed -= (impulse * m2) * xp
            ball_2.y_speed -= (impulse * m2) * yp
            
            




        


def calc_motion_vector():

    x_speed = 0
    y_speed = 0

    if len(mouse_trajectory) > 19:
        x_speed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0])/len(mouse_trajectory)
        y_speed = (mouse_trajectory[-1][1] - mouse_trajectory[0][1])/len(mouse_trajectory)

    return x_speed, y_speed


ball1 = Ball(50, 50, 35, 'red', 100, 0.9, 0, 0, 1, 0.02)
ball2 = Ball(500, 500, 50, 'blue', 300, 0.8, 0, 0, 2, 0.03)
ball3 = Ball(200, 200, 20, 'purple', 200, 0.92, 0, 0, 3, 0.04)
ball4 = Ball(600, 600, 40, 'pink', 150, 0.86, 0, 0, 4, 0.026)
balls = [ball1,ball2,ball3,ball4]


run = True
while run:
    timer.tick(fps)
    screen.fill('black')

    mouse_coords = pygame.mouse.get_pos()
    mouse_trajectory.append(mouse_coords)

    if len(mouse_trajectory) > 20:
        mouse_trajectory.pop(0)
    x_push, y_push = calc_motion_vector()

    for b in balls:
        b.draw()
        b.y_speed = b.gravity_check()
        b.update_pos(mouse_coords)

    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            balls[i].collision_check(balls[i], balls[j])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if ball1.check_select(event.pos) or ball2.check_select(event.pos) or ball3.check_select(event.pos) or ball4.check_select(event.pos):
                    active_select = True
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_select = False
                for i in range(len(balls)):
                    balls[i].check_select((-1000,-1000))

    pygame.display.flip()

pygame.quit()