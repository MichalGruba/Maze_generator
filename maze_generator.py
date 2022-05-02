import numpy
from numpy.random import randint as rand
import matplotlib.pyplot as pyplot

columns = 30
rows = 30


class Triangle:
    def __init__(self, x, y, r, ix, iy):
        self.s = [x, y]
        if (ix % 2 == 0 and iy % 2 == 0) or (ix % 2 != 0 and iy % 2 != 0):
            p1 = [x, y + r]
            p2 = [x + r, y - r]
            p3 = [x - r, y - r]
            self.direction = 'up'
        else:
            p1 = [x, y - r]
            p2 = [x + r, y + r]
            p3 = [x - r, y + r]
            self.direction = 'down'
        px = [p1[0], p2[0], p3[0], p1[0]]
        py = [p1[1], p2[1], p3[1], p1[1]]
        self.lx = []
        self.ly = []
        sides = 3
        for i in range(sides):
            self.lx.append([px[i], px[i + 1]])
            self.ly.append([py[i], py[i + 1]])
        if not (ix == columns - 1):
            self.lx[0] = []
            self.ly[0] = []
        if not (iy == 0 or self.direction == 'down'):
            self.lx[1] = []
            self.ly[1] = []
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
        self.paths = []


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


def alg(hx):
    x, y = rand(0, columns - 1), rand(0, rows - 1)
    visited = [[x, y]]
    backtrack = [[x, y]]
    path = []
    while len(visited) != rows * columns:
        if len(hx[x][y].neighbours) != 0:
            rdn = rand(0, len(hx[x][y].neighbours))
            if not ([hx[x][y].neighbours[rdn][1], hx[x][y].neighbours[rdn][0]] in visited):
                visited.append([hx[x][y].neighbours[rdn][1], hx[x][y].neighbours[rdn][0]])
                backtrack.append([hx[x][y].neighbours[rdn][1], hx[x][y].neighbours[rdn][0]])
                a = hx[x][y].neighbours[rdn][1]
                b = hx[x][y].neighbours[rdn][0]
                remove(x, y, a, b, hx)
                hx[x][y].paths.append(hx[x][y].neighbours.pop(rdn))
                x, y = a, b
                path.append([x, y])
                continue
            else:
                hx[x][y].paths.append(hx[x][y].neighbours.pop(rdn))
                continue
        else:
            x, y = backtrack[-2][0], backtrack[-2][1]
            path.append([x, y])
            del backtrack[-1]
            continue


r = 2
triangles = []
temp = []
k = 0
a = 1
for i in range(rows):
    for j in range(columns):
        if j % 2 == 0:
            temp.append(Triangle(a + j * r, 1 + 2 * i * r, r, j, i))
        else:
            temp.append(Triangle(a + j * r, 1 + 2 * i * r, r, j, i))
    triangles.append(temp)
    if i % 2 == 0:
        k = k + 1
        a = 1
    else:
        a = 1
    temp = []
alg(triangles)
yy = 1

while yy % 2 != 0:
    yy, xx = rand(0, columns - 1), 0
triangles[xx][yy].lx[1] = []
triangles[xx][yy].ly[1] = []
px = [xx]
py = [yy]
yy = 1

while yy % 2 != 0:
    yy, xx = rand(0, columns - 1), rows - 1
triangles[xx][yy].lx[1] = []
triangles[xx][yy].ly[1] = []

for k in range(rows):
    for j in range(columns):
        for i in range(triangles[k][j].lx.__len__()):
            pyplot.plot(triangles[k][j].lx[i], triangles[k][j].ly[i], color='blue')
pyplot.show()
