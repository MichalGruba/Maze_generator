import numpy as np
from numpy.random import randint as rand
import matplotlib.pyplot as plt

# size of the labyrinth
columns = 40
rows = 40


class Triangle:
    def __init__(self, ix, iy):
        # radius of circle around triangle
        self.r = 2
        # coordinates of circle center
        x = ix * self.r
        y = self.r + 2 * iy * self.r
        self.indices = [ix, iy]
        self.s = [x, y]
        self.h = 0
        self.g = 0
        self.f = 0
        self.parent = None
        # triangle points for triangle facing upwards
        if (ix % 2 == 0 and iy % 2 == 0) or (ix % 2 != 0 and iy % 2 != 0):
            p1 = [x, y + self.r]
            p2 = [x + self.r, y - self.r]
            p3 = [x - self.r, y - self.r]
            self.direction = 'up'
        # triangle points for triangle facing downwards
        else:
            p1 = [x, y - self.r]
            p2 = [x + self.r, y + self.r]
            p3 = [x - self.r, y + self.r]
            self.direction = 'down'

        # create the sides of the triangle
        p_x = [p1[0], p2[0], p3[0], p1[0]]
        p_y = [p1[1], p2[1], p3[1], p1[1]]
        self.lx = []
        self.ly = []
        sides = 3
        for m in range(sides):
            self.lx.append([p_x[m], p_x[m + 1]])
            self.ly.append([p_y[m], p_y[m + 1]])
        # remove the unnecessary sides
        if not (ix == columns - 1):
            self.lx[0] = []
            self.ly[0] = []
        if not (iy == 0 or self.direction == 'down'):
            self.lx[1] = []
            self.ly[1] = []
        # create a list of neighbouring triangles
        self.neighbours = []
        if self.direction == 'up':
            if ix > 0:
                self.neighbours.append([ix - 1, iy])
            if ix < columns - 1:
                self.neighbours.append([ix + 1, iy])
            if iy > 0:
                self.neighbours.append([ix, iy - 1])
        if self.direction == 'down':
            if ix > 0:
                self.neighbours.append([ix - 1, iy])
            if ix < columns - 1:
                self.neighbours.append([ix + 1, iy])
            if iy < rows - 1:
                self.neighbours.append([ix, iy + 1])
        self.all_neighbours = self.neighbours.copy()

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        return self.f == other.f

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __repr__(self):
        return str([self.indices, self.f])


# function removing the wall of a triangle
def remove(x1, y1, x2, y2, tr):
    dx = x2 - x1
    dy = y2 - y1
    if tr[x1][y1].direction == 'up' and dx == 0 and dy == 1:
        tr[x2][y2].lx[2] = []
        tr[x2][y2].ly[2] = []
    if tr[x1][y1].direction == 'up' and dx == 0 and dy == -1:
        tr[x1][y1].lx[2] = []
        tr[x1][y1].ly[2] = []
    if tr[x1][y1].direction == 'up' and dx == -1 and dy == 0:
        tr[x2][y2].lx[1] = []
        tr[x2][y2].ly[1] = []
    if tr[x1][y1].direction == 'down' and dx == 0 and dy == 1:
        tr[x2][y2].lx[2] = []
        tr[x2][y2].ly[2] = []
    if tr[x1][y1].direction == 'down' and dx == 0 and dy == -1:
        tr[x1][y1].lx[2] = []
        tr[x1][y1].ly[2] = []
    if tr[x1][y1].direction == 'down' and dx == 1 and dy == 0:
        tr[x1][y1].lx[1] = []
        tr[x1][y1].ly[1] = []


# removes one triangle side from top and bottom of the maze to create entrance and escape
def make_entrance(xx):
    yy = 1
    while yy % 2 != 0:
        yy = rand(0, columns - 1)
    triangles[xx][yy].lx[1] = []
    triangles[xx][yy].ly[1] = []

    return xx, yy


# function generating the labyrinth
def generate_lab(tr):
    x, y = rand(0, rows - 1), rand(0, columns - 1)
    visited = [[x, y]]
    backtrack = [[x, y]]
    while len(visited) != rows * columns:
        if len(tr[x][y].neighbours) != 0:
            rdn = rand(0, len(tr[x][y].neighbours))
            if not ([tr[x][y].neighbours[rdn][1], tr[x][y].neighbours[rdn][0]] in visited):
                visited.append([tr[x][y].neighbours[rdn][1], tr[x][y].neighbours[rdn][0]])
                backtrack.append([tr[x][y].neighbours[rdn][1], tr[x][y].neighbours[rdn][0]])
                b, a = tr[x][y].neighbours.pop(rdn)
                remove(x, y, a, b, tr)
                x, y = a, b
                continue
            else:
                tr[x][y].neighbours.pop(rdn)
                continue
        else:
            x, y = backtrack[-2][0], backtrack[-2][1]
            del backtrack[-1]
            continue


# generates a grid made of triangles
def generate_grid():
    triangle_list = np.empty((rows, columns), dtype=object)
    for r in range(rows):
        for c in range(columns):
            triangle_list[r, c] = Triangle(c, r)

    return triangle_list


# calculate distance between 2 tiles
def distance(p1, p2):
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


# checks if the neighbour is accessible/ there is no wall blocking it
def check_if_accessible(t1, t2, triangles_list):
    dy = t2[0] - t1[0]
    dx = t2[1] - t1[1]

    t1 = [i for i in triangles_list.reshape(-1) if t1 == i.indices][0]
    t2 = [i for i in triangles_list.reshape(-1) if t2 == i.indices][0]

    if t1.direction == 'up' and dy == 1 and t2.lx[2] == []:
        return True
    elif t1.direction == 'up' and dy == -1 and t1.lx[2] == []:
        return True
    elif t1.direction == 'up' and dx == -1 and t2.lx[1] == []:
        return True
    elif t1.direction == 'down' and dy == 1 and t2.lx[2] == []:
        return True
    elif t1.direction == 'down' and dy == -1 and t1.lx[2] == []:
        return True
    elif t1.direction == 'down' and dx == 1 and t1.lx[1] == []:
        return True

    return False


# A* algorithm implementation to solve the labyrinth
def a_star(start, goal, triangles_list):
    open_nodes = set()
    closed = set()

    open_nodes.add(triangles_list[start[0]][start[1]])
    goal = [list(goal)[1], list(goal)[0]]
    print(start, goal)
    while len(open_nodes) != 0:
        open_nodes = set(sorted(open_nodes, key=lambda x: x.f))
        current = open_nodes.pop()
        closed.add(current)

        if current.indices == goal:
            solution_path = []
            curr = current
            radius = curr.r
            exit_point = curr.s.copy()
            exit_point[1] += radius
            solution_path.append(exit_point)
            while curr is not None:
                solution_path.append(curr.s)
                curr = curr.parent

            entrance_point = solution_path[-1].copy()
            entrance_point[1] -= radius
            solution_path.append(entrance_point)
            return solution_path[::-1]

        neighbours = current.all_neighbours
        for neighbour in neighbours:
            if not check_if_accessible(current.indices, neighbour, triangles_list):
                neighbours = [i for i in neighbours if i != neighbour]

        for pos in neighbours:
            child = [i for i in triangles_list.reshape(-1) if pos == i.indices][0]
            if child in closed:
                continue

            child.parent = current
            child.g = current.g + distance(current.s, child.s)
            child.h = distance(child.s, goal)
            child.f = child.g + child.h

            open_nodes.add(child)


# displays the labyrinth
def display(triangles_list):
    for k in range(rows):
        for j in range(columns):
            for i in range(triangles_list[k][j].lx.__len__()):
                plt.plot(triangles_list[k][j].lx[i], triangles_list[k][j].ly[i], color='blue')
    plt.show()


if __name__ == '__main__':
    # generate the grid made of triangles
    triangles = generate_grid()

    # carve the labyrinth on the grid
    generate_lab(triangles)

    # choose starting and ending point
    start_point = make_entrance(0)
    end_point = make_entrance(rows - 1)

    # draw the solution
    path = a_star(start_point, end_point, triangles)
    path = np.array(path)
    plt.plot(path[:, 0], path[:, 1])

    # draw the maze
    display(triangles)

