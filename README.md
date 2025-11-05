# PURE: A Predictive Path-based UAV-IoT Network for Response-Oriented Energy-Efficient Border Monitoring

[![Conference](https://img.shields.io/badge/ICDCN-2026-blue)](https://icdcn.org/)
[![DOI](https://img.shields.io/badge/DOI-10.1145%2F3772290.3772300-blue)](https://doi.org/10.1145/3772290.3772300)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📄 Publication
**Abhishek Pandey**, Priyanka Soni, and Sourav Kanti Addya.  
“**PURE: A Predictive Path-based UAV-IoT Network for Response-Oriented Energy-Efficient Border Monitoring.**”  
*Proceedings of the 27th International Conference on Distributed Computing and Networking (ICDCN 2026)*,  
January 06–09, 2026, Nara, Japan.  
DOI: [10.1145/3772290.3772300](https://doi.org/10.1145/3772290.3772300)  
📘 **Status:** Accepted

---

## 🔍 Overview
**PURE** (Predictive Path-based UAV-IoT Network for Response-Oriented Energy-efficient Border Monitoring)  
is a **fully decentralized UAV-IoT surveillance framework** that integrates:
- **Model Predictive Control (MPC)** for adaptive UAV path planning  
- **Energy-aware computation offloading** for IoT-assisted intelligence  
- **Autonomous threat detection and neutralization** in real-time border zones  

PURE operates without any centralized control, making it resilient in **infrastructure-deficient** or **electronic warfare (EW)-contested** environments.  

---

## 🧠 Core Contributions
- **(i) Decentralized MPC-Enabled UAV-IoT Framework:**  
  A distributed coordination architecture combining energy-aware offloading with MPC-based UAV trajectory optimization.

- **(ii) Hybrid Predictive Offloading Mechanism:**  
  Integrates Gaussian Mixture Model (GMM)–based energy forecasting with local computation scheduling for energy-efficient decisions.

- **(iii) Demonstrated Performance Gains:**  
  Achieved **5.81% improvement in energy efficiency** and **37.5% higher threat neutralization rate** compared to ECOP and MPC-only baselines.

---

## ⚙️ System Architecture
The system models a UAV-IoT ecosystem deployed over a dynamic border region.  
IoT devices generate tasks and threats are simulated as intrusions moving toward the border.  
Each UAV predicts its path and allocates resources adaptively using local information.  

<p align="center">
  <img src="results/system_architecture.png" alt="System Architecture" width="750"/>
</p>

---

## 🧩 Features
- MPC-based UAV trajectory optimization  
- Decentralized, energy-aware task offloading  
- Threat modeling and real-time neutralization logic  
- Gaussian Mixture Model (GMM) for stochastic energy prediction  
- Comparative evaluation with ECOP-only and MPC-only baselines  
- Config-driven modular Python simulator with animated UAV paths  

---

## 🚀 Installation & Usage

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/abhishek-pndy/PURE-UAV-IoT.git
cd PURE-UAV-IoT
```

### 2️⃣ Install Requirements
```bash
pip install -r requirements.txt
```

### 3️⃣ Run Simulation
```bash
python main.py
```

### 4️⃣ View Results
Simulation outputs and plots are stored in the `results/` directory, including:
- `comparison_energy_efficiency.png`  
- `comparison_threats_neutralized.png`  
- `PURE_efficiency_vs_threats.png`  
- `PURE_neutralized_vs_threats.png`  
- Animated UAV surveillance visuals in `.mp4` and `.gif` formats  

---

## 📬 Contact
For questions or collaboration, reach out at:  
📧 **abhishekpandey.242cs004@nitk.edu.in**

---

**© 2026 Abhishek Pandey**  
Department of Computer Science, National Institute of Technology Karnataka, Surathkal
