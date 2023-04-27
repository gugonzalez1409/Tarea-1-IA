import random #para elegir sucesor aleatorio DFS
import queue #para implementar costo uniforme y a*

class Nodo:
    def __init__(self, nombre, heuristica, hijos=None, costos=None):
        self.nombre = nombre # nombre del nodo
        self.heuristica = heuristica # heuristica del nodo
        self.hijos = hijos or [] # lista de hijos
        self.costos = costos or [] # lista de costos por cada hijo
        self.expandido = 0 #contador de expansiones

    def agregar_hijo(self, hijo, costo):
        self.hijos.append(hijo) # añade los hijos del nodo
        self.costos.append(costo) # añade los costos correspondientes

def construir_arbol(init, goal, nodos, aristas):

    arbol = {} # diccionario que contiene todos los nodos
    for nombre, heuristica in nodos.items(): # crea los nodos del árbol
        arbol[nombre] = Nodo(nombre, heuristica)


    for inicio, destino, costo in aristas: # agrega las aristas a los nodos
        arbol[inicio].agregar_hijo(arbol[destino], costo)


    nodo_init = arbol[init] # asigna nodo inicial y destino
    nodo_goal = arbol[goal]

    return arbol, nodo_init, nodo_goal #retorna arbol completo, nodo inicio y nodo meta

#leer archivo y parsear
#grafo contiene todo el input
#nodos contiene el nombre de cada nodo con su heuristica
#ari contiene nodo origen, destino y costo
def leer_grafo(file):
    with open('input.txt', 'r') as f:
        grafo = f.readlines()

    init = grafo[0].split()[1]
    goal = grafo[1].split()[1]

    nodos = {}
    for line in grafo[2:10]:
        nom, heur = line.split()
        nodos[nom] = int(heur)

    ari = []
    for line in grafo[10:]:
        inicio, destino, costo = line.split(',')
        ari.append((inicio, destino, int(costo)))
    return init, goal, nodos, ari

#arbol, nodo_init, nodo_goal = construir_arbol(init, goal, nodos, ari)

# ALGORITMO DFS
caminoDFS = [] # lista que tendra camino recorrido para printear
def dfs(nodo_inicio, nodo_meta, costo, arbol):
    if nodo_inicio == nodo_meta: # cuando llega al nodo objetivo
        nodo_inicio.expandido += 1 # expande el nodo meta
        caminoDFS.append(nodo_inicio.nombre)
        printResultado(caminoDFS, costo, arbol)# imprime los resultados
        return
    else:
        nodo_inicio.expandido+=1 # expande nodo
        caminoDFS.append(nodo_inicio.nombre) # lo inserta en la ruta solucion
        hijos = nodo_inicio.hijos # busca los hijos
        if hijos:
            nodo_siguiente = random.choice(hijos) # elige un hijo al azar
            index_siguiente = hijos.index(nodo_siguiente) # consigue el indice del hijo
            costo_siguiente = nodo_inicio.costos[index_siguiente] # consigue el costo
            dfs(nodo_siguiente, nodo_meta, costo+costo_siguiente,arbol) # se vuelve a hacer el dfs con el hijo
        else:# en caso que no haya solucion
            return
# ALGORITMO GREEDY
caminoGreedy = [] # lista con solucion
def greedy(nodo_inicio, nodo_meta,costo, arbol):
    if nodo_inicio == nodo_meta: #condicion de termino
        nodo_inicio.expandido+=1
        caminoGreedy.append(nodo_inicio.nombre) # inserta el nodo meta a la lista
        printResultado(caminoGreedy, costo, arbol)
        return
    else:
        nodo_inicio.expandido+=1 # aumenta el contador de expansion del nodo
        caminoGreedy.append(nodo_inicio.nombre) # lo añade a la lista de la ruta solucion
        hijos = nodo_inicio.hijos # consigue lista de hijos del nodo
        if hijos:
            min = hijos[0].heuristica # para encontrar el valor menor de heuristica
            nodo_siguiente = hijos[0] # para almacenar el nodo siguiente
            for i in range(len(hijos)):
                if(min >= hijos[i].heuristica): #busca la menor heuristica de los hijos
                    nodo_siguiente = hijos[i]
            index_siguiente = hijos.index(nodo_siguiente) # consigue indice en la lista del nodo siguiente
            costo_siguiente = nodo_inicio.costos[index_siguiente] # consigue el costo
            greedy(nodo_siguiente, nodo_meta, costo+costo_siguiente,arbol) # vuelve a hacer la busqueda con el hijo
        else:
            return # no hay solucion

def costo_uniforme(nodo_inicio, nodo_meta, arbol):
    pq = queue.PriorityQueue()
    pq.put((0, nodo_inicio, []))# cola de prioridad con costo acumulado, nodo y lista para ir obteniendo ruta solucion
    while not pq.empty(): # mientras la cola no este vacia
        costo_actual, nodo_actual, camino = pq.get(0) # obtienes los costos y el nodo
        if nodo_actual == nodo_meta: # condicion de termino
            nodo_actual.expandido += 1 # expande nodod
            camino_final =  camino + [nodo_actual.nombre]# lo añade al camino
            printResultado(camino_final, costo_actual, arbol) # printea resultados
            return
        nodo_actual.expandido+=1 # expande el nodo
        for hijo, costo in zip(nodo_actual.hijos, nodo_actual.costos): # iterar en hijos y costos de nodo actual
            costo_nuevo = costo_actual + costo # actualiza el costo
            if hijo.expandido == 0 or hijo.costo_actual > costo_nuevo: # compara los costos para elegir camino
                hijo.costo_actual = costo_nuevo
            pq.put((int(costo_nuevo), hijo, camino + [nodo_actual.nombre])) # pone los valores en la pq
    return

def a_estrella(nodo_inicio, nodo_meta, arbol):
    pq = queue.PriorityQueue()
    pq.put((nodo_inicio.heuristica,0, nodo_inicio, [])) # pq con funcion = (costo + heuristica), costo acumulado, nodo inicial, y una lista para llevar camino solucion
    while not pq.empty():
        _, costo_actual, nodo_actual, camino = pq.get(0) # obtiene valores de la pq
        if nodo_actual == nodo_meta: # condicion de termino
            nodo_actual.expandido+=1 # expande nodo
            camino_final = camino + [nodo_actual.nombre] # añade nodo final a la solucion
            printResultado(camino_final, costo_actual,arbol) # imprime nodos
            return
        nodo_actual.expandido+=1 # expande el nodo
        for hijo, costo in zip(nodo_actual.hijos, nodo_actual.costos): #zip para iterar en hijos y costos
            costo_nuevo = costo_actual + costo
            if hijo.expandido == 0 or (costo_nuevo + hijo.heuristica) < hijo.costo_actual: # revisa si hijo a sido expandido y compara la suma del costo con la heuristica
                hijo.costo_actual = costo_nuevo # actualiza costo de hijo
                pq.put((costo_nuevo + hijo.heuristica, costo_nuevo, hijo, camino + [nodo_actual.nombre])) # añade en la pq
    return

def printResultado(camino=[], costo=[],arbol={}): #para imprimir los resultados en el formato pedido
    expandido = 0
    solucion = '->'.join(camino)
    print(solucion)
    print(costo)
    for i in arbol:
        expandido = expandido + arbol[i].expandido
        print(f"Nodo {i}: {arbol[i].expandido}")
    print("Total:", expandido)
    return


init, goal, nodos, ari = leer_grafo('input.txt')
arbol,nodo_init, nodo_goal = construir_arbol(init,goal,nodos,ari)
arbol2,nodo_init2, nodo_goal2 = construir_arbol(init,goal,nodos,ari)
arbol3,nodo_init3, nodo_goal3 = construir_arbol(init,goal,nodos,ari)
arbol4, nodo_init4, nodo_goal4 = construir_arbol(init,goal, nodos, ari)
print("ALGORITMO DFS:")
dfs(nodo_init, nodo_goal,0, arbol)
print("ALGORITMO GREEDY:")
greedy(nodo_init2, nodo_goal2,0, arbol2)
print("ALGORITMO COSTO UNIFORME:")
costo_uniforme(nodo_init3, nodo_goal3,arbol3)
print("ALGORITMO A*:")
a_estrella(nodo_init4,nodo_goal4,arbol4)
