import pygame
import math
import random
import csv

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
    def __init__(self,x_pos, y_pos, radius, mass, retention,y_speed, x_speed, friction):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.mass = mass
        self.retention = retention
        self.y_speed = y_speed
        self.x_speed = x_speed
        self.friction = friction
        


    def gravity_check(self):    
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
                self.x_speed = max(0, self.x_speed - self.friction) #brings the ball to a stop if value is negative
            elif self.x_speed < 0:
                self.x_speed += self.friction
        
        self.y_pos += self.y_speed
        self.x_pos += self.x_speed

        return self.y_speed
        
    
    def collision_check(self, ball_1, ball_2):
        
        dx = ball_1.x_pos - ball_2.x_pos
        dy = ball_1.y_pos - ball_2.y_pos

        cdist = math.sqrt(dx**2 + dy**2) #distance bettween the center of the two balls using distance formula

        r = ball_1.radius + ball_2.radius

        if cdist == 0:
            return False

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
                return False
            
            e = min(ball_1.retention, ball_2.retention)

            m1 = 1/(ball_1.mass)
            m2 = 1/(ball_2.mass)
            
            if m1 + m2 == 0:
                return False
            
            re_m = m1 + m2 

            impulse = (1 + e) * abs(v_uvector) / re_m

            ball_1.x_speed += (impulse * m1) * xp
            ball_1.y_speed += (impulse * m1) * yp

            ball_2.x_speed -= (impulse * m2) * xp
            ball_2.y_speed -= (impulse * m2) * yp
            
            return True
        
        return False

      
    
    
def random_ball_gen():
    
    radius = random.uniform(10.0, 50.0)
    mass = math.pi * (radius ** 2) 
    
    x_pos = random.uniform(radius, width - radius)
    y_pos = random.uniform(radius, height - radius)
    
    x_speed = random.uniform(-15.0, 15.0)
    y_speed = random.uniform(-15.0, 15.0)
    
    retention = random.uniform(0.5, 1.0) 
    friction = random.uniform(0.01, 0.05)
    

    return Ball(x_pos, y_pos, radius, mass, retention, y_speed, x_speed, friction)


def validity_check():

    ball_1 = random_ball_gen()
    ball_2 = random_ball_gen()

    while True:
            dx = ball_1.x_pos - ball_2.x_pos
            dy = ball_1.y_pos - ball_2.y_pos

            cdist = math.sqrt(dx**2 + dy**2)

            r = ball_1.radius + ball_2.radius

            if cdist<r:
                ball_2 = random_ball_gen()
            
            else:
                return ball_1, ball_2


def data_generator(num_samples = 1000, filename = "data.csv"):

    print("Generating the simulations\n")
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "b1_mass", "b2_mass", "b1_x", "b1_y", "b2_x", "b2_y", 
            "b1_vx_in", "b1_vy_in", "b2_vx_in", "b2_vy_in", 
            "b1_vx_out", "b1_vy_out", "b2_vx_out", "b2_vy_out" 
        ])

        count = 0

        while (count<num_samples):
            b1 , b2 = validity_check()
            collision_happened = False
            timeout = 0

            while not collision_happened and timeout < 500:

                    b1.gravity_check()
                    b2.gravity_check()


                    b1_vx_pre, b1_vy_pre = b1.x_speed, b1.y_speed
                    b2_vx_pre, b2_vy_pre = b2.x_speed, b2.y_speed
                    
                    
                    
                    if b1.collision_check(b1, b2):
                        writer.writerow([
                            b1.mass, b2.mass, b1.x_pos, b1.y_pos, b2.x_pos, b2.y_pos,
                            b1_vx_pre, b1_vy_pre, b2_vx_pre, b2_vy_pre,
                            b1.x_speed, b1.y_speed, b2.x_speed, b2.y_speed
                        ])
                        count += 1
                        collision_happened = True
                    
                    timeout += 1
        print("Done")

if __name__ == "__main__":
    data_generator(50000)