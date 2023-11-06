from math import cos, sin
import pygame

pygame.init()


class DoublePendule:
    def __init__(self, x1, y1, x2, y2, win_size_, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.win_size = win_size_
        self.color = color

        self.l1 = 240
        self.l2 = 240
        self.m1 = 20
        self.m2 = 20
        self.a1 = 0
        self.a2 = 0
        self.a1_v = 0
        self.a2_v = 0
        self.g = 1
        self.a1_a = 0
        self.a2_a = 0
        self.x1 = self.l1 * sin(self.a1)
        self.y1 = self.l1 * cos(self.a1)
        self.x2 = self.x1 + self.l2 * sin(self.a2)
        self.y2 = self.y1 + self.l2 * cos(self.a2)
        self.trace = []
        self.trace.append((self.x2, self.y2))


    def move(self, dt):
        self.a1_a = (-self.g * (2 * self.m1 + self.m2) * sin(self.a1) - self.m2 * self.g * sin(self.a1 - 2 * self.a2) - 2 * sin(self.a1 - self.a2) * self.m2 * (self.a2_v ** 2 * self.l2 + self.a1_v ** 2 * self.l1 * cos(self.a1 - self.a2))) / (self.l1 * (2 * self.m1 + self.m2 - self.m2 * cos(2 * self.a1 - 2 * self.a2)))
        self.a2_a = (2 * sin(self.a1 - self.a2) * (self.a1_v ** 2 * self.l1 * (self.m1 + self.m2) + self.g * (self.m1 + self.m2) * cos(self.a1) + self.a2_v ** 2 * self.l2 * self.m2 * cos(self.a1 - self.a2))) / (self.l2 * (2 * self.m1 + self.m2 - self.m2 * cos(2 * self.a1 - 2 * self.a2)))
        self.a1_v += self.a1_a * dt
        self.a2_v += self.a2_a * dt
        self.a1 += self.a1_v * dt
        self.a2 += self.a2_v * dt
        self.x1 = self.l1 * sin(self.a1)
        self.y1 = self.l1 * cos(self.a1)
        self.x2 = self.x1 + self.l2 * sin(self.a2)
        self.y2 = self.y1 + self.l2 * cos(self.a2)


    def launch(self, angle1, angle2):
        self.a1 = angle1
        self.a2 = angle2
        self.x1 = self.l1 * sin(self.a1)
        self.y1 = self.l1 * cos(self.a1)
        self.x2 = self.x1 + self.l2 * sin(self.a2)
        self.y2 = self.y1 + self.l2 * cos(self.a2)
        self.trace = []
        self.trace.append((self.x2, self.y2))

    def draw(self, window_):
        pygame.draw.line(window_, self.color, (self.win_size[0] / 2, self.win_size[1] / 2), (self.win_size[0] / 2 + self.x1, self.win_size[1] / 2 + self.y1), 2)
        pygame.draw.line(window_, self.color, (self.win_size[0] / 2 + self.x1, self.win_size[1] / 2 + self.y1), (self.win_size[0] / 2 + self.x2, self.win_size[1] / 2 + self.y2), 2)
        pygame.draw.circle(window_, self.color, (int(self.win_size[0] / 2 + self.x1), int(self.win_size[1] / 2 + self.y1)), 10)
        pygame.draw.circle(window_, self.color, (int(self.win_size[0] / 2 + self.x2), int(self.win_size[1] / 2 + self.y2)), 10)


def create_all_colors(nb_colors):
    colors_ = []
    color_count = (256*3) / nb_colors
    for i in range(nb_colors):
        r = 0
        g = 0
        b = 0

        if color_count * i < 256:
            r = 255 - color_count * i
            g = color_count * i
        elif color_count * i < 512:
            c = color_count*i - 256
            g = 255 - c
            b = c
        else:
            c = color_count * i - 512
            b = 255 - c
            r = c

        colors_.append((r, g, b))

    return colors_


win_size = (1000, 1000)
window = pygame.display.set_mode(win_size)

pendules = []

nb_pendules = 10000
colors = create_all_colors(nb_pendules)
for count in range(nb_pendules):
    pendules.append(DoublePendule(0, 0, 0, 0, win_size, (colors[count][0], colors[count][1], colors[count][2])))
    pendules[count].launch(2, 2-0.00001*count)


run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    window.fill((0, 0, 0))
    for pendule in pendules:
        pendule.move(0.5)
        pendule.draw(window)
    pygame.display.flip()

pygame.quit()