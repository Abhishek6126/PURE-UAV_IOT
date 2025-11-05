# models/iot_device.py
import numpy as np

class IoTDevice:
    def __init__(self, id, x, y, battery, sensing_range):
        self.id = id
        self.x = x
        self.y = y
        self.energy = battery
        self.sensing_range = sensing_range
        self.active = True

    def generate_task(self):
        return {
            'device_id': self.id,
            'position': (self.x, self.y),
            'data_size': np.random.randint(10, 100),  # in MB
            'urgency': np.random.choice(['low', 'medium', 'high'])
        }

    def distance_to(self, x, y):
        return np.linalg.norm(np.array([self.x, self.y]) - np.array([x, y]))


