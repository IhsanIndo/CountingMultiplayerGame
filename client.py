import socket
import base64
import json
import os

port = 8239
data = {}
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # s.connect(("192.168.0."+input("192.168.0."), port))
    while True:
        try:
            s.connect(("---------", port))
            break
        except:
            pass
    s.sendall(base64.encodebytes(b"are you a counting game server?"))
    # print(s.recv(1024).decode("utf-8"))
    if base64.decodebytes(s.recv(1024)).decode("utf-8") == "yes we are":
        print("Great! were connected to a real server")
        print("Starting game please wait.")
        data = json.loads(base64.decodebytes(s.recv(1024)).decode("utf-8"))
        while True:
            print("Current data: " + str(data["data"][-1]))
            print("Waiting for enemy")
            if data["turn"] != "client":
                while True:
                    try:
                        data = json.loads(base64.decodebytes(s.recv(1024)).decode("utf-8"))
                        break
                    except:
                        pass
                os.system("cls")
            print("Current data: " + str(data["data"][-1]))
            print("Enemy: " + str(data["data"][-1]) + " [+" + str(data["data"][-1] - data["data"][-2]) + "]")
            if data["data"][-1] >= 20:
                os.system("cls")
                print("Unfortunately, The enemy wins!")
                s.close()
                exit(0)
            if data["turn"] == "client":
                turn = input("Its your turn to add: [1 or 2] ")
                turn = int(turn)
                print("Its now " + str(int(data["data"][-1]) + turn))
                if turn > 2:
                    turn = 2
                if turn < 1:
                    turn = 1
                data["data"].append(int(data["data"][-1]) + turn)
                data["turn"] = "server"
                print("\nSending response....")
                s.sendall(base64.encodebytes(json.dumps(data).encode("utf-8")))
                print("Successfully Sended the response!")
                if data["data"][-1] >= 20:
                    os.system("cls")
                    print("Congrats! You Win! :D")
                    s.close()
                    exit(0)
                os.system("cls")
            else:
                print("Waiting for the enemy's turn")
        print(data)
    else:
        print("This is not an Counting game server")
    s.close()
