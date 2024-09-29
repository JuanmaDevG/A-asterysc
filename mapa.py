from casilla import *
from nodo import *

ID_HIERBA=0
ID_MURO=1
ID_AGUA=4
ID_ROCA=5

KCAL_HIERBA=2
KCAL_AGUA=4
KCAL_ROCA=6

class Mapa():
    def __init__(self, archivo):        
        self.mapa=leer(archivo)         
        self.alto = len(self.mapa)
        self.ancho = len(self.mapa[0])        
        
    def __str__(self):
        salida = "" 
        for f in range(self.alto):            
            for c in range(self.ancho):               
                if self.mapa[f][c] == ID_HIERBA:
                    salida += "  "
                if self.mapa[f][c] == ID_MURO:
                    salida += "# "                 
                if self.mapa[f][c] == 3:
                    salida += "D "
                if self.mapa[f][c] == ID_AGUA:
                    salida += "~ "
                if self.mapa[f][c] == ID_ROCA:
                    salida += "* "   
            salida += "\n"
        return salida
    
    def getAlto(self):
        return self.alto
    
    def getAncho(self):
        return self.ancho
    
    def getCelda(self, y, x):
        return self.mapa[y][x]

    def setCelda(self, y, x, valor):
        self.mapa[y][x]=valor    

    # ---------------------------------
    # Functions for debugging
    # ---------------------------------

    def whereis(self, p: Nodo | Casilla):
        strmap = ""
        y = 0; x = 0;
        p = p.toTuple() if isinstance(p, Casilla) else p.pos.toTuple()
        for l in self.mapa :
            for obj_id in l :
                strmap += "X " if p[0] == y and p[1] == x else ["  ", "# ", "? ", "D ", "~ ", "* "][obj_id]
                x+=1
            strmap += "\n"
            x=0
            y+=1
        return strmap

    def _isValid(self, y: int, x: int) -> bool:
        return y >= 0 and y < self.alto and x >= 0 and x < self.ancho and self.mapa[y][x] != ID_MURO

    def isValid(self, p = Casilla | Nodo | list) -> bool | list :
        result = []
        if isinstance(p, list) :
            for obj in p :
                result.append(self._isValid(*(obj.toTuple() if isinstance(obj, Casilla) else obj.pos.toTuple())))
        else :
            result = self._isValid(*(p.toTuple() if isinstance(p, Casilla) else p.pos.toTuple()))
        return result

    def viewExpansion(self, nodes: [Nodo]):
        enctype = 'utf-8'
        bytemap = bytearray(str(self).encode(enctype))
        for n in nodes :
            p = n.pos.col + (n.pos.fila * self.ancho * 2) + n.pos.fila # last sum is "+ \n characters
            bytemap[p] = ord('x')
        return bytemap.decode(enctype)

# ---------------------------------------------------------------------
# Funciones
# ---------------------------------------------------------------------

def leer(archivo):
    mapa=[] 
    try:  
        fich=open(archivo, "r")
        fila=-1
        for cadena in fich:
            fila=fila+1            
            mapa.append([])            
            for i in range(len(cadena)):                
                if cadena[i] == ".":
                    mapa[fila].append(ID_HIERBA)                    
                if cadena[i] == "#":
                    mapa[fila].append(ID_MURO)
                if cadena[i] == "~":
                    mapa[fila].append(ID_AGUA)
                if cadena[i] == "*":
                    mapa[fila].append(ID_ROCA)
                    
    except:
        print ("Error de fichero")
        fich.close()
        
    fich.close()
    return mapa


# ---------------------------------------------------------------------
if __name__=="__main__":   
    mapa = Mapa('mapa.txt')
    print (mapa)
    
    
