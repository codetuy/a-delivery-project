from board import Board, set_remove
from button import Button
from display import *
from interactive import interactive

pygame.init()


def sortBoxes(origin, boxes, newBoxes=None):
    if newBoxes is None:
        newBoxes = []
    if len(boxes) == 0:
        return boxes
    distances = {}

    for i in boxes:
        dist = pow(i.x - origin.x, 2) + pow(i.y - origin.y, 2)
        distances[i] = dist

    origin = min(distances.keys(),
                 key=(lambda k: distances[k]))  # New origin is the node with the smallest dist from the previous origin

    newBoxes.append(origin)
    boxes.remove(origin)
    sortBoxes(origin, boxes, newBoxes)
    return newBoxes


def findGoalPath(b, winner, currentOpenSet, currentClosedSet):
    for i in range(len(b.openSet)):
        if b.openSet[i].f < b.openSet[winner].f:
            winner = i
    b.current = b.openSet[winner]
    if b.current.isGoal(b):
        b.finish = True
        b.act = "done"
        temp = b.current
        b.path.append(temp)
        b.paths.extend(b.path)
        b.path = b.paths
        return True

    set_remove(b.openSet, b.current)
    currentClosedSet.append(b.current);
    neighbors = b.current.neighbors

    for i in range(len(neighbors)):
        neighbor = neighbors[i]
        newPath = False
        if neighbor not in currentClosedSet and not neighbor.wall:
            temp_g = b.current.g + 1

            if neighbor in b.openSet:
                if temp_g < neighbor.g:
                    neighbor.g = temp_g
                    newPath = True
            else:
                neighbor.g = temp_g
                b.openSet.append(neighbor)
                newPath = True

            if newPath:
                neighbor.h = neighbor.heuristic(b.goal)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.previous = b.current


def A_star(b):
    box = 0
    skip = False
    skip_b = Button(GOLD, WIDTH - 100, HEIGHT - 30, 90, 20, text="Fast Forward")
    b.checkpoints = sortBoxes(b.start, b.checkpoints, [])  # first reference point - b.start
    while len(b.openSetsBox[box]) > 0:
        b.act = 'work'
        winner = 0
        currentOpenSet = b.openSetsBox[box]
        currentClosedSet = b.closedSetBox[box]
        if len(b.openSetsBox) > 1:
            if box < len(b.checkpoints):
                for i in range(len(currentOpenSet)):
                    if currentOpenSet[i].f < currentOpenSet[winner].f:
                        winner = i
                b.current = currentOpenSet[winner]

                # Found the closest checkpint
                if b.current.isBox(b.checkpoints[box]):
                    b.currentBox += 1
                    b.checkpointsFound[box] = True
                    b.current.previous = None

                    box += 1
                    b.paths.extend(b.path)
                    b.openSetsBox[box][0] = b.current
                    b.openSet = b.openSetsBox[box]
                    b.closedSetBox.append([])

                # If the the processes of finding the next checkpoint
                else:

                    # Remove the current node from the open set
                    # Mark the node as visited
                    # Update the list of neighbors of the current node
                    set_remove(currentOpenSet, b.current)
                    currentClosedSet.append(b.current)
                    neighbors = b.current.neighbors

                    # Look through the neigbors
                    for i in range(len(neighbors)):
                        neighbor = neighbors[i]
                        newPath = False

                        if neighbor not in currentClosedSet and not neighbor.wall:
                            temp_g = b.current.g + 1

                            if neighbor in currentOpenSet:
                                if temp_g < neighbor.g:
                                    neighbor.g = temp_g
                                    newPath = True

                            else:
                                neighbor.g = temp_g
                                currentOpenSet.append(neighbor)
                                newPath = True

                            if newPath:
                                # New path has been chosen
                                # Update the estimated cost from the neigbor's node to the checkpoint
                                neighbor.h = neighbor.heuristic(b.checkpoints[box])
                                neighbor.f = neighbor.g + neighbor.h
                                neighbor.previous = b.current
            else:
                if findGoalPath(b, winner, currentOpenSet, currentClosedSet): return
        else:
            if findGoalPath(b, winner, currentOpenSet, currentClosedSet): return

        b.path = []
        temp = b.current
        b.path.append(temp)
        while temp.previous:
            b.path.append(temp.previous)
            temp = temp.previous

        # Check if user fastforwards
        for e in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if skip_b.isOver(pos):
                skip_b.color = ORANGE
                if e.type == pygame.MOUSEBUTTONDOWN:
                    skip = True
                    skip_b.color = D_ORANGE
            else:
                skip_b.color = GOLD

        if not skip:
            display_l(b)
            skip_b.draw(screen)
            pygame.display.update()
    else:
        print("No Solution")

    display(b)


def main():
    b = Board(rows, cols)
    b.initialize()

    while True:
        b = interactive(b)
        A_star(b)
        b.finish = False

    pygame.quit()
    sys.exit()


main()
