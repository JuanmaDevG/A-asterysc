from __future__ import annotations
from casilla import *

class Nodo:
    def __init__(self, pos: Casilla, g, h, kcal: int, parent: Nodo = None):
        self.pos = pos
        self.f = g + h
        self.g = g
        self.h = h
        self.kcal = kcal + parent.kcal if parent is not None else 0
        if parent is None or isinstance(parent, Nodo):
            self.parent = parent
        else:
            self.parent = None
            print('WARNING: the value of this parent\'s node should have been another Node or None.')
        
        self.children = []

    def __str__(self):
        return f'(position: {str(self.pos)}, f: {self.f}, g: {self.g}, h: {self.h}, parent: {self.parent.pos if self.parent != None else self.parent})'

    # WARNING: equals operator does NOT compare node quality (f, g, h, kcal) or inheritance
    def __eq__(self, other):
        return self.pos == other.pos
