# offloading/offloading_manager.py

class OffloadingManager:
    def __init__(self, uavs, config):
        self.uavs = uavs
        self.config = config

    def assign_task(self, device, task):
        """Assign a task to a UAV based on distance and load (simplified ECOP logic)."""
        best_uav = min(
            self.uavs,
            key=lambda u: ((u.x - device.x) ** 2 + (u.y - device.y) ** 2)
                          + (100 - u.energy)  # penalize low energy UAVs
        )
        distance = device.distance_to(best_uav.x, best_uav.y)
        if distance <= self.config['uav']['service_range']:
            # Assume offloading accepted
            best_uav.energy -= 0.5  # Offloading cost
            return best_uav.id
        return None
