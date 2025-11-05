# models/threat.py
import numpy as np

class Threat:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.detected = False
        self.neutralized = False

    @staticmethod
    def generate_random(area_size, count):
        return [Threat(i, np.random.randint(0, area_size), np.random.randint(0, area_size)) for i in range(count)]

    def position(self):
        return (self.x, self.y)

    def is_near(self, x, y, radius):
        return np.linalg.norm(np.array([self.x, self.y]) - np.array([x, y])) <= radius