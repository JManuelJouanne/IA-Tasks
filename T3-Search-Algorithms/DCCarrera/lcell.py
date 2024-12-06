import math


class LCell:
    def __init__(self, x, y, p, map):
        self.x = x
        self.y = y
        self.p = p 
        self.map = map
        self.sandCost = 1
        self.iceCost = -0.5

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and \
               self.map == other.map

    def __repr__(self):
        return str((self.x, self.y, self.p))

    def __str__(self):
        return str((self.x, self.y, self.p))

    def __hash__(self):
        return hash((self.x, self.y, self.p))
    
    def successors(self):
        succ = []
        current_x, current_y = self.x, self.y  # Pre-calcula los valores de la posición actual
        current_pose = self.p

        for old_pose, new_pose, endx, endy, cost, new_move in self.map.neighbors:
            if old_pose == current_pose:
                all_inside = True
                for r in new_move:  # r: relative position
                    if not self.map.inside(current_x + r[0], current_y + r[1]) or not self.map.line_of_sight(current_x, current_y, current_x + r[0], current_y + r[1]):
                        all_inside = False
                        break
                    if self.map.sand[current_x + r[0]][current_y + r[1]]:
                        cost += self.sandCost
                    elif self.map.ice[current_x + r[0]][current_y + r[1]]:
                        cost += self.iceCost

                if all_inside:
                    newx, newy = current_x + endx, current_y + endy
                    succ.append((LCell(newx, newy, new_pose, self.map), f'[{newx}, {newy}]', cost))
        return succ

    def is_goal(self):
        return self.x == self.map.goal_x and self.y == self.map.goal_y
