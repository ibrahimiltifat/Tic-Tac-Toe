import pygame
import os

letterX = pygame.image.load(os.path.join('img', 'x.png'))
letterO = pygame.image.load(os.path.join('img', 'O.png'))


class Grid:
    def __init__(self):
        self.grid_lines = [((0, 180), (600, 180)),
                           ((0, 380), (600, 380)),
                           ((180, 0), (180, 600)),
                           ((390, 0), (390, 600))]
        self.grid = [[0 for x in range(3)] for y in range(3)]

    def draw(self, surface):
        for line in self.grid_lines:
            pygame.draw.line(surface, (200, 200, 200), line[0], line[1], 2)

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x, y) == "X":
                    surface.blit(letterX, (x*200, y*200 ))
                elif self.get_cell_value(x, y) == "O":
                    surface.blit(letterO, (x*200 , y*200))


    def print_grid(self):
        for row in self.grid:
            print(row)

    def get_cell_value(self, x, y):
        return self.grid[y][x]

    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value

    def get_mouse(self, x, y, player):
        if player == "X":
            self.set_cell_value(x, y, "X")
        if player == "O":
            self.set_cell_value(x, y, "O")

    def winning(self, player):
        if (self.grid[0][0] == self.grid[0][1] == self.grid[0][2] == player or
                self.grid[1][0] == self.grid[1][1] == self.grid[1][2] == player or
                self.grid[2][0] == self.grid[2][1] == self.grid[2][2] == player or
                self.grid[0][0] == self.grid[1][0] == self.grid[2][0] == player or
                self.grid[0][1] == self.grid[1][1] == self.grid[2][1] == player or
                self.grid[2][0] == self.grid[2][1] == self.grid[2][2] == player or
                self.grid[0][0] == self.grid[2][2] == self.grid[2][2] == player or
                self.grid[0][2] == self.grid[2][2] == self.grid[2][0] == player):

            print(player + " won")
            return 1
        else:
            return 0
