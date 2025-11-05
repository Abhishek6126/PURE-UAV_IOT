# simulation/simulation_manager.py
import numpy as np
from models.iot_device import IoTDevice
from models.uav_node import UAV
from models.threat import Threat
from mpc.predictor import GMMPredictor
from mpc.mpc_controller import MPCController
from offloading.offloading_manager import OffloadingManager
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

class DecentralizedUAVSystem:
    def __init__(self, config):
        self.mode = config.get("mode", "hybrid")  # default is hybrid
        self.config = config
        self.area_size = config['area_size']
        self.time_slots = config['time_slots']

        # Adjusted wave frequency for a smoother border line
        self.devices = []
        self.border_path = sorted([(d.x, d.y) for d in self.devices], key=lambda p: p[0])
        for i in range(config['iot']['device_count']):
            x = int(i * self.area_size / config['iot']['device_count'])
            y_offset = 10 * np.sin(i / 15.0)  # Lower frequency wave
            y = int(self.area_size // 2 + y_offset + np.random.randint(-2, 3))
            self.devices.append(IoTDevice(
                id=i,
                x=np.clip(x, 0, self.area_size - 1),
                y=np.clip(y, 0, self.area_size - 1),
                battery=np.random.uniform(*config['iot']['battery_range']),
                sensing_range=config['iot']['sensing_range']
            ))

        # Increase UAV count to 3
        self.uavs = [
            UAV(id=j,
                x=int(self.area_size // 4 * (j + 1)),
                y=self.area_size // 2,
                battery=config['uav']['battery'],
                hover_time=config['uav']['hover_time'])
            for j in range(3)
        ]
        self.border_path = sorted([(d.x, d.y) for d in self.devices], key=lambda p: p[0])
        total_points = len(self.border_path)
        num_uavs = len(self.uavs)
        segment_size = max(1, total_points // num_uavs)

        self.uav_patrol_paths = []

        for i in range(num_uavs):
            start = i * segment_size
            end = min((i + 1) * segment_size, total_points)
            path = self.border_path[start:end]

            # Fallback to entire border if segment is empty
            if not path:
                path = self.border_path

            self.uav_patrol_paths.append(path)

        for i in range(num_uavs):
            start = i * segment_size
            end = (i + 1) * segment_size if i != num_uavs - 1 else len(self.border_path)
            path = self.border_path[start:end]
            self.uav_patrol_paths.append(path)

        # Fewer threats and closer to the border
        self.threats = []
        if self.mode != "ecop":  # Skip threats if in ECOP mode
            for i in range(self.config['threats']['count']):
                side = np.random.choice(['top', 'bottom'])
                x = np.random.randint(0, self.area_size)
                y = np.random.randint(self.area_size // 2 - 20, self.area_size // 2 - 10) if side == 'bottom' else np.random.randint(self.area_size // 2 + 10, self.area_size // 2 + 20)
                self.threats.append(Threat(id=i, x=x, y=y))


        self.gmm = GMMPredictor()
        self.controller = MPCController(self.devices, self.uavs, config, self.gmm)
        self.offloader = OffloadingManager(self.uavs, config)

        self.metrics = {
            'energy_efficiency': [],
            'total_energy': [],
            'threats_handled': []
        }

        self.visual_frames = []

    def run_simulation(self):
        for t in range(self.time_slots):
            print(f"[TIME {t}] Running MPC optimization...")
            actual_energy_data = {d.id: np.random.uniform(0.5, 3.0) for d in self.devices}
            self.controller.update_energy_history(actual_energy_data)
            assignments, active_devices = self.controller.optimize()
            for idx, uav in enumerate(self.uavs):
                path = self.uav_patrol_paths[idx]
                pos = path[t % len(path)]  # loop over segment
                uav.x, uav.y = pos
            if self.mode != "mpc-only":  # Don't offload in MPC-only
                for device in active_devices:
                    task = device.generate_task()
                    self.offloader.assign_task(device, task)


            neutralized = 0
            if self.mode != "ecop":  # No threat logic in ECOP
                for threat in self.threats:
                    if not threat.neutralized:
                        direction = -1 if threat.y > self.area_size // 2 else 1
                        threat.y = np.clip(threat.y + direction * np.random.randint(1, 4), 0, self.area_size - 1)
                        threat.x = np.clip(threat.x + np.random.randint(-2, 3), 0, self.area_size - 1)

                for threat in self.threats:
                    if not threat.neutralized:
                        for uav in self.uavs:
                            if threat.is_near(uav.x, uav.y, self.config['uav']['service_range']):
                                threat.neutralized = True
                                neutralized += 1
                                break


            energy_spent = sum([d.energy for d in self.devices]) + sum([u.energy for u in self.uavs])
            served_devices = len(active_devices)

            if energy_spent > 0:
                self.metrics['energy_efficiency'].append(served_devices / energy_spent)
            else:
                self.metrics['energy_efficiency'].append(0)

            self.metrics['threats_handled'].append(neutralized)
            self.metrics['total_energy'].append(energy_spent)

            self.visual_frames.append({
                'uavs': [(uav.x, uav.y) for uav in self.uavs],
                'devices': [(d.x, d.y) for d in self.devices],
                'threats': [(th.x, th.y, th.neutralized) for th in self.threats]
            })

        return self.metrics

    def visualize(self):
        if self.mode == "ecop":
            return  # Skip animation for ECOP

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_xlim(0, self.area_size)
        ax.set_ylim(0, self.area_size)
        ax.set_title("UAV-IoT Threat Simulation")

        device_scatter = ax.scatter([], [], c='red', label='IoT Devices')
        uav_scatter = ax.scatter([], [], c='blue', marker='^', label='UAVs')
        threat_scatter = ax.scatter([], [], c='purple', marker='x', label='Threats')
        neutralized_scatter = ax.scatter([], [], c='green', marker='x', label='Neutralized')
        for uav in self.uavs:
            ax.text(uav.x, uav.y + 2, f"UAV-{uav.id}", color='blue', fontsize=8)
        def update(frame_idx):
            frame = self.visual_frames[frame_idx]

            device_data = np.array(frame['devices']) if frame['devices'] else np.empty((0, 2))
            uav_data = np.array(frame['uavs']) if frame['uavs'] else np.empty((0, 2))

            threats_active = [p[:2] for p in frame['threats'] if not p[2]]
            threats_neutralized = [p[:2] for p in frame['threats'] if p[2]]

            threat_data = np.array(threats_active) if threats_active else np.empty((0, 2))
            neutralized_data = np.array(threats_neutralized) if threats_neutralized else np.empty((0, 2))

            device_scatter.set_offsets(device_data)
            uav_scatter.set_offsets(uav_data)
            threat_scatter.set_offsets(threat_data)
            neutralized_scatter.set_offsets(neutralized_data)

            return device_scatter, uav_scatter, threat_scatter, neutralized_scatter

        ani = animation.FuncAnimation(fig, update, frames=len(self.visual_frames), interval=1000, repeat=False)
        ax.legend()
        plt.show()

        
        from matplotlib.animation import PillowWriter
        ani.save("results/simulation.gif", writer=PillowWriter(fps=1))
        plt.show()

