# main.py

from simulation.simulation_manager import DecentralizedUAVSystem
from visualize_3d import visualize_3d
import matplotlib.pyplot as plt
import json
import os

def compute_percentage_gains(results_dict):
    hybrid = results_dict['PURE']
    ecop = results_dict['ECOP']
    mpc = results_dict['MPC-ONLY']

    def avg(lst): return sum(lst) / len(lst)

    gain_eff_ecop = ((avg(hybrid['energy_efficiency']) - avg(ecop['energy_efficiency'])) / avg(ecop['energy_efficiency'])) * 100
    gain_eff_mpc = ((avg(hybrid['energy_efficiency']) - avg(mpc['energy_efficiency'])) / avg(mpc['energy_efficiency'])) * 100

    gain_threats_ecop = 100 
    gain_threats_mpc = ((avg(hybrid['threats_handled']) - avg(mpc['threats_handled'])) / avg(mpc['threats_handled'])) * 100

    print("\n[PERFORMANCE GAIN OVER 10 RUNS]")
    print(f"Energy Efficiency Gain over ECOP: {gain_eff_ecop:.2f}%")
    print(f"Energy Efficiency Gain over MPC-ONLY: {gain_eff_mpc:.2f}%")
    print(f"Threat Neutralization Gain over ECOP: {gain_threats_ecop:.2f}%")
    print(f"Threat Neutralization Gain over MPC-ONLY: {gain_threats_mpc:.2f}%")


def plot_comparisons(results_dict):
    time_slots = list(range(len(next(iter(results_dict.values()))['energy_efficiency'])))
    os.makedirs("results", exist_ok=True)

    colors = {
        'PURE': 'green',
        'ECOP': 'skyblue',
        'MPC-ONLY': 'orange'
    }

    # --- Energy Efficiency ---
    plt.figure(figsize=(8, 5))
    for label, res in results_dict.items():
        plt.plot(
            time_slots,
            res['energy_efficiency'],
            label=label,
            color=colors.get(label.upper(), 'black'),
            linestyle='--'
        )
    plt.xlabel("Time Slot")
    plt.ylabel("Mb/Joule")
    plt.title("Energy Efficiency over Time")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/comparison_energy_efficiency.png")
    plt.show()

    # --- Threats Neutralized ---
    plt.figure(figsize=(8, 5))
    for label, res in results_dict.items():
        plt.plot(
            time_slots,
            res['threats_handled'],
            label=label,
            color=colors.get(label.upper(), 'black'),
            linestyle='--'
        )
    plt.xlabel("Time Slot")
    plt.ylabel("Threats")
    plt.title("Threats Neutralized over Time")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/comparison_threats_neutralized.png")
    plt.show()

    # --- Total Energy Consumption ---
    plt.figure(figsize=(8, 5))
    for label, res in results_dict.items():
        plt.plot(
            time_slots,
            res['total_energy'],
            label=label,
            color=colors.get(label.upper(), 'black'),
            linestyle='--'
        )
    plt.xlabel("Time Slot")
    plt.ylabel("Energy (J)")
    plt.title("Total Energy Consumption over Time")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/comparison_energy_consumed.png")
    plt.show()




# def plot_comparisons(results_dict):
    # time_slots = list(range(len(next(iter(results_dict.values()))['energy_efficiency'])))
    # os.makedirs("results", exist_ok=True)
   
    # # --- Energy Efficiency ---
    # plt.figure(figsize=(8, 5))
    # for label, res in results_dict.items():
    #     plt.plot(time_slots, res['energy_efficiency'], label=f'{label}')
    # plt.xlabel("Time Slot")
    # plt.ylabel("Mb/Joule")
    # plt.title("Energy Efficiency over Time")
    # plt.grid(True)
    # plt.legend()
    # plt.tight_layout()
    # plt.savefig("results/comparison_energy_efficiency.png")
    # plt.show()

    # # --- Threats Neutralized ---
    # plt.figure(figsize=(8, 5))
    # for label, res in results_dict.items():
    #     plt.plot(time_slots, res['threats_handled'], label=f'{label}')
    # plt.xlabel("Time Slot")
    # plt.ylabel("Threats")
    # plt.title("Threats Neutralized over Time")
    # plt.grid(True)
    # plt.legend()
    # plt.tight_layout()
    # plt.savefig("results/comparison_threats_neutralized.png")
    # plt.show()

    # # --- Total Energy Consumption ---
    # plt.figure(figsize=(8, 5))
    # for label, res in results_dict.items():
    #     plt.plot(time_slots, res['total_energy'], label=f'{label}')
    # plt.xlabel("Time Slot")
    # plt.ylabel("Energy (J)")
    # plt.title("Total Energy Consumption over Time")
    # plt.grid(True)
    # plt.legend()
    # plt.tight_layout()
    # plt.savefig("results/comparison_energy_consumed.png")
    # plt.show()


import numpy as np

def plot_grouped_bar_charts(results_dict):
    os.makedirs("results", exist_ok=True)

    modes = list(results_dict.keys())
    time_slots = list(range(len(next(iter(results_dict.values()))['energy_efficiency'])))
    num_slots = len(time_slots)
    num_modes = len(modes)
    
    bar_width = 0.25
    x = np.arange(num_slots)  # Time slot positions

    colors = {
        'PURE': 'green',
        'ECOP': 'skyblue',
        'MPC-ONLY': 'orange'
    }

    # Plot 1: Threats Neutralized per Time Slot
    plt.figure(figsize=(10, 5))
    for idx, mode in enumerate(modes):
        values = results_dict[mode]['threats_handled']
        plt.bar(x + idx * bar_width, values, width=bar_width, label=mode, color=colors[mode])
    plt.xlabel("Time Slot")
    plt.ylabel("Threats Neutralized")
    plt.title("Threats Neutralized per Time Slot")
    plt.xticks(x + bar_width, time_slots)
    plt.legend()
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig("results/grouped_threats.png")
    plt.show()

    # Plot 2: Energy Efficiency per Time Slot
    plt.figure(figsize=(10, 5))
    for idx, mode in enumerate(modes):
        values = results_dict[mode]['energy_efficiency']
        plt.bar(x + idx * bar_width, values, width=bar_width, label=mode, color=colors[mode])
    plt.xlabel("Time Slot")
    plt.ylabel("Energy Efficiency (Mb/J)")
    plt.title("Energy Efficiency per Time Slot")
    plt.xticks(x + bar_width, time_slots)
    plt.legend()
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig("results/grouped_efficiency.png")
    plt.show()

def run_threat_scaling_analysis(base_config, threat_counts):
    efficiency_vals = []
    threats_neutralized_vals = []

    for threat_count in threat_counts:
        print(f"[INFO] Running PURE model with {threat_count} threats...")
        config = base_config.copy()
        config['mode'] = 'PURE'
        config['threats']['count'] = threat_count

        system = DecentralizedUAVSystem(config)
        results = system.run_simulation()

        # Average energy efficiency across slots
        avg_efficiency = sum(results['energy_efficiency']) / len(results['energy_efficiency'])
        efficiency_vals.append(avg_efficiency)

        # Total threats neutralized
        total_threats = sum(results['threats_handled'])
        threats_neutralized_vals.append(total_threats)

    return efficiency_vals, threats_neutralized_vals

def plot_threat_scaling(threat_counts, efficiency_vals, neutralized_vals):
    import matplotlib.pyplot as plt
    os.makedirs("results", exist_ok=True)

    # Plot 1: Energy Efficiency vs Threat Count
    plt.figure(figsize=(8, 5))
    plt.plot(threat_counts, efficiency_vals, marker='o',linestyle='--', color='green')
    plt.title("Energy Efficiency vs Number of Threats (PURE Model)")
    plt.xlabel("Number of Threats")
    plt.ylabel("Avg Energy Efficiency (Mb/J)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("results/PURE_efficiency_vs_threats.png")
    plt.show()

    # Plot 2: Threats Neutralized vs Total Threats
    plt.figure(figsize=(8, 5))
    plt.plot(threat_counts, neutralized_vals, marker='s',linestyle='--', color='green')
    plt.title("Threats Neutralized vs Number of Threats (PURE Model)")
    plt.xlabel("Number of Threats")
    plt.ylabel("Total Neutralized")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("results/PURE_neutralized_vs_threats.png")
    plt.show()


def plot_bar_comparisons(results_dict):
    os.makedirs("results", exist_ok=True)

    # Extract means
    modes = list(results_dict.keys())
    avg_efficiency = [sum(res['energy_efficiency']) / len(res['energy_efficiency']) for res in results_dict.values()]
    avg_threats = [sum(res['threats_handled']) / len(res['threats_handled']) for res in results_dict.values()]

    # Plot Average Energy Efficiency
    plt.figure(figsize=(6, 4))
    plt.bar(modes, avg_efficiency, color=['green', 'skyblue', 'orange'])
    plt.title("Average Energy Efficiency")
    plt.ylabel("Mb per Joule")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig("results/avg_energy_efficiency.png")
    plt.show()

    # Plot Average Threats Neutralized
    plt.figure(figsize=(6, 4))
    plt.bar(modes, avg_threats, color=['green', 'skyblue', 'orange'])
    plt.title("Average Threats Neutralized")
    plt.ylabel("Number of Threats")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig("results/avg_threats_neutralized.png")
    plt.show()

def plot_boxplots(results_dict):
    os.makedirs("results", exist_ok=True)

    # Box Plot: Threats Neutralized
    plt.figure(figsize=(7, 5))
    data = [res['threats_handled'] for res in results_dict.values()]
    labels = list(results_dict.keys())
    plt.boxplot(data, labels=labels, patch_artist=True,
                boxprops=dict(facecolor='lightblue'))
    plt.title("Threats Neutralized per Time Slot")
    plt.ylabel("Number of Threats")
    plt.grid(True)
    plt.savefig("results/threats_boxplot.png")
    plt.show()

    # Box Plot: Energy Efficiency
    plt.figure(figsize=(7, 5))
    data = [res['energy_efficiency'] for res in results_dict.values()]
    plt.boxplot(data, labels=labels, patch_artist=True,
                boxprops=dict(facecolor='lightgreen'))
    plt.title("Energy Efficiency per Time Slot")
    plt.ylabel("Mb per Joule")
    plt.grid(True)
    plt.savefig("results/efficiency_boxplot.png")
    plt.show()


def run_mode(config, mode):
    config['mode'] = mode
    system = DecentralizedUAVSystem(config)
    results = system.run_simulation()
    return results


def run_threat_sweep(threat_counts, base_config):
    results_per_threat = {}

    for count in threat_counts:
        print(f"[INFO] Running simulation with {count} threats...")
        config = base_config.copy()
        config['mode'] = 'PURE'  # You can test other modes too
        config['threats']['count'] = count

        system = DecentralizedUAVSystem(config)
        results = system.run_simulation()
        results_per_threat[count] = results

    return results_per_threat


def plot_threat_sweep(results_dict):
    os.makedirs("results", exist_ok=True)
    time_slots = list(range(len(next(iter(results_dict.values()))['energy_efficiency'])))

    # Energy Efficiency Plot
    plt.figure(figsize=(10, 5))
    for count, res in results_dict.items():
        plt.plot(time_slots, res['energy_efficiency'], label=f'{count} Threats')
    plt.title("Energy Efficiency vs Time for Varying Threat Counts")
    plt.xlabel("Time Slot")
    plt.ylabel("Mb per Joule")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/threatsweep_efficiency.png")
    plt.show()

    # Threat Neutralization Plot
    plt.figure(figsize=(10, 5))
    for count, res in results_dict.items():
        plt.plot(time_slots, res['threats_handled'], label=f'{count} Threats')
    plt.title("Threats Neutralized vs Time")
    plt.xlabel("Time Slot")
    plt.ylabel("Number Neutralized")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/threatsweep_neutralized.png")
    plt.show()

def plot_threats_line(results_dict, time_slots, modes, colors):
    plt.figure(figsize=(10, 5))
    for mode in modes:
        values = results_dict[mode]['threats_handled']
        plt.plot(time_slots, values, label=mode, marker='o', linewidth=2,linestyle='--', color=colors[mode])

    plt.xlabel("Time Slot")
    plt.ylabel("Threats Neutralized")
    plt.title("Threats Neutralized Over Time")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/threats_lineplot.png")
    plt.show()

def plot_threats_summary_bar(results_dict, modes, colors):
    plt.figure(figsize=(8, 5))
    totals = [sum(results_dict[mode]['threats_handled']) for mode in modes]
    plt.bar(modes, totals, color=[colors[mode] for mode in modes])
    plt.ylabel("Total Threats Neutralized")
    plt.title("Total Threats Neutralized per Strategy")
    plt.tight_layout()
    plt.savefig("results/threats_total_bar.png")
    plt.show()

def plot_threats_boxplot(results_dict, modes, colors):
    plt.figure(figsize=(8, 5))
    data = [results_dict[mode]['threats_handled'] for mode in modes]
    box = plt.boxplot(data, labels=modes, patch_artist=True)
    
    for patch, mode in zip(box['boxes'], modes):
        patch.set_facecolor(colors[mode])
        
    plt.ylabel("Threats Neutralized")
    plt.title("Distribution of Threat Neutralization")
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("results/threats_boxplot.png")
    plt.show()

def aggregate_multiple_runs(base_config, mode, runs=10):
    from copy import deepcopy
    total_slots = None
    accumulated = {
        'energy_efficiency': None,
        'threats_handled': None,
        'total_energy': None
    }

    for run in range(runs):
        print(f"[RUN {run+1}] Mode: {mode}")
        config = deepcopy(base_config)
        config['mode'] = mode.lower()

        system = DecentralizedUAVSystem(config)
        result = system.run_simulation()

        for key in accumulated:
            if accumulated[key] is None:
                accumulated[key] = [0.0] * len(result[key])
            for i in range(len(result[key])):
                accumulated[key][i] += result[key][i]

    # Take average
    for key in accumulated:
        accumulated[key] = [val / runs for val in accumulated[key]]

    return accumulated


def main():
    config_path = 'config.json'
    if not os.path.exists(config_path):
        raise FileNotFoundError("Missing config.json")

    with open(config_path, 'r') as f:
        base_config = json.load(f)

    # print("[INFO] Running simulations for comparison...")
    # comparison_results = {}
    # for mode in ['PURE', 'ecop', 'mpc-only']:
    #     print(f"[INFO] Mode: {mode}")
    #     config = base_config.copy()
    #     config['mode'] = mode
    #     results = run_mode(config, mode)
    #     comparison_results[mode.upper()] = results

    print("[INFO] Running 10-run average simulations for comparison...")
    comparison_results = {}
    # for mode in ['PURE', 'ECOP', 'MPC-ONLY']:
    #     averaged_result = aggregate_multiple_runs(base_config, mode, runs=1)
    #     comparison_results[mode] = averaged_result

   

    # plot_comparisons(comparison_results)
    # plot_grouped_bar_charts(comparison_results)
        # --- Run threat scaling for PURE ---
    # threat_counts = list(range(10, 101, 10))  # 10, 20, ..., 100
    # eff_vals, neut_vals = run_threat_scaling_analysis(base_config, threat_counts)
    # plot_threat_scaling(threat_counts, eff_vals, neut_vals)

    # compute_percentage_gains(comparison_results)

    # system = DecentralizedUAVSystem(num_uavs=5, num_devices=100, num_threats=3)
    # system.run_simulation(steps=50)

    # Create 3D animation
    # visualize_3d(system.visual_frames, system.area_size)
        # --- Single visualization run ---
    print("[INFO] Running single visualization simulation...")
    config = base_config.copy()
    config['mode'] = 'PURE'   # or "ECOP" or "MPC-ONLY"
    config['threats']['count'] = 20
    system = DecentralizedUAVSystem(config)
    results = system.run_simulation()

    # Now visualize
    visualize_3d(system.visual_frames, system.area_size)

    # plot_grouped_bar_charts(comparison_results)
    
    # Define plotting helpers
    # time_slots = list(range(len(next(iter(comparison_results.values()))['threats_handled'])))
    # modes = list(comparison_results.keys())
    # colors = {
    #     'PURE': 'green',
    #     'ECOP': 'skyblue',
    #     'MPC-ONLY': 'orange'
    # }

    # # Plotting
    # plot_threats_line(comparison_results, time_slots, modes, colors)
    # plot_threats_summary_bar(comparison_results, modes, colors)
    # plot_threats_boxplot(comparison_results, modes, colors)

    #  # --- B. Threat count sweep experiment ---
    # print("[INFO] Running simulations for varying number of threats...")
    # threat_counts = [2, 5, 10, 20, 40]
    # threat_sweep_results = run_threat_sweep(threat_counts, base_config)
    # plot_threat_sweep(threat_sweep_results)

     # C. Visual animation run (only one)
    # print("[INFO] Running single visualization simulation...")
    # config = base_config.copy()
    # config['mode'] = 'PURE'
    # config['threats']['count'] = 20  # or any default
    # system = DecentralizedUAVSystem(config)
    # results = system.run_simulation()
    # system.visualize()

if __name__ == '__main__':
    main()
