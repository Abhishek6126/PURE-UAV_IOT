# models/uav_node.py
import numpy as np

class UAV:
    def __init__(self, id, x, y, battery, hover_time):
        self.id = id
        self.x = x
        self.y = y
        self.energy = battery
        self.hover_time = hover_time
        self.assigned_task = None

    def move_to(self, target_x, target_y):
        distance = np.linalg.norm(np.array([self.x, self.y]) - np.array([target_x, target_y]))
        self.x = target_x
        self.y = target_y
        self.energy -= distance * 0.1  # simple movement cost model
        return distance

    def can_reach(self, device, service_range):
        return device.distance_to(self.x, self.y) <= service_range