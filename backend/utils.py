import torch
import psutil
import numpy as np

def detect_power_level():
    """Detect system power level based on GPU, RAM, and CPU availability."""
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    total_ram = psutil.virtual_memory().total / (1024 ** 3)
    cpu_cores = psutil.cpu_count(logical=False)

    if torch.cuda.is_available() and total_ram > 8:
        power_mode = "HIGH"
    elif cpu_cores > 4:
        power_mode = "MEDIUM"
    else:
        power_mode = "LOW"

    return power_mode, device

def euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return np.linalg.norm(np.array(p1) - np.array(p2))
