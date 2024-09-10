import os
import time
import numpy as np
import msvcrt

class ASCIIRenderer:
    def __init__(self, width=80, height=60):
        self.width = width
        self.height = height
        self.buffer = [[" " for _ in range(width)] for _ in range(height)]

    def clear_buffer(self):
        self.buffer = [[" " for _ in range(self.width)] for _ in range(self.height)]

    def render_line(self, p1, p2, char='#'):
        x1, y1 = p1
        x2, y2 = p2
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            if 0 <= x1 < self.width and 0 <= y1 < self.height:
                self.buffer[y1][x1] = char
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def render_face(self, points, char):
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            self.render_line(p1, p2, char)

    def fill_face(self, points, char):
        points = sorted(points, key=lambda p: p[1])
        if len(points) < 3:
            return
        y_min = points[0][1]
        y_max = points[-1][1]

        for y in range(y_min, y_max + 1):
            x_points = []
            for i in range(len(points)):
                p1 = points[i]
                p2 = points[(i + 1) % len(points)]
                if p1[1] <= y <= p2[1] or p2[1] <= y <= p1[1]:
                    if p1[1] != p2[1]:
                        x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) // (p2[1] - p1[1])
                        x_points.append(x)
            if len(x_points) >= 2:
                x_points.sort()
                self.render_line((x_points[0], y), (x_points[-1], y), char)

    def display(self):
        print("\n".join("".join(row) for row in self.buffer))

    def update(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display()


class Camera:
    def __init__(self, fov=70, pos=(0, 0, 0), yaw=0):
        self.fov = fov
        self.pos = np.array(pos)
        self.yaw = yaw

    def move_forward(self, distance):
        self.pos[0] += distance * np.sin(np.radians(self.yaw))
        self.pos[2] += distance * np.cos(np.radians(self.yaw))

    def move_backward(self, distance):
        self.move_forward(-distance)

    def turn_left(self, angle):
        self.yaw -= angle

    def turn_right(self, angle):
        self.yaw += angle

    def project(self, point):
        x, y, z = point - self.pos
        x_rot = x * np.cos(np.radians(self.yaw)) - z * np.sin(np.radians(self.yaw))
        z_rot = x * np.sin(np.radians(self.yaw)) + z * np.cos(np.radians(self.yaw))
        scale = 1 / max(z_rot, 0.1)
        x_screen = int(x_rot * scale * 40 + 40)
        y_screen = int(y * scale * 30 + 30)
        return x_screen, y_screen, z_rot


class Cube:
    def __init__(self, scale=(1, 1, 1), pos=(0, 0, 0)):
        self.scale = np.array(scale)
        self.pos = np.array(pos)
        self.vertices = self.generate_vertices()
        self.faces = self.generate_faces()

    def generate_vertices(self):
        sx, sy, sz = self.scale
        px, py, pz = self.pos
        return np.array([
            [px - sx, py - sy, pz - sz],
            [px + sx, py - sy, pz - sz],
            [px + sx, py + sy, pz - sz],
            [px - sx, py + sy, pz - sz],
            [px - sx, py - sy, pz + sz],
            [px + sx, py - sy, pz + sz],
            [px + sx, py + sy, pz + sz],
            [px - sx, py + sy, pz + sz],
        ])

    def generate_faces(self):
        return [
            [self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3]],
            [self.vertices[4], self.vertices[5], self.vertices[6], self.vertices[7]],
            [self.vertices[0], self.vertices[1], self.vertices[5], self.vertices[4]],
            [self.vertices[2], self.vertices[3], self.vertices[7], self.vertices[6]],
            [self.vertices[0], self.vertices[3], self.vertices[7], self.vertices[4]],
            [self.vertices[1], self.vertices[2], self.vertices[6], self.vertices[5]],
        ]


def get_key_press():
    if msvcrt.kbhit():
        return msvcrt.getch().decode('utf-8').lower()
    return None


def render_scene():
    screen = ASCIIRenderer(640, 360)
    camera = Camera(pos=(0, 0, 50))
    cube = Cube(scale=(10, 10, 10), pos=(0, 25, 100))
    shading_chars = ['.', '-', '+', '#']

    while True:
        key = get_key_press()
        if key == 'w':
            camera.move_forward(2)
        elif key == 's':
            camera.move_backward(2)
        elif key == 'a':
            camera.turn_left(5)
        elif key == 'd':
            camera.turn_right(5)

        screen.clear_buffer()

        for face in cube.faces:
            projected_points = [camera.project(vert) for vert in face]
            min_z = min(p[2] for p in projected_points)
            # Normalize the depth and ensure it stays within the bounds
            shade_index = max(0, min(len(shading_chars) - 1, int((min_z - 50) / 25)))
            screen.fill_face([p[:2] for p in projected_points], shading_chars[shade_index])

        screen.update()
        time.sleep(0.05)


if __name__ == "__main__":
    render_scene()
