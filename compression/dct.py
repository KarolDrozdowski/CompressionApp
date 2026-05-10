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

    # zeroing (kompresja stratna)
    cutoff = int(len(coeffs) * keep_ratio)
    compressed = np.zeros_like(coeffs)
    compressed[:cutoff] = coeffs[:cutoff]

    return compressed


def dct_decompress(coeffs):
    return idct_1d(coeffs)