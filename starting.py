import pygame
from astar import Astar
import time
from bfs import Bfs
from dfs import Dfs


class Game(Astar, Bfs, Dfs):
    def __init__(self):
        Astar.__init__(self)
        Bfs.__init__(self)
        Dfs.__init__(self)

        pygame.init()
        self.display_width = 1020 + 2 + 200   #setting windows size
        self.display_height = 570 + 2 + 300 - 210
        self.screen = pygame.display.set_mode(
            (self.display_width, self.display_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(u'Algorithm Visualization')
        self.width = 34 #width of grid cell
        self.height = 22 #height of grid

        self.walls = list()
        self.maze = [[]]

        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.less_red = (150, 0, 0)
        self.blue = (0, 255, 0)
        self.less_blue = (0, 150, 0)
        self.green = (0, 0, 255)
        self.less_green = (0, 0, 150)
        self.black = (0, 0, 0)
        self.grid_color = (0, 150, 255)

    def text_objects(self, message, font):
        textSurface = font.render(message, False, self.white)
        return textSurface, textSurface.get_rect()

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        pygame.draw.rect(self.screen, ic, (x, y, w, h))
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.screen, ac, (x, y, w, h))
            if click[0] == 1 and action != None:
                time.sleep(0.5)
                action()

        font = pygame.font.SysFont("freesansbold.ttf", 25)
        textSurface, textRect = self.text_objects(msg, font)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.screen.blit(textSurface, textRect)

    def welcome_screen(self):

        game_exit = False

        while not game_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    pygame.quit()
                    pass

            message = ['Astar, BFS and DFS visualizer']
            width_counter = 0
            for message in message:
                text = pygame.font.Font('freesansbold.ttf', 30)
                TextSurf, TextRect = self.text_objects(message, text)
                TextRect.center = ((self.display_width / 2),
                                   (self.display_height / 2 - 150 +
                                    width_counter))
                width_counter += 30
                self.screen.blit(TextSurf, TextRect)

                self.button("G O !", 500, 450, 100, 50, self.red,
                            self.less_red, self.construct_maze)

                pygame.display.update()
                self.clock.tick(60)

    def construct_maze(self):
        game_exit = False
        draw_grid = False
        self.screen.fill(self.black)
        while not game_exit:
            self.button("Start Node='s'",
                        1025,
                        50,
                        190,
                        50,
                        self.red, (0, 0, 50),
                        action=None)
            self.button("end Node='e'",
                        1025,
                        125,
                        190,
                        50,
                        self.red, (0, 0, 50),
                        action=None)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    gameExit = True

                elif event.type == pygame.KEYDOWN:
                    x, y = pygame.mouse.get_pos()
                    x = x // 30
                    y = y // 30
                    if event.key == pygame.K_s:
                        pygame.draw.rect(self.screen, self.red,
                                         (x * 30, y * 30, 29, 29))
                        self.start_node = (x, y)
                    if event.key == pygame.K_e:
                        pygame.draw.rect(self.screen, self.green,
                                         (x * 30, y * 30, 29, 29))
                        self.end_node = (x, y)

            if not draw_grid:
                for x in range(0, 1020 + 30, 30):
                    pygame.draw.line(self.screen, self.grid_color, (0, x),
                                     (1020, x), 2)  #horizontal line

                    pygame.draw.line(self.screen, self.grid_color, (x, 0),
                                     (x, 1020), 2)
                    self.clock.tick(60)
                    pygame.display.update()
                    draw_grid = True

            x, y = pygame.mouse.get_pos()
            x = x // 30
            y = y // 30
            if pygame.mouse.get_pressed(
            )[0] and x * 30 < 1020 and y * 30 < 400 + 8 * 30:

                pygame.draw.rect(self.screen, self.grid_color,
                                 (x * 30, y * 30, 29, 29))
                if (x, y) not in self.walls:
                    self.walls.append((x, y))

            self.maze = [[0 for i in range(self.height)]
                         for j in range(self.width)]
            for x in self.walls:
                self.maze[x[0]][x[1]] = 1

            self.button("Astar",
                        1025,
                        250,
                        190,
                        50,
                        self.less_blue, (0, 0, 50),
                        action=self.animate_astar)
            self.button("BFS",
                        1025,
                        350,
                        190,
                        50,
                        self.less_blue, (0, 0, 50),
                        action=self.bfs)
            self.button("DFS",
                        1025,
                        450,
                        190,
                        50,
                        self.less_blue, (0, 0, 50),
                        action=self.dfs)
            self.button("Reset",
                        1025,
                        600,
                        190,
                        50,
                        self.less_blue, (0, 0, 50),
                        action=start_game)

            pygame.display.update()

    def animate_astar(self):
        a, path = Astar.search(self, self.maze, 1, self.start_node,
                               self.end_node)

        for a in a:

            pygame.draw.rect(self.screen, self.less_red,
                             (a.position[0] * 30, a.position[1] * 30, 29, 29))
            pygame.display.update()
            self.clock.tick(60)

        draw = []
        for i, j in enumerate(path):
            for k, l in enumerate(j):
                if l is not -1:
                    draw.append((i, k))

        for i in draw[::-1]:

            pygame.draw.rect(self.screen, self.red,
                             (i[0] * 30, i[1] * 30, 29, 29))
            self.clock.tick(200)
            pygame.display.update()

    def bfs(self):
        a, path = Bfs.search(self, self.maze, self.start_node, self.end_node)
        for a in a:

            pygame.draw.rect(self.screen, self.less_red,
                             (a[0] * 30, a[1] * 30, 29, 29))
            pygame.display.update()
            self.clock.tick(60)

        draw = []
        for i, j in enumerate(path):
            for k, l in enumerate(j):
                if l is not -1:
                    draw.append((i, k))

        for i in draw[::-1]:

            pygame.draw.rect(self.screen, self.red,
                             (i[0] * 30, i[1] * 30, 29, 29))
            self.clock.tick(200)
            pygame.display.update()

    def dfs(self):
        a, path = Dfs.search(self, self.maze, self.start_node, self.end_node)
        for a in a:

            pygame.draw.rect(self.screen, self.less_red,
                             (a[0] * 30, a[1] * 30, 29, 29))
            pygame.display.update()
            self.clock.tick(60)

        draw = []
        for i, j in enumerate(path):
            for k, l in enumerate(j):
                if l is not -1:
                    draw.append((i, k))

        for i in draw[::-1]:

            pygame.draw.rect(self.screen, self.red,
                             (i[0] * 30, i[1] * 30, 29, 29))
            self.clock.tick(200)
            pygame.display.update()


def start_game():
    a = Game()

    a.welcome_screen()


start_game()