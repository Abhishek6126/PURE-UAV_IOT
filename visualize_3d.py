import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

def visualize_3d(frames, area_size, save_path="uav_simulation.gif"):
    """
    Creates a 3D animation of UAV movements over time.

    Args:
        frames (list): Collected frames from DecentralizedUAVSystem.visual_frames
        area_size (int): Size of the simulation area
        save_path (str): Path to save the 3D animation (gif or mp4)
    """
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlim(0, area_size)
    ax.set_ylim(0, area_size)
    ax.set_zlim(0, len(frames))   # Time as Z-axis
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Time")

    # Track UAV paths
    num_uavs = len(frames[0]['uavs'])
    uav_paths = [[] for _ in range(num_uavs)]
    scatters = [ax.plot([], [], [], 'o', label=f"UAV {i}")[0] for i in range(num_uavs)]

    def update(frame_idx):
        frame = frames[frame_idx]
        for i, (x, y) in enumerate(frame['uavs']):
            uav_paths[i].append((x, y, frame_idx))
            path = np.array(uav_paths[i])
            scatters[i].set_data(path[:, 0], path[:, 1])
            scatters[i].set_3d_properties(path[:, 2])
        return scatters

    ani = FuncAnimation(fig, update, frames=len(frames), interval=200, blit=False)
    plt.legend()
    plt.tight_layout()

    # Save animation
    if save_path.endswith(".gif"):
        ani.save(save_path, writer=PillowWriter(fps=20))
    elif save_path.endswith(".mp4"):
        ani.save(save_path, writer="ffmpeg")
    else:
        raise ValueError("Unsupported format. Use .gif or .mp4")

    print(f"✅ 3D animation saved at {save_path}")
    plt.show()
