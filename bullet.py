import pygame

sw = 800
sh = 800


class Bullet(object):
    def __init__(self, player):
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player.cosine
        self.s = player.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), [self.x, self.y, self.w, self.h])

    def check_off_screen(self):
        if self.x < -50 or self.x > sw or self.y > sh or self.y < -50:
            return True
