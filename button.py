import pygame

pygame.init()


class Button:
    def __init__(self, color, x, y, w, h, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.w + 4, self.h + 4), 5)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), 0)
        if self.text != '':
            font = pygame.font.SysFont('rainyhearts', 15)
            text = font.render(self.text, True, (255, 255, 255))
            screen.blit(text,
                        (self.x + (self.w / 2 - text.get_width() / 2), self.y + (self.h / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.w:
            if self.y < pos[1] < self.y + self.h:
                return True

        return False
