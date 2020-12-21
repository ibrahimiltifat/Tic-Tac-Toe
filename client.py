import pygame
from grid import Grid

surface = pygame.display.set_mode((600, 600))
pygame.display.set_caption('TIC_TAC_TOE')

import threading


def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

    return thread


# creating a TCP socket for the client
import socket

HOST = '127.0.0.1'
PORT = 65004

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))



def recieve_data():

    while True:
        data = sock.recv(1024).decode()
        data = data.split('-')
        x, y, player = int(data[0]), int(data[1]), data[2]
        grid.set_cell_value(x, y, player)


create_thread(recieve_data)

grid = Grid()
running = True
player="O"

while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed():

                    pos = pygame.mouse.get_pos()
                    cellX, cellY = pos[0] // 200, pos[1] // 200
                    grid.get_mouse(cellX, cellY, player)
                    send_data = '{}-{}-{}'.format(cellX, cellY, player).encode()
                    sock.send(send_data)
                    if grid.winning(player):
                        running = False

        surface.fill((0, 0, 0))
        grid.draw(surface)
        pygame.display.flip()
