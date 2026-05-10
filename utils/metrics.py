import numpy as np
import sys

def mse(original, reconstructed):
    original = np.array(original)
    reconstructed = np.array(reconstructed)
    return np.mean((original - reconstructed) ** 2)


def size_bytes(obj):
    return sys.getsizeof(obj)


def format_size(bytes_val):
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024**2:
        return f"{bytes_val/1024:.2f} KB"
    else:
        return f"{bytes_val/(1024**2):.2f} MB"


def compression_ratio(original_size, compressed_size):
    if compressed_size == 0:
        return 0
    return original_size / compressed_size


def compression_percent(original_size, compressed_size):
    return (1 - compressed_size / original_size) * 100 if original_size else 0