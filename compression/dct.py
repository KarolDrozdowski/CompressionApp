import numpy as np

def dct_1d(signal):
    signal = np.array(signal, dtype=float)
    N = len(signal)
    coeffs = np.zeros(N)

    for k in range(N):
        alpha = np.sqrt(1 / N) if k == 0 else np.sqrt(2 / N)

        for n in range(N):
            coeffs[k] += signal[n] * np.cos(np.pi * k * (2*n + 1) / (2*N))

        coeffs[k] *= alpha

    return coeffs


def idct_1d(coeffs):
    coeffs = np.array(coeffs, dtype=float)
    N = len(coeffs)
    signal = np.zeros(N)

    for n in range(N):
        for k in range(N):
            alpha = np.sqrt(1 / N) if k == 0 else np.sqrt(2 / N)
            signal[n] += alpha * coeffs[k] * np.cos(np.pi * k * (2*n + 1) / (2*N))

    return signal


def dct_compress(signal, keep_ratio=0.5):
    coeffs = dct_1d(signal)

    N = len(coeffs)
    cutoff = int(N * keep_ratio)

    compressed = coeffs[:cutoff].astype(np.float32)

    return compressed, N


def dct_decompress(compressed, original_length):
    coeffs = np.zeros(original_length, dtype=np.float32)
    coeffs[:len(compressed)] = compressed

    return idct_1d(coeffs)