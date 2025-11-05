# mpc/predictor.py
from sklearn.mixture import GaussianMixture
import numpy as np

class GMMPredictor:
    def __init__(self, n_components=2):
        self.models = {}
        self.n_components = n_components

    def train(self, device_id, energy_history):
        if len(energy_history) >= self.n_components:
            data = np.array(energy_history).reshape(-1, 1)
            gmm = GaussianMixture(n_components=self.n_components, random_state=0)
            gmm.fit(data)
            self.models[device_id] = gmm

    def predict(self, device_id):
        if device_id in self.models:
            gmm = self.models[device_id]
            mean = np.dot(gmm.weights_, gmm.means_.flatten())
            return max(mean, 0.1)  # Ensure positive prediction
        return 1.0  # Default fallback
