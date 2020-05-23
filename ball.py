import pygame
class Ball():
    def __init__(self, x, y, radius,  dir1, dir2 ):
        self.x = x
        self.y = y
        self.color = (0,0, 0 )
        self.radius = radius
        self.circle = (x, y, radius)
        self.vel = 7
        self.dir_x = dir1
        self.dir_y = dir2

    def draw(self, window):
        pygame.draw.circle(window, self.color,(self.x, self.y), self.radius)

    def update(self):
        self.circle = (self.x, self.y, self.radius)
    def move(self):
        self.x = self.x + (self.dir_x) * (self.vel)
        self.y = self.y + (self.dir_y) * (self.vel)
        if self.x<=0:
            self.dir_x = 1
        if self.x>= 500:
            self.dir_x = -1
        self.update()

    def collide(self, x, y, width, height):
        if (self.x > x) and(self.x < x+width) and (self.y > y) and (self.y < y+height):

            return True
        else:
            return False

