import socket
from _thread import *
import sys
from game import Game
server = "192.168.1.67"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    str(e)
s.listen(2)
print("Waiting for a connection, Server Started")
connected = set()
games = {}
idCount = 0
pos = {(150, 150), (350, 350)}
def create_mes(tup):
    st=str(tup[0])
    for i in range(1, len(tup)):
        st+=","
        st+=str(tup[i])
    return st

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2])


def make_pos(tup, ind):
    return str(tup[0]) + "," + str(tup[1])+","+str(ind)

pos = [(250,50),(250,480)]
ball_pos = (250,250)
ind = [0,0]
interrupt = False

def threaded_client(conn, p, gameId):
    
    if p == 0:
        conn.send(str.encode(str(pos[0][0])+','+str(pos[0][1])+','+str(pos[1][0])+','+str(pos[1][1])))
    else:
        conn.send(str.encode(str(pos[1][0])+','+str(pos[1][1])+','+str(pos[0][0])+','+str(pos[0][1])))

    started = False
    while True:

        try:
            mes= conn.recv(2048).decode()
            if gameId in games:
                if started == False:
                    if games[gameId].start1 == True and games[gameId].start2 == True:
                        print("The game will start")
                        conn.send(str.encode("Y"))
                        started = True
                    else:
                        conn.send(str.encode("wait"))
                        if mes == "clicked" and p == 0:
                            games[gameId].start1 = True
                        if mes == "clicked" and p == 1:
                            games[gameId].start2 = True
                else:
                    if mes == "Finish":
                        break
                    else:
                        pos_x, pos_y, ind_mes = read_pos(mes)
                        pos[p] = (pos_x, pos_y)
                        ind[p] = ind_mes
                        if not mes:
                            print("Disconnected")
                            break
                        else:
                            if p == 1:
                                reply1 = pos[0]
                                reply2 = ind[0]
                            else:
                                reply1 = pos[1]
                                reply2 = ind[1]

                        conn.sendall(str.encode(make_pos(reply1, reply2)))
            else:
                break



        except:
            pass

    print("Game is finished")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount+=1
    p = 0
    gameId = (idCount - 1)//2
    print(gameId)
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1
    start_new_thread(threaded_client, (conn, p, gameId))


