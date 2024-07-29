import numpy as np
import pyglet as pg
n = {'s': 0}


class Shape:
    points = np.array([])
    lines = np.array([])

    def __init__(self, center=np.array([0, 0, 0]), theta=0.0, phi=0.0, name_points=True):
        labels = []
        if name_points:
            id = chr(ord('a')+n['s'])
            n['s'] += 1
            for i in range(len(self.points)):
                labels += [id+str(i)]
        self.points = self.points@np.array([[1, 0, 0],
                                            [0, np.cos(theta), -np.sin(theta)],
                                            [0, np.sin(theta), np.cos(theta)]
                                            ])
        self.points = self.points@np.array([[np.cos(phi), 0, np.sin(phi)],
                                            [0, 1, 0],
                                            [-np.sin(phi), 0, np.cos(phi)]
                                            ])
        self.points = self.points + center
        self.labels = np.array(labels)


class Cube(Shape):
    def __init__(self, center=np.array([0, 0, 0]), side_length=300, theta=0.0, phi=0.0):
        points = []
        poss = [side_length/2, -side_length/2]
        for i in poss:
            for j in poss:
                for k in poss:
                    points += [[i, j, k]]
        points = np.array(points)
        points = points
        lines = []
        for i in range(len(points)):
            for j in range(len(points)):
                if (((points[i]==points[j])*1).sum()==2) and i<j:
                    lines += [[i, j]]
        self.points = np.array(points)
        self.lines = np.array(lines)
        super(Cube, self).__init__(center, theta, phi)


class GeneralCylinder(Shape):
    def __init__(self, points=np.array([]), connections=np.array([]), h=10, center=np.array([0, 0, 0]), theta=0.0, phi=0.0):
        pn = points.tolist()
        print(pn)
        super(GeneralCylinder, self).__init__(center, theta, phi)

class Cylinder:
    def __init__(self):
        pass

def top_down_projection(self, px, py, pz, h_obs=1000, h_scr=900, zoom=5):
    ratio = (h_obs-h_scr)/(h_obs - pz)
    return np.array([px*ratio,py*ratio])*zoom


class MeshView(pg.window.Window):
    points = np.array([])
    lines = np.array([])
    labels = np.array([])
    shapes = []
    projecion = top_down_projection

    def __init__(self):
        super(MeshView, self).__init__()
        self.mov = np.array([0, 0, 0])
        self.rot = np.array([[1, 0, 0],
                             [0, 1, 0],
                             [0, 0, 1]])
        self.set_caption("Mesh Viewer")
        self.maximize()
        self.show_labels=False
        self.show_pos=False

    def plot(self):
        points = (self.projecion(self.points[:,0], self.points[:,1], self.points[:, 2])).transpose()
        mid = np.array([self.width//2, self.height//2])
        points = points+mid
        for i in self.lines:
            pg.shapes.Line(*points[i].flatten().tolist(),width=1).draw()
        if self.show_labels:
            if self.show_pos:
                for i in range(len(points)):
                    pg.text.Label(self.labels[i]+': '+str(np.round(self.points[i])),
                                  x=points[i][0]+5,
                                  y=points[i][1]+5,
                                  font_size=10).draw()
            else:
                for i in range(len(points)):
                    pg.text.Label(self.labels[i],
                                  x=points[i][0]+5,
                                  y=points[i][1]+5,
                                  font_size=7).draw()

    def __build_mesh__(self):
        points = []
        lines = []
        labels = []
        for i in self.shapes:
            lines += (i.lines + len(points)).tolist()
            points += i.points.tolist()
            labels += i.labels.tolist()
        self.points = np.array(points)
        self.lines = np.array(lines)
        self.labels = np.array(labels)
        self.plot()

    def on_draw(self):
        self.clear()
        self.plot()

    def move(self, t):
        self.points = self.points + np.array(self.mov)
        self.points = self.points@self.rot
        self.on_draw()

    def on_key_press(self, symbol, modifiers):
        v = 20
        w = np.pi/16
        if modifiers == 1:
            if symbol==119:
                self.rot = np.array([[1, 0, 0],
                                     [0, np.cos(w), -np.sin(w)],
                                     [0, np.sin(w), np.cos(w)]
                                     ])
            elif symbol==97:
                self.rot = np.array([[np.cos(w), 0, np.sin(w)],
                                    [0, 1, 0],
                                    [-np.sin(w), 0, np.cos(w)]
                                    ])
            elif symbol==115:
                self.rot = np.array([[1, 0, 0],
                                     [0, np.cos(w), np.sin(w)],
                                     [0, -np.sin(w), np.cos(w)]
                                     ])
            elif symbol==100:
                self.rot = np.array([[np.cos(w), 0,  -np.sin(w)],
                                    [0, 1, 0],
                                    [np.sin(w), 0, np.cos(w)]
                                    ])
        else:
            if symbol==119:
                self.mov[1] = -v
            elif symbol==97:
                self.mov[0] = v
            elif symbol==115:
                self.mov[1] = v
            elif symbol==100:
                self.mov[0] = -v
            elif symbol == pg.window.key.I:
                self.mov[2] = v
            elif symbol == pg.window.key.O:
                self.mov[2] = -v
            elif symbol == pg.window.key.L:
                self.show_labels = not self.show_labels
            elif symbol == pg.window.key.P:
                self.show_pos = not self.show_pos
        self.plot()

    def on_key_release(self, symbol, modifiers):
        if symbol==119:
            self.mov[1] = 0
        elif symbol==97:
            self.mov[0] = 0
        elif symbol==115:
            self.mov[1] = 0
        elif symbol==100:
            self.mov[0] = 0
        elif symbol == pg.window.key.I:
            self.mov[2] = 0
        elif symbol == pg.window.key.O:
            self.mov[2] = 0
        self.rot = np.array([[1, 0, 0],
                             [0, 1, 0],
                             [0, 0, 1]])

    def __run__(self):
        pg.app.run()


run = True
if run:
    w = MeshView()
    n_box = 3
    for i in np.arange(n_box)*2*np.pi/n_box:
        w.shapes += [Cube(np.array([300*np.cos(i), 300*np.sin(i), 0]), side_length=200, theta=-i, phi=np.pi/2)]
    w.__build_mesh__()
    pg.clock.schedule_interval(w.move, .1)
    w.__run__()

