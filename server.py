import socket
import base64
import json
import random
import os


port = 8239

s = socket.socket()
s.bind(('', port))
print("Created server on this IP")

s.listen(5)
while True:
    # Establish connection with client.
    c, addr = s.accept()
    print('Got connection from', addr)

    # Recv data from client.
    if base64.decodebytes(c.recv(1024)).decode("utf-8") == "are you a counting game server?":
        c.sendall(base64.encodebytes(b"yes we are"))

        print("Starting game please wait.")
        # Start the game
        data = {"turn": "server",
                "data": [0, 1]}
        if random.randint(1, 2) == 2:
            data["turn"] = "client"
        c.sendall(base64.encodebytes(json.dumps(data).encode("utf-8")))
        while True:

            print("Waiting for enemy")
            if data["turn"] != "server":
                while True:
                    try:
                        data = json.loads(base64.decodebytes(c.recv(1024)).decode("utf-8"))
                        break
                    except:
                        pass
            print("Current data: " + str(data["data"][-1]))
            print("Enemy: " + str(data["data"][-1]) + " [+" + str(data["data"][-1] - data["data"][-2]) + "]")
            if data["data"][-1] >= 20:
                print("Unfortunately, The enemy wins!")
                c.close()
                exit(0)
            if data["turn"] == "server":
                turn = input("Its your turn: [1 or 2] ")
                turn = int(turn)
                print("Its now " + str(int(data["data"][-1]) + turn))
                if turn > 2:
                    turn = 2
                if turn < 1:
                    turn = 1
                data["data"].append(int(data["data"][-1]) + turn)
                data["turn"] = "client"
                print("\nSending response...")
                print(data)
                c.sendall(base64.encodebytes(json.dumps(data).encode("utf-8")))
                print("Successfully Sended the response!")
                if data["data"][-1] >= 20:
                    os.system("cls")
                    print("Congrats! You Win! :D")
                    c.close()
                    exit(0)
            else:
                print("Waiting for the enemy's turn")
        print(data)

    # Close the connection with the client
    c.close()
