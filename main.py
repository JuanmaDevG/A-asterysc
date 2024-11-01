import sys, pygame, math
from casilla import *
from mapa import *
from pygame.locals import *
from heapq import heappop, heappush, heapify


MARGEN=5
MARGEN_INFERIOR=60
TAM=30
NEGRO=(0,0,0)
HIERBA=(250, 180, 160)
MURO=(30, 70, 140)
AGUA=(173, 216, 230) 
ROCA=(110, 75, 48)
AMARILLO=(255, 255, 50) 
EPSILON=0.2


# ---------------------------------------------------------------------
# Funciones
# ---------------------------------------------------------------------

# Devuelve si una casilla del mapa se puede seleccionar como destino o como origen
def bueno(mapi, pos):
    return mapi.getCelda(*pos.toTuple()) in [ID_HIERBA, ID_AGUA, ID_ROCA]
    
# Devuelve si una posición de la ventana corresponde al mapa
def esMapa(mapi, posicion):
    res=False     
    
    if posicion[0] > MARGEN and posicion[0] < mapi.getAncho()*(TAM+MARGEN)+MARGEN and \
    posicion[1] > MARGEN and posicion[1] < mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res= True       
    
    return res
    
#Devuelve si se ha pulsado algún botón
def pulsaBoton(mapi, posicion):
    res=-1
    
    if posicion[0] > (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2-65 and posicion[0] < (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2-15 and \
       posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res=1
    elif posicion[0] > (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2+15 and posicion[0] < (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2+65 and \
       posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res=2

    return res
   
# Construye la matriz para guardar el camino
def inic(mapi):    
    cam=[]
    for i in range(mapi.alto):        
        cam.append([])
        for j in range(mapi.ancho):            
            cam[i].append('.')
    
    return cam

def getkcal(cellId: int):
    return {ID_HIERBA: KCAL_HIERBA, ID_AGUA: KCAL_AGUA, ID_ROCA: KCAL_ROCA}[cellId]


def getFrontier(padre: Nodo, mapi: Mapa, f_list: list, in_list: list, dst: Casilla) -> [Nodo]:
    frontier = []
    for pos in padre.pos.getFrontier() :
        if pos.fila < mapi.alto and pos.col < mapi.ancho and pos.col >= 0 and pos.fila >= 0 and mapi.getCelda(*pos.toTuple()) != ID_MURO :
            hijo = Nodo(pos, g(pos, mapi, padre), h_euclidean(pos, dst), getkcal(mapi.getCelda(*pos.toTuple())), padre)
            if hijo not in f_list and hijo.pos not in in_list and hijo.doesNotLoop():
                frontier.append(hijo)
    return frontier

# Returns -1 if the index is not found instead of throwing an exception
def noexceptIndex(l: list, elem) -> int :
    idx = 0
    for obj in l :
        if elem == obj :
            return idx
        idx += 1
    
    return -1 # Nothing found

def g(pos: Casilla, mapi: Mapa, padre: Nodo = None):
    if padre is not None :
        return (1.5 if padre.pos.col - pos.col + padre.pos.fila - pos.fila in [2, 0, -2] else 1) + padre.g # Diagonal: 1.5, No diagonal: 1
    else :
        return 0 # Orphan position is initial

def h_manhattan(orig: Casilla, dst: Casilla):
    return abs(orig.col - dst.col) + abs(orig.fila - dst.fila)


def h_euclidean(orig: Casilla, dst: Casilla):
    return math.sqrt(pow(orig.col - dst.col, 2) + pow(orig.fila - dst.fila, 2))


# Devuelve la menor de las distancias, sea la horizontal o la vertical
# Es menos admisible que la de manhattan o la euclidea porque es menos precisa
def h_custom(orig: Casilla, dst: Casilla):
    return min(abs(orig.fila - dst.fila), abs(orig.col - dst.col))

def a_star(mapi: Mapa, origen: Casilla, destino: Casilla, camino: list) : # -> coste, kcal
    Nodo.setRegularCmpMode()
    in_list = {}
    f_list = [Nodo(origen, g(origen, mapi), h_euclidean(origen, destino), getkcal(mapi.getCelda(*origen.toTuple())))]
    
    while f_list:
        n = heappop(f_list)
        if n.pos == destino :
            m = n
            while m != None :
                camino[m.pos.fila][m.pos.col] = 'x'
                m = m.parent

            return n.f, n.kcal
        else :
            in_list[n.pos] = n
            n.children = getFrontier(n, mapi, f_list, in_list, destino)

            for fnode in n.children :
                idx = noexceptIndex(f_list, fnode)
                if idx == -1 :
                    heappush(f_list, fnode)
                elif fnode.f < f_list[idx].f :
                    f_list[idx] = fnode
                    heapify(f_list) # O(n)

    return -1, -1 # No solution


def a_star_epsilon(mapi: Mapa, origen: Casilla, destino: Casilla, camino: list):
    Nodo.setEpsilonCmpMode()
    in_list = {}
    f_list = []
    focal_list = [Nodo(origen, g(origen, mapi), h_euclidean(origen, destino), getkcal(mapi.getCelda(*origen.toTuple())))]
    
    while focal_list:
        n = heappop(focal_list) # Kcal heuristic based pop
        if n.pos == destino :
            m = n
            while m != None :
                camino[m.pos.fila][m.pos.col] = 'x'
                m = m.parent

            return n.f, n.kcal
        else :
            in_list[n.pos] = n
            n.children = getFrontier(n, mapi, f_list, in_list, destino)

            # Add children to frontier list
            Nodo.setRegularCmpMode()
            for fnode in n.children :
                idx = noexceptIndex(f_list, fnode)
                if idx == -1 :
                    heappush(f_list, fnode)
                elif fnode.f < f_list[idx].f :
                    f_list[idx] = fnode
                    heapify(f_list)
            Nodo.setEpsilonCmpMode()
            if not f_list: continue

            # Add elements to focal list
            min_node = f_list[0]
            i = 0
            while i < len(f_list):
                if f_list[i].f <= ((1 + EPSILON) * min_node.f):
                    heappush(focal_list, f_list.pop(i))
                    i -= 1
                i+= 1

    return -1, -1 # No solution


# función principal
def main():
    pygame.init()    
    
    reloj=pygame.time.Clock()
    
    if len(sys.argv)==1: #si no se indica un mapa coge mapa.txt por defecto
        file='mapa.txt'
    else:
        file=sys.argv[-1]
         
    mapi=Mapa(file)     
    camino=inic(mapi)   
    
    anchoVentana=mapi.getAncho()*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN    
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension)
    pygame.display.set_caption("Practica 1")
    
    boton1=pygame.image.load("boton1.png").convert()
    boton1=pygame.transform.scale(boton1,[50, 30])
    
    boton2=pygame.image.load("boton2.png").convert()
    boton2=pygame.transform.scale(boton2,[50, 30])
    
    personaje=pygame.image.load("rabbit.png").convert()
    personaje=pygame.transform.scale(personaje,[TAM, TAM])
    
    objetivo=pygame.image.load("carrot.png").convert()
    objetivo=pygame.transform.scale(objetivo,[TAM, TAM])
    
    coste=-1
    cal=0
    running= True    
    origen=Casilla(-1,-1)
    destino=Casilla(-1,-1)
    
    while running:        
        #procesamiento de eventos
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                running=False 
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()      
                if pulsaBoton(mapi, pos)==1 or pulsaBoton(mapi, pos)==2:
                    if origen.getFila()==-1 or destino.getFila()==-1:
                        print('Error: No hay origen o destino')
                    else:
                        camino=inic(mapi)
                        if pulsaBoton(mapi, pos)==1:
                            coste, cal = a_star(mapi, origen, destino, camino)
                            if coste==-1:
                                print('Error: No existe un camino válido entre origen y destino')
                        else:
                            coste, cal = a_star_epsilon(mapi, origen, destino, camino)
                            if coste==-1:
                                print('Error: No existe un camino válido entre origen y destino')
                            
                elif esMapa(mapi,pos):                    
                    if event.button==1: #botón izquierdo                        
                        colOrigen=pos[0]//(TAM+MARGEN)
                        filOrigen=pos[1]//(TAM+MARGEN)
                        casO=Casilla(filOrigen, colOrigen)                        
                        if bueno(mapi, casO):
                            origen=casO
                        else: # se ha hecho click en una celda no accesible
                            print('Error: Esa casilla no es válida')
                    elif event.button==3: #botón derecho
                        colDestino=pos[0]//(TAM+MARGEN)
                        filDestino=pos[1]//(TAM+MARGEN)
                        casD=Casilla(filDestino, colDestino)                        
                        if bueno(mapi, casD):
                            destino=casD
                        else: # se ha hecho click en una celda no accesible
                            print('Error: Esa casilla no es válida')         
        
        #código de dibujo        
        #limpiar pantalla
        screen.fill(NEGRO)
        #pinta mapa
        for fil in range(mapi.getAlto()):
            for col in range(mapi.getAncho()):                
                if camino[fil][col]!='.':
                    pygame.draw.rect(screen, AMARILLO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapi.getCelda(fil,col)==0:
                    pygame.draw.rect(screen, HIERBA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapi.getCelda(fil,col)==4:
                    pygame.draw.rect(screen, AGUA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapi.getCelda(fil,col)==5:
                    pygame.draw.rect(screen, ROCA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)                                    
                elif mapi.getCelda(fil,col)==1:
                    pygame.draw.rect(screen, MURO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    
        #pinta origen
        screen.blit(personaje, [(TAM+MARGEN)*origen.getCol()+MARGEN, (TAM+MARGEN)*origen.getFila()+MARGEN])        
        #pinta destino
        screen.blit(objetivo, [(TAM+MARGEN)*destino.getCol()+MARGEN, (TAM+MARGEN)*destino.getFila()+MARGEN])       
        #pinta botón
        screen.blit(boton1, [anchoVentana//2-65, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        screen.blit(boton2, [anchoVentana//2+15, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        #pinta coste y energía
        if coste!=-1:            
            fuente= pygame.font.Font(None, 25)
            textoCoste=fuente.render("Coste: "+str(coste), True, AMARILLO)            
            screen.blit(textoCoste, [anchoVentana-90, mapi.getAlto()*(TAM+MARGEN)+MARGEN+15])
            textoEnergía=fuente.render("Cal: "+str(cal), True, AMARILLO)
            screen.blit(textoEnergía, [5, mapi.getAlto()*(TAM+MARGEN)+MARGEN+15])
            
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)
        
    pygame.quit()


#---------------------------------------------------------------------
if __name__=="__main__":
    main()
