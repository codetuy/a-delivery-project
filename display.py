import pygame

pygame.init()

cols = 61
rows = 31
ppb = 15

# Colours
ORANGE = (240, 94, 35)
D_ORANGE = (240 - 50, 94 - 50, 35 - 20)
GREEN = (0, 255, 0)
D_GREEN = (0, 200, 0)
GOLD = (255, 191, 0)
AQUA = (102, 221, 170)
L_AQUA = (127, 255, 212)
L2_AQUA = (127, 255, 169)
D_AQUA = (26, 101, 101)
L_RED = (255, 0, 0)
RED = (166, 25, 25)
WHITE = (255, 255, 255)
BLACK = (153, 76, 0)
AMBER = (255, 213, 0)
VIOLET = (185, 139, 231)
D_VIOLET = (185 - 30, 139 - 30, 231 - 30)

PATHSHADE1 = (221, 105, 242)
PATHSHADE2 = (224, 117, 219)
PATHSHADE3 = (227, 130, 196)
PATHSHADE4 = (231, 143, 173)
PATHSHADE5 = (234, 155, 151)
PATHSHADE6 = (238, 168, 128)
PATHSHADE7 = (244, 193, 83)
PATHSHADE8 = (248, 206, 60)

# Display
padding = 50
WIDTH = padding + cols * ppb + 100
HEIGHT = padding * 2 + rows * ppb

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# fonts/text

font = pygame.font.Font('rainyhearts.ttf', 20)
font1 = pygame.font.Font('rainyhearts.ttf', 15)
font2 = pygame.font.Font('rainyhearts.ttf', 30)
font3 = pygame.font.Font('rainyhearts.ttf', 15)
action = font.render(None, True, BLACK)


def display_l(b):
    global action
    global screen

    screen.fill(WHITE)
    for row in range(b.rows):
        for col in range(b.cols):
            node = b.matrix[row][col]

            if node in b.paths:
                pygame.draw.rect(screen, GOLD, [padding + col * ppb, padding + row * ppb, ppb, ppb])

                # Draw finished path
                if b.finish:
                    pygame.draw.rect(screen, AMBER, [padding + col * ppb, padding + row * ppb, ppb, ppb])

            if node in b.path and node != b.currentBox:
                pygame.draw.rect(
                    screen, GOLD, [padding + col * ppb, padding + row * ppb, ppb, ppb])
                if b.current is not None:
                    if node == b.current:
                        pygame.draw.rect(screen, VIOLET, [padding + col * ppb, padding + row * ppb, ppb, ppb])
            else:
                pygame.draw.ellipse(screen, WHITE, [padding + col * ppb, padding + row * ppb, ppb, ppb])

            if node in b.checkpoints:
                pygame.draw.rect(screen, BLACK, [padding + col * ppb, padding + row * ppb, ppb, ppb])
            elif node == b.start:
                pygame.draw.ellipse(screen, ORANGE, [padding + col * ppb, padding + row * ppb, ppb, ppb])
            elif node == b.goal:
                pygame.draw.ellipse(screen, RED, [padding + col * ppb, padding + row * ppb, ppb, ppb])
            elif node is not None and node.wall:
                pygame.draw.rect(screen, D_AQUA, [padding + col * ppb, padding + row * ppb, ppb, ppb])

            elif node == b.current:
                pygame.draw.ellipse(screen, VIOLET, [padding + col * ppb, padding + row * ppb, ppb, ppb])

            # Draw Node selection interface
            if b.userSelect == 's':
                choose = font.render("Start", True, D_AQUA)
                screen.blit(choose, (WIDTH - 55, padding + 40))
                pygame.draw.ellipse(screen, ORANGE, [WIDTH - 80, padding + 40, 20, 20])
            elif b.userSelect == 'g':
                choose = font.render("Goal", True, D_AQUA)
                screen.blit(choose, (WIDTH - 55, padding + 80))
                pygame.draw.ellipse(screen, RED, [WIDTH - 80, padding + 80, 20, 20])
            elif b.userSelect == 'box':
                choose = font.render("Box", True, D_AQUA)
                screen.blit(choose, (WIDTH - 55, padding + 120))
                pygame.draw.rect(screen, BLACK, [WIDTH - 80, padding + 120, 20, 20])
            elif b.userSelect == 'w':
                choose = font.render("Wall", True, D_AQUA)
                screen.blit(choose, (WIDTH - 55, padding + 160))
                pygame.draw.rect(screen, D_AQUA, [WIDTH - 80, padding + 160, 20, 20])

            # Draw action of the user.
            bigtextX = WIDTH // 2 - 100
            bigtextY = HEIGHT - 40
            # work: Process of Pathfinding
            if b.act == 'work':
                if len(b.openSetsBox) > 1:
                    if b.currentBox < len(b.openSetsBox):
                        currentCP = font.render(
                            "Looking for Box #" + str(b.currentBox), True, BLACK)
                    else:
                        currentCP = font.render("Looking for Goal", True, RED)
                    screen.blit(currentCP, (padding, HEIGHT - 35))

            # fail: Unable to find a path to goal/ readh every checkpoint
            elif b.act == 'fail':
                action = font3.render('Fail: There exists no path to read every node selection', True, RED)
            # done: Path found
            elif b.act == 'done':
                action = font3.render('Path found: Completed!', True, RED)

            screen.blit(action, (bigtextX, bigtextY))


def display(b):
    display_l(b)
    pygame.display.update()
