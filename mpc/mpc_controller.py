# mpc/mpc_controller.py
import numpy as np
from collections import defaultdict

class MPCController:
    def __init__(self, devices, uavs, config, gmm):
        self.devices = devices
        self.uavs = uavs
        self.config = config
        self.gmm = gmm
        self.history = defaultdict(list)

    def update_energy_history(self, actual_data):
        for device in self.devices:
            self.history[device.id].append(actual_data[device.id])
            if len(self.history[device.id]) > self.config['gmm']['history_window']:
                self.history[device.id].pop(0)
            self.gmm.train(device.id, self.history[device.id])

    def optimize(self):
        active_devices = [d for d in self.devices if self.gmm.predict(d.id) > self.config['offloading']['energy_threshold']]

        assignments = {}
        for uav in self.uavs:
            if not active_devices:
                break
            best_device = min(active_devices, key=lambda d: d.distance_to(uav.x, uav.y))
            uav.move_to(best_device.x, best_device.y)
            assignments[uav.id] = (best_device.x, best_device.y)

            # Service devices within range
            for d in active_devices:
                if uav.can_reach(d, self.config['uav']['service_range']):
                    d.energy -= self.config['offloading']['consumption_per_slot']
                    d.energy = max(0, d.energy)

        return assignments, active_devices