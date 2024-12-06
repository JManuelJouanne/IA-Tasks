from binary_heap import BinaryHeap
from node import Node
import time

class EarlyAstar:
    def __init__(self, initial_state, heuristic, weight=1):
        self.expansions = 0
        self.generated = 0
        self.initial_state = initial_state
        self.weight = weight
        self.heuristic = heuristic
        self.solution = None
        self.U = float('inf')  # Valor de U inicial (infinito)

    def search(self):
        self.start_time = time.process_time()
        
        self.open = BinaryHeap()
        
        initial_node = Node(self.initial_state)
        initial_node.g = 0
        initial_node.h = self.heuristic(self.initial_state)
        # initial_node.key = 10000*self.weight*initial_node.h  # asignamos el valor f
        initial_node.key = self.weight*initial_node.h  # asignamos el valor f
        self.open.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        while not self.open.is_empty():
            n = self.open.extract()   # extrae n de la open
            if self.U < n.key:
                self.end_time = time.process_time()
                return self.solution

            succ = n.state.successors()
            self.expansions += 1
            for child_state, action, cost in succ:
                child_node = self.generated.get(child_state)
                is_new = child_node is None  # es la primera vez que veo a child_state
                path_cost = n.g + cost  # costo del camino encontrado hasta child_state
                if is_new or path_cost < child_node.g:
                    if is_new:
                        child_node = Node(child_state)
                        child_node.h = self.heuristic(child_state)
                        self.generated[child_state] = child_node

                    if child_state.is_goal() and path_cost < self.U:
                        self.U = path_cost
                        self.solution = child_node
                    
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.key = child_node.g + self.weight*child_node.h
                    child_node.action = action
                    self.open.insert(child_node)

        self.end_time = time.process_time()
        return None