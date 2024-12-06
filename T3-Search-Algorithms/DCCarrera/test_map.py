import json
import random
from map import Map
from lcell import LCell
from cell import Cell
from astar import Astar
from early_astar import EarlyAstar

def zero_heuristic(c):
    return 0

def manhattan_heuristic(c):
    return Map.manhattan(c.x, c.y, c.map.goal_x, c.map.goal_y)

def euclidian_heuristic(c):
    return Map.euclidian(c.x, c.y, c.map.goal_x, c.map.goal_y)

def octile_heuristic(c):
    return Map.octile(c.x, c.y, c.map.goal_x, c.map.goal_y)


############### Variables configurables ###########################
epsilon = 10                             # Variable epsilon de actividad 6 (2 es el valor estándar).
m = Map(epsilon, 'Maps/maze4.map')
connectivity = "primitiveFull"  # Las conectividades son int(4), int(8), "primitiveSimpleRight", "primitiveSimpleDiagonal", "primitiveFull"
primitivasActivated = True              # Estas usando alguna primitiva? Debe ser True en "primitiveSimpleRight", "primitiveSimpleDiagonal", "primitiveFull"
m.set_connectivity(connectivity)  
heuristic = manhattan_heuristic       # Cambia la heurística a utilizar
weight = 1                              # peso que usamos en la heuristica de A*
visualize = True                        # mostrar o no la solución?
num_probs = 10                           # numero de problemas que se ejecutan
algorithm = "Astar"                # "Astar" o "EarlyAstar"
random.seed(0)

############## No es necesario cambiar hacia abajo #############################
total_expansions = 0
total_generated = 0
total_cost = 0
total_time = 0
total_problems_solve = 0

print(' prob\t  #exp\t  #gen\t costo\t runtime')
results = []
while total_problems_solve < num_probs:
    while True:
        xi = random.randint(0, m.size_x-1)
        yi = random.randint(0, m.size_y-1)
        xg = random.randint(0, m.size_x-1)
        yg = random.randint(0, m.size_y-1)
        if m.map[xi][yi] and m.map[xg][yg]:
            m.init_x = xi
            m.init_y = yi
            m.goal_x = xg
            m.goal_y = yg
            break
    if connectivity == 8 or connectivity == 4:
        init = Cell(m.init_x, m.init_y, m)
    else:
        if connectivity == "primitiveSimpleRight":
            poses = [(0,1), (1,0), (0,-1), (-1,0)]
        else:
            poses = [(1,1), (-1,1), (1,-1), (-1,-1),(0,1), (1,0), (0,-1), (-1,0)]
        initial_pose = random.choice(poses)
        init = LCell(m.init_x, m.init_y, initial_pose, m)
    if algorithm == "Astar":
        s = Astar(init, heuristic, weight)
    elif algorithm == "EarlyAstar":
        s = EarlyAstar(init, heuristic, weight)
    
    result = s.search()
    if result:
        cost = result.g
    else:
        cost = -1
    print('{:5d}\t{:6d}\t{:6d}\t{:=6.2f}\t{:=5.2f}'.format(total_problems_solve+1, s.expansions, len(s.generated), cost, s.end_time-s.start_time))

    if result:
        total_cost += cost
        total_expansions += s.expansions
        total_time += s.end_time - s.start_time
        total_generated += len(s.generated)

        if primitivasActivated:
            path = [(int(c.x), int(c.y), c.p) for c in result.trace()]
        else:
            path = [(int(c.x), int(c.y)) for c in result.trace()]
        gen = set()
        for c in s.generated:
            gen.add((int(c.x), int(c.y)))

        if visualize:
            m.draw_solution(path, gen, primitives= primitivasActivated)

        # Guardar en JSON
        total_problems_solve +=1
        data = {
            "start": [int(m.init_x), int(m.init_y)],
            "goal": [int(m.goal_x), int(m.goal_y)],
            "path": path,
            "explored": list(gen),
            "cost": float(cost),
            "expansions": int(s.expansions),
            "generated": int(len(s.generated)),
            "runtime": float(s.end_time - s.start_time)
        }
        results.append(data)

        # for key, value in data.items():
        #     print(f"Key: {key}, Type: {value.__class__}, Value: {value}")                 
    
    else:
        print("No solution found...")



# Guardar todos los resultados en un archivo JSON
with open('output.json', 'w') as f:
    json.dump(results, f, indent=4)

print('Suma #exp:', total_expansions)
print('Suma #gen:', total_generated)
print('Suma cost:', round(total_cost, 2))
print('Runtime total: {:.2f} s'.format(total_time), "\n")

print(total_expansions)
print(total_generated)
print(round(total_cost, 2))
print('{:.2f}'.format(total_time))
