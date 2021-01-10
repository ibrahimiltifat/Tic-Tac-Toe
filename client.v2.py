import tkinter as tk
from tkinter import messagebox
import socket
from time import sleep
import threading

main_frame = tk.Tk()
main_frame.title("Tic Tac Toe C")
window = tk.Frame(main_frame)
nameButton = tk.Button(window, text="Play", command=lambda: connect())
nameButton.pack(side=tk.RIGHT)
entry = tk.Entry(window)
entry.pack(side=tk.RIGHT)
label = tk.Label(window, text="Name: ")
label.pack(side=tk.RIGHT)
window.pack(side=tk.TOP)
wind = tk.Frame(main_frame)

client = None
HOST_ADDR = "192.168.0.110"
HOST_PORT = 8012

turn = False
didYouStart = False
listOfLabels = []
columns = 3

my_info = {
    "name": "",
    "symbol": "X",
    "score": 0
}

oppo_info = {
    "name": " ",
    "symbol": "O",
    "score": 0
}

for x in range(3):
    for y in range(3):
        label2 = tk.Label(wind, text=" ", height=2, width=5, highlightbackground="brown",
                          highlightcolor="brown", highlightthickness=1)
        label2.bind("<Button-1>", lambda e, xy=[x, y]: sendCoordinate(xy))
        label2.grid(row=x, column=y)

        dict_labels = {"xy": [x, y], "symbol": "", "label": label2, "ticked": False}
        listOfLabels.append(dict_labels)

label_status = tk.Label(wind, text="Not connected to server")
label_status.grid(row=3, columnspan=3)
wind.pack_forget()


def init(a, b):
    global listOfLabels, turn, my_info, oppo_info, didYouStart
    sleep(2)

    for k in range(len(listOfLabels)):
        listOfLabels[k]["symbol"] = ""
        listOfLabels[k]["ticked"] = False
        listOfLabels[k]["label"]["text"] = ""
        listOfLabels[k]["label"].config(foreground="red", highlightthickness=1)

        if didYouStart:
            didYouStart = False
            turn = False
            label_status["text"] = "It is your opponent's turn."
        else:
            didYouStart = True
            turn = True
            label_status["text"] = "It is your turn."


def sendCoordinate(c):
    global client, turn
    index = c[0] * columns + c[1]
    label3 = listOfLabels[index]

    if turn:
        if label3["ticked"] is not True:
            label3["label"].config(foreground="blue")
            label3["label"]["text"] = my_info["symbol"]
            label3["ticked"] = True
            label3["symbol"] = my_info["symbol"]
            client.send(("|cor" + str(c[0]) + "|" + str(c[1])).encode())
            turn = False

            gameResult = checkProcess()
            if gameResult[0] is True and gameResult[1] != "":
                my_info["score"] = my_info["score"] + 1
                label_status["text"] = "Congrats, you win!"
                label_status.config(foreground="green")
                th = threading.Thread(target=init, args=("", ""))
                th.setDaemon(True)
                th.start()

            elif gameResult[0] is True and gameResult[1] == "":
                label_status["text"] = "It is a draw!"
                label_status.config(foreground="cyan")
                th = threading.Thread(target=init, args=("", ""))
                th.setDaemon(True)
                th.start()
            else:
                label_status["text"] = "Opponent's turn."
    else:
        label_status["text"] = "It is not your turn."


def rowCheck():
    symbolList = []
    listOfLabels_2 = []
    win = False
    symbolOfWin = ""

    for i in range(len(listOfLabels)):
        symbolList.append(listOfLabels[i]["symbol"])
        listOfLabels_2.append(listOfLabels[i])
        if (i + 1) % 3 == 0:
            if symbolList[0] == symbolList[1] == symbolList[2]:
                if symbolList[1] != "":
                    win = True
                    symbolOfWin = symbolList[0]
                    listOfLabels_2[0]["label"].config(foreground="green", highlightbackground="green")
                    listOfLabels_2[1]["label"].config(foreground="green", highlightbackground="green")
                    listOfLabels_2[2]["label"].config(foreground="green", highlightbackground="green")
            symbolList = []
            listOfLabels_2 = []
    return [win, symbolOfWin]


def columnCheck():
    win = False
    symbolOfWin = ""
    for i in range(columns):
        if listOfLabels[i]["symbol"] == listOfLabels[i + columns]["symbol"] == listOfLabels[i + columns + columns][
            "symbol"]:
            if listOfLabels[i]["symbol"] != "":
                win = True
                symbolOfWin = listOfLabels[i]["symbol"]
                listOfLabels[i]["label"].config(foreground="green")
                listOfLabels[i + columns]["label"].config(foreground="green")
                listOfLabels[i + columns + columns]["label"].config(foreground="green")
    return [win, symbolOfWin]


def diagonallyCheck():
    win = False
    symbolOfWin = ""
    i, j = 0, 2

    x = listOfLabels[i]["symbol"]
    y = listOfLabels[i + (columns + 1)]["symbol"]
    z = listOfLabels[(columns + columns) + (i + 1)]["symbol"]
    if listOfLabels[i]["symbol"] == listOfLabels[i + (columns + 1)]["symbol"] == \
            listOfLabels[(columns + columns) + (i + 2)]["symbol"]:
        if listOfLabels[i]["symbol"] != "":
            win = True
            symbolOfWin = listOfLabels[i]["symbol"]
            listOfLabels[i]["label"].config(foreground="green")
            listOfLabels[i + (columns + 1)]["label"].config(foreground="green")
            listOfLabels[(columns + columns) + (i + 2)]["label"].config(foreground="green")

    elif listOfLabels[j]["symbol"] == listOfLabels[j + (columns - 1)]["symbol"] == listOfLabels[j + (columns + 1)][
        "symbol"]:
        if listOfLabels[j]["symbol"] != "":
            win = True
            symbolOfWin = listOfLabels[j]["symbol"]
            listOfLabels[j]["label"].config(foreground="green")
            listOfLabels[j + (columns - 1)]["label"].config(foreground="green")
            listOfLabels[j + (columns + 1)]["label"].config(foreground="green")

    else:
        win = False

    return [win, symbolOfWin]


def drawCheck():
    for j in range(len(listOfLabels)):
        if listOfLabels[j]["ticked"] is False:
            return [False, ""]
    return [True, ""]


def checkProcess():
    result = rowCheck()
    if result[0]:
        return result

    result = columnCheck()
    if result[0]:
        return result

    result = diagonallyCheck()
    if result[0]:
        return result

    result = drawCheck()
    return result


def connect():
    global my_info
    if len(entry.get()) < 1:
        tk.messagebox.showerror(title="error", message="You need to enter your name")
    else:
        my_info["name"] = entry.get()
        connectToServer(entry.get())


def connectToServer(s):
    global client, HOST_PORT, HOST_ADDR
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        client.send(s.encode())
        th = threading.Thread(target=communicate, args=(client, "m"))
        th.setDaemon(True)
        th.start()
        window.pack_forget()
        wind.pack(side=tk.TOP)
        main_frame.title("Client" + s)
    except Exception as e:
        tk.messagebox.showerror(title="error", message="cannot connect")


def communicate(sender, m):
    global my_info, oppo_info, turn, didYouStart
    while 1:
        rcvd = sender.recv(4096).decode()
        if rcvd is None:
            break
        elif rcvd == "w1":
            label_status["text"] = "Welcome " + my_info["name"] + ":) We will connect you when another player comes"
        elif rcvd == "w2":
            label_status["text"] = "Welcome " + my_info["name"] + ":) We matched you with another player."

        elif rcvd.startswith("rvl"):
            oppo_info["name"] = rcvd[3:-1]
            my_info["symbol"] = rcvd[-1]

            if my_info["symbol"] == "O":
                oppo_info["symbol"] = "X"
            elif my_info["symbol"] == "X":
                oppo_info["symbol"] = "O"

            label_status["text"] = "GOOD NEWS: " + oppo_info["name"] + " is connected!"
            sleep(3)
            if my_info["symbol"] == "O":
                label_status["text"] = "It is your turn!"
                turn = True
                didYouStart = True
            else:
                label_status["text"] = "Now, it is " + oppo_info["name"] + "'s turn!"
                didYouStart = False
                turn = False
        elif rcvd.startswith("|cor"):
            temp = rcvd.replace("|cor", "")
            x_coor = temp[:temp.find("|")]
            y_coor = temp[temp.find("|") + 1:]
            index = int(x_coor) * columns + int(y_coor)
            label = listOfLabels[index]
            label["symbol"] = oppo_info["symbol"]
            label["label"]["text"] = oppo_info["symbol"]
            label["ticked"] = True

            result = checkProcess()
            if result[0] is True and result[1] != "":
                oppo_info["score"] = oppo_info["score"] + 1
                if result[1] == oppo_info["symbol"]:  #
                    label_status["text"] = "You have lost! Your score:" + str(my_info["score"]) + " - " \
                                                                                                  "" + oppo_info[
                                               "name"] + "'s score:" + str(oppo_info["score"])
                    label_status.config(foreground="purple")
                    th = threading.Thread(target=init, args=("", ""))
                    th.setDaemon(True)
                    th.start()
            elif result[0] is True and result[1] == "":
                label_status["text"] = "It is a draw! Your score:" + str(my_info["score"]) + " - " + oppo_info[
                                           "name"] + "'s score:" + str(oppo_info["score"])
                label_status.config(foreground="orange")
                th = threading.Thread(target=init, args=("", ""))
                th.setDaemon(True)
                th.start()
            else:
                turn = True
                label_status["text"] = "It is your turn!"
                label_status.config(foreground="black")

    sender.close()


main_frame.mainloop()
