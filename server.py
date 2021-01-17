
import tkinter
import socket
import threading
import time

server = None
ADDR = "127.0.0.1"
PORT = 8012
name = ""
allclients = []
clientnames = []

#setting up the GUI
whole_Frame = tkinter.Tk()
whole_Frame.title("CS447-Project")

showclients = tkinter.Frame(whole_Frame)
displayer = tkinter.Text(showclients, height=20, width=25)
displayer.pack(side=tkinter.RIGHT, fill=tkinter.X, pady=(5, 0))
displayer.config(background="#A2A3A4", state="disabled")
showclients.pack(side=tkinter.TOP)

buttonCol = tkinter.Frame(whole_Frame)
serverStarter = tkinter.Button(buttonCol, text="Run Server", command=lambda: runserver())
serverStarter.pack(side=tkinter.RIGHT)
buttonCol.pack(side=tkinter.BOTTOM)


def runserver():
    serverStarter.config(state=tkinter.DISABLED)
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ADDR, PORT))
    server.listen(5)
    th = threading.Thread(target=letclientconnect, args=(server, ""))
    th.setDaemon(True)
    th.start()


def letclientconnect(srvr, st):
    while 1:
        if len(allclients) < 2:
            cli, addr = srvr.accept()
            allclients.append(cli)
            th = threading.Thread(target=communicate, args=(cli, addr))
            th.setDaemon(True)
            th.start()


def communicate(cli, address):
    global server, name, allclients
    name = cli.recv(4096).decode()
    if len(allclients) < 2:
        cli.send("w1".encode())#assigning client1 and client2
    else:
        cli.send("w2".encode())

    clientnames.append(name)
    updateDisplayer(clientnames)

    if len(allclients) > 1:
        time.sleep(1)
        allclients[0].send(("rvl" + clientnames[1] + "X").encode())#exchigng name information with the clients
        allclients[1].send(("rvl" + clientnames[0] + "O").encode())

    while 1:
        try:
            rcvd = cli.recv(4096).decode()
            if rcvd is None:
                break
            elif rcvd.startswith("|cor"):
                if cli == allclients[0]:#telling both the clients about new coordinates after every turn
                    allclients[1].send(rcvd.encode())
                elif cli == allclients[1]:
                    allclients[0].send(rcvd.encode())
        except Exception as w:
            break
    index = indexofcli(allclients, cli)
    print(index)
    del clientnames[index], allclients[index]
    cli.close()
    updateDisplayer(clientnames)


def indexofcli(all, searched):
    for clis in range(len(all)):
        if all[clis] == searched:
            return clis
    return -1


def updateDisplayer(clinames):
    displayer.config(state=tkinter.NORMAL)
    displayer.delete("1.0", tkinter.END)
    for name in clinames:
        displayer.insert(tkinter.END, name + "\n")
    displayer.config(state=tkinter.DISABLED)


whole_Frame.mainloop()
