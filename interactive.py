import sys

from board import *
from button import Button
from display import *


def interactive(b):
    terminate = False
    userPick = False
    possibleStart = False
    boardCleared = False
    # Initialize all buttons
    randomBoard = Button(GREEN, padding, 10, 70, 30, "RANDOM")
    creativeBoard = Button(GREEN, padding + 80, 10, 70, 30, "CREATIVE")
    basicBoard = Button(GREEN, padding + 160, 10, 70, 30, "BASIC")
    optStart = Button(GREEN, WIDTH - 100, 10, 70, 30, "Start")
    optClear = Button(D_VIOLET, WIDTH - 180, 10, 70, 30, "Clear")
    optRestart = Button(D_VIOLET, WIDTH - 260, 10, 70, 30, "Restart")
    next_b = Button(GOLD, WIDTH - 100, HEIGHT - 30, 90, 20, text="Next")
    selection = False
    b.act = "choose"
    while not terminate:
        possibleRestart = True
        screen.fill(WHITE)
        display_l(b)
        for e in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if randomBoard.isOver(pos):
                    userPick = False
                    possibleStart = False
                elif creativeBoard.isOver(pos):
                    userPick = True
                    possibleStart = False
                    boardCleared = False
                    b = ObstacleBoard(rows, cols)
                elif basicBoard.isOver(pos):
                    userPick = True
                    possibleStart = False
                    boardCleared = False
                    b = Board(rows, cols)
                elif optClear.isOver(pos):
                    b.clear()
                    possibleStart = False
                    possibleRestart = False
                    userPick = False
                    boardCleared = True
                elif optRestart.isOver(pos):
                    if possibleRestart and not boardCleared:
                        b.restart()
                        possibleStart = True
                    else:
                        possibleStart = False

            if randomBoard.isOver(pos):
                randomBoard.color = GREEN
            else:
                randomBoard.color = AQUA
            if creativeBoard.isOver(pos):
                creativeBoard.color = GREEN
            else:
                creativeBoard.color = AQUA
            if basicBoard.isOver(pos):
                basicBoard.color = GREEN
            else:
                basicBoard.color = AQUA
            if optClear.isOver(pos):
                optClear.color = VIOLET
            else:
                optClear.color = D_VIOLET
            if optRestart.isOver(pos) and possibleRestart:
                optRestart.color = VIOLET
            else:
                optRestart.color = D_VIOLET

            if userPick and not possibleStart:
                b.initialize()
                b.act = 'choose'
                b.userChoose()
                possibleStart = True
                possibleRestart = False

            if possibleStart and not boardCleared and b.start.x:
                # User has option to start the Pathfinding
                optStart.color = GREEN
                if optStart.isOver(pos):
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        b.initChildren()
                        possibleRestart = False
                        return b
                else:
                    optStart.color = D_GREEN
            else:
                optStart.color = L_RED

            randomBoard.draw(screen)
            creativeBoard.draw(screen)
            basicBoard.draw(screen)

            if userPick:
                next_b.draw(screen)

            if possibleStart:
                optStart.draw(screen, (0, 150, 0))  # Green button
            else:
                optStart.draw(screen, (150, 0, 0))  # Red button

            optClear.draw(screen)
            optRestart.draw(screen)
            pygame.display.update()
