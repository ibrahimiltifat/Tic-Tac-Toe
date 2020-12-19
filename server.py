import pygame
from grid import Grid

# import os
#
# os.environ['SDL_VIDEO_WINDOW_POSITION'] = '400,100'

surface = pygame.display.set_mode((600, 600))
pygame.display.set_caption('TIC_TAC_TOE')

grid = Grid()


running = True
player = "X"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed():
                pos = pygame.mouse.get_pos()
                # print(pos[0]//200, pos[1] // 200)
                grid.get_mouse(pos[0] // 200, pos[1] // 200, player)
                if grid.winning(player):
                    running=False
                if player == "X":
                    player = "O"
                else:
                    player = "X"


    surface.fill((0, 0, 0))
    grid.draw(surface)
    pygame.display.flip()


