from casilla import *
from mapa import *

class Nodo:
    def __init__(self, pos: Casilla, g, h, parent: 'Nodo' = None):
        self.pos = pos
        self.f = g + h
        self.g = g
        self.h = h
        if parent is None or isinstance(parent, Nodo):
            self.parent = parent
        else:
            self.parent = None
            print('WARNING: the value of this parent\'s node should have been another Node or None.')
        
        self.children = []

    def addChildren(self, *children):
        for child in children:
            self.children.append(child)

