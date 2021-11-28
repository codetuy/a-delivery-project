class Node:
    def __init__(self, row, col):
        self.x = col
        self.y = row
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.previous = None
        self.wall = False

    def isBox(self, checkpoint):
        if self == checkpoint:
            return True
        return False

    def isGoal(self, b):
        if self == b.goal:
            return True
        return False

    def createChildren(self, b):
        # NWSE
        if 0 <= self.y + 1 < b.rows:
            self.neighbors.append(b.matrix[self.y + 1][self.x])
        if 0 <= self.y - 1 < b.rows:
            self.neighbors.append(b.matrix[self.y - 1][self.x])
        if 0 <= self.x + 1 < b.cols:
            self.neighbors.append(b.matrix[self.y][self.x + 1])
        if 0 <= self.x - 1 < b.cols:
            self.neighbors.append(b.matrix[self.y][self.x - 1])

    def heuristic(self, nodeB):
        return abs(self.x - nodeB.x) + abs(self.y - nodeB.y)  # Manhattan Dist
        # return sqrt((self.x - nodeB.x) ** 2 + (self.y - nodeB.y) ** 2)  # Euclid Dist
