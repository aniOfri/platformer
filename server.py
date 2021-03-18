import socket
from platformer import Platformer
from _thread import *
import pickle

width = 500
height = 700

server = "0.0.0.0"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server started..")

connected = set()
games = {}
count = 0


def threaded_client(conn, p, game_id):
    global count
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if game_id in games:
                pfmr = games[game_id]

                if not data:
                    break
                else:
                    if data == "update":
                        pfmr.update(p)
                    elif "down" in data:
                        x = int(data[len(data) - 1])
                        pfmr.dir[p][x] = True
                    elif "up" in data:
                        x = int(data[len(data) - 1])
                        pfmr.dir[p][x] = False
                    elif data == "move":
                        pfmr.move(p)

                reply = pfmr
                conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("Lost connection..")
    try:
        del games[game_id]
        print("Closing game.. ", game_id)
    except:
        pass
    count -= 1
    conn.close()


while True:
    conn, address = s.accept()
    print("Connected to:", address)

    count += 1
    p = 0
    game_id = (count - 1) // 2
    if count % 2 == 1:
        games[game_id] = Platformer(game_id)
        print("Creating a new game...")
    else:
        games[game_id].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, game_id))
