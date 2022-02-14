import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def NURBS(tt, x, y, z ,w, k):
    # knots vector
    t = []
    for i in range(len(listx) - k):
        t.append(i + 1)

    n = t[-1] + 1
    # Добавляем k -- degree раз нули и n -- size of control points в начало и конец соответственно
    # иначе кривая не будет доходить до последней контрольной точки и начинаться с первой
    for i in range(k):
        t.insert(0, 0)
        t.append(n)
    d = 0
    # индекс кривой Безье в котором лежит точка
    for i in range(len(t) - 1):
        if tt >= t[i] and tt < t[i + 1]:
            d = i
            break
    cx, cy, cz, cw = [], [], [], []

    for i in range(k):
        cx.append(x[d - i] * w[d - i])
        cy.append(y[d - i] * w[d - i])
        cz.append(z[d - i] * w[d - i])
        cw.append(w[d - i])
    # Вычисление basic function
    for r in range(k, 1, -1):
        i = d
        for s in range(r - 1):
            t_i = t[i]
            t_ij = t[i + r - 1]
            coef = (tt - t_i) / (t_ij - t_i)
            cx[s] = coef * cx[s] + (1 - coef) * cx[s + 1]
            cy[s] = coef * cy[s] + (1 - coef) * cy[s + 1]
            cz[s] = coef * cz[s] + (1 - coef) * cz[s + 1]
            cw[s] = coef * cw[s] + (1 - coef) * cw[s + 1]
            i = i - 1
    return (cx[0] / cw[0], cy[0] / cw[0], cz[0] / cw[0])


listx = [2, 3, 2, 4, 3, 4, 2]
listy = [2, 4, 1, 8, 4, 10, 5]
listz = [0, 2, 3, 6, 7, 8, 10]
listw = [1, 3, 1, 5, 1.3, 4, 1]
#listx = [2, 2, 2, 2, 2, 2]
#listy = [2, 4, 1, 8, 4, 10]
#listz = [0, 1, 2, 3, 4, 5]
#listw = [1, 3, 4, 5, 1.3, 4]

degree = 3
# количество кривых Безье (n + 1 - degree)
t = np.linspace(0, len(listx) - degree + 1 - 0.001, 100)

curve = [NURBS(i, listx, listy, listz, listw, degree) for i in t]
x, y, z = zip(*curve)

fig = plt.figure()
fig.subplots_adjust(bottom=0.3)
ax = fig.add_subplot(111, projection='3d')
plt.axis('off')
#ax.plot(x, y, z)

v = []
angles = np.linspace(0, 2*np.pi, 20)

for angle in angles:
    points = []
    for j in range(len(x)):
        points.append((x[j]*np.cos(angle) - y[j]*np.sin(angle), x[j]*np.sin(angle) - y[j]*np.cos(angle), z[j]))
    points = np.array(points)
    print(points[0])
    print(points[1])
    v.append(points)

verts = []

for i in range(len(v) - 1):
    for j in range(len(v[i])):
        verts.append([
            v[i][j], v[(i + 1) % len(v)][j],
            v[(i + 1) % len(v)][(j + 1) % len(v[i])],
            v[i][(j + 1) % len(v[i])]
        ])


ax.add_collection3d(Poly3DCollection(verts,  linewidths=1, edgecolor=(0, 1, 1), facecolor=(0, 0, 1)))
ax.set_xlim([-20, 20])
ax.set_ylim([-20, 20])
ax.set_zlim([-20, 20])


plt.show()
