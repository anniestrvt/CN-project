import pygame
from network import Network
from ball import Ball
import sys
width = 500
height = 550
#pygame.init()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


pygame.font.init()

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 8
        self.num = 0
        if ( self.y> 300):
            self.num = 1

    def draw(self, win):
        # surf = pygame.Surface((self.width, self.height))
        # image = pygame.image.load('tennis2.png')
        # surf.blit(image,   (0,0))
        # pygame.display.update()
        # win.blit(surf, (self.x, self.y))
        pygame.draw.rect(win, self.color, self.rect)


    def move(self):
        keys = pygame.key.get_pressed()
        if self.num == 0:
            #ограничен полем по y от 50 до 300
            if keys[pygame.K_LEFT] and self.x>-self.width/2:
                self.x -= self.vel

            if keys[pygame.K_RIGHT] and self.x<width-(self.width/2):
                self.x += self.vel

            if keys[pygame.K_UP] and self.y>(50-self.height/2) :
                self.y -= self.vel

            if keys[pygame.K_DOWN]and self.y<300-(self.height):
                self.y += self.vel
        else:
            #ограничен полем по y от 300 до 550
            if keys[pygame.K_LEFT] and self.x > -self.width / 2:
                self.x -= self.vel

            if keys[pygame.K_RIGHT] and self.x < width - (self.width / 2):
                self.x += self.vel

            if keys[pygame.K_UP] and self.y > 300 :
                self.y -= self.vel

            if keys[pygame.K_DOWN] and self.y < 550 - (self.height / 2):
                self.y += self.vel


        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

def redraw_waiting_window(win):
    win.fill((0, 0, 0))
    font = pygame.font.SysFont("comicsans", 30)
    text = font.render("Waiting for the second player....", 1, (0, 255, 255))
    win.blit(text, (100, 200))
    text1 = font.render("You will be green player", 1, (0, 255, 255))
    win.blit(text1, (150, 350))
    pygame.display.update()
def redraw_main_window(win, player, player2, ball, count1, count2):
    win.fill((255, 255, 255))
    pygame.draw.line(win, (0, 0, 0), (0, 50), (500, 50), 3)
    pygame.draw.line(win, (0, 0, 0), (0, 300), (500, 300), 3)
    font = pygame.font.SysFont("comicsans", 50)
    t = "Count:"+str(count1)+":"+str(count2)
    text = font.render(t, 1, (0, 0, 255))
    win.blit(text, (150, 0))
    player.draw(win)
    player2.draw(win)
    ball.draw(win)
    pygame.display.update()



def read_pos(str):

    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2])


def make_pos(tup, ind1):
    return str(tup[0]) + "," + str(tup[1])+","+str(ind1)
def read_mes(str):
    str1 = str.split(",")
    return str1

def final(win,count1, count2,pos):
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((0, 0, 0))
        t = ""
        if count1 > count2:
            if pos < 300:
                t = "You lost!!!"
            else:
                t = "You won!!!"
            if count1<6:
                count1 = 6
        if count2 > count1:
            if pos < 300:
                t = "You won!!!"
            else:
                t = "You lost!!!"
            if count2<6:
                count2 = 6

        font = pygame.font.SysFont("comicsans", 30)
        text = font.render(t, 1, (0, 255, 255))
        win.blit(text, (200, 200))
        t1 = "Count: "+str(count1)+':'+str(count2)
        text1 = font.render(t1, 1, (0, 255, 255))
        win.blit(text1, (180, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                pygame.quit()


def main():
    count1=0
    count2 = 0
    n = Network()
    k = n.getP()
    pos = k.split(',')
    p = Player(int(pos[0]), int(pos[1]), 50, 50, (0, 255, 0))
    p2 = Player(int(pos[2]), int(pos[3]), 50, 50, (255, 0, 0))
    b= Ball(250, 250, 10, 1, 1)
    clock = pygame.time.Clock()
    run = True
    game_started=False
    k = n.send("clicked")
    game_finished = False
    while run:

        if game_started == False:
            k = n.send(str(1))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
            if k == "wait":
                redraw_waiting_window(win)
            elif k == "Y":
                game_started = True
                print("Yeeeesssss")
        else:
            clock.tick(40)
            keys = pygame.key.get_pressed()
            my_ind_1=0
            if keys[pygame.K_SPACE] and b.collide(p.x, p.y, p.width, p.height):

                my_ind_1=1
                if b.dir_y == 1:
                    b.dir_y = -1
                elif b.dir_y == -1:
                    b.dir_y = 1
            if b.y<=50 :
                count1+=1
                b.x=150
                b.y=525
                b.dir_x=1
                b.dir_y=-1
            if b.y>=550 :
                count2 += 1
                b.x=150
                b.y=65
                b.dir_x=1
                b.dir_y=1
            if count1>5 or count2>5:
                y = n . send("Finish")
                game_finished = True
                break
            else:
                try:
                    p2Pos_x, p2Pos_y, ind1= read_pos(n.send(make_pos((p.x, p.y), my_ind_1)))

                    if ind1 == 1 and b.dir_y==1:
                        b.dir_y = -1
                    elif ind1 == 1 and b.dir_y==-1:
                        b.dir_y = 1
                    p2.x = p2Pos_x
                    p2.y = p2Pos_y
                    p2.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                            y = n . send("Finish")

                            pygame.quit()
                            sys.exit()
                            break

                    b . move()
                    p.move()
                    redraw_main_window(win, p, p2, b, count1, count2)
                except:
                    break
    #if game_finished == True:

    final(win, count1, count2, int(pos[1]))

def menu():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        win.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()
menu()
