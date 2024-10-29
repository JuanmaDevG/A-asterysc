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

    def __repr__(self):
        return f'({self.pos}, f = {self.f}, g = {self.g}, h = {self.h}, parent = {self.parent.pos if self.parent != None else None})'

    # WARNING: equals operator does NOT compare node quality (f, g, h, kcal) or inheritance
    def __eq__(self, other: Nodo):
        return other is not None and self.pos == other.pos

    def __gt__(self, other):
        return self.f > other.f

    def __lt__(self, other):
        return self.f < other.f

    def doesNotLoop(self):
        if self.parent is None: return True
        if self == self.parent: return False

        p = self.parent
        while p.parent is not None:
            p = p.parent
            if self == p:
                return False #Does loop
        return True
