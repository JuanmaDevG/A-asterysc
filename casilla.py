from enum import Enum
from copy import copy

class Move(Enum) : #(y, x)
    UP = (-1, 0)
    UP_RIGHT = (-1, 1)
    RIGHT = (0, 1)
    DOWN_RIGHT = (1, 1)
    DOWN = (1, 0)
    DOWN_LEFT = (1, -1)
    LEFT = (0, -1)
    UP_LEFT = (-1, -1)

class Casilla():
    def __init__(self, f: int, c: int):
        self.fila=f
        self.col=c

    def __str__(self):
        return str(self.toTuple())

    def __eq__(self, other):
        return self.fila == other.fila and self.col == other.col

    def __repr__(self):
        return str(self.toTuple())

    def getFila (self) -> int:
        return self.fila
    
    def getCol (self) -> int:
        return self.col

    def toTuple(self) -> (int, int):
        return (self.fila, self.col)
        
    def move(self, mv: Move):
        self.fila, self.col = self.fila + mv.value[0], self.col + mv.value[1]

    def pivotOver(self, pos: (int, int), mv: Move):
        self.fila, self.col = pos[0] + mv.value[0], pos[1] + mv.value[1]
    
    def getPivotInstance(self, mv: Move):
        instance = copy(self)
        instance.move(mv)
        return instance

    def getFrontier(self) -> [int]:
        frontier = []
        for mv in Move:
            frontier.append(self.getPivotInstance(mv))
        
        return frontier
