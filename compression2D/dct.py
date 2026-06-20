import numpy as np


BLOCK_SIZE = 8


def _as_uint8_image(image):
    return np.asarray(image, dtype=np.uint8)


def _dct_matrix(size=BLOCK_SIZE):
    matrix = np.zeros((size, size), dtype=np.float64)

    for k in range(size):
        alpha = np.sqrt(1 / size) if k == 0 else np.sqrt(2 / size)
        for n in range(size):
            matrix[k, n] = alpha * np.cos(np.pi * k * (2 * n + 1) / (2 * size))

    return matrix


def _pad_to_block_size(image, block_size=BLOCK_SIZE):
    height, width = image.shape
    padded_height = int(np.ceil(height / block_size) * block_size)
    padded_width = int(np.ceil(width / block_size) * block_size)

    padded = np.zeros((padded_height, padded_width), dtype=np.float64)
    padded[:height, :width] = image.astype(np.float64)

    return padded, image.shape


def dct_compress_image(image, keep_ratio=0.5, block_size=BLOCK_SIZE):
    image = _as_uint8_image(image)
    padded, original_shape = _pad_to_block_size(image, block_size)
    transform = _dct_matrix(block_size)

    compressed = np.zeros_like(padded, dtype=np.float32)
    keep_count = max(1, min(block_size, int(np.ceil(block_size * keep_ratio))))

    for row in range(0, padded.shape[0], block_size):
        for col in range(0, padded.shape[1], block_size):
            block = padded[row:row + block_size, col:col + block_size]
            coeffs = transform @ block @ transform.T
            kept = np.zeros_like(coeffs)
            kept[:keep_count, :keep_count] = coeffs[:keep_count, :keep_count]
            compressed[row:row + block_size, col:col + block_size] = kept

    metadata = {
        "original_shape": original_shape,
        "padded_shape": padded.shape,
        "block_size": block_size,
        "keep_count": keep_count,
    }

    return compressed, metadata


def dct_decompress_image(compressed, metadata):
    block_size = metadata["block_size"]
    original_shape = metadata["original_shape"]
    transform = _dct_matrix(block_size)

    reconstructed = np.zeros(metadata["padded_shape"], dtype=np.float64)

    for row in range(0, compressed.shape[0], block_size):
        for col in range(0, compressed.shape[1], block_size):
            coeffs = compressed[row:row + block_size, col:col + block_size]
            block = transform.T @ coeffs @ transform
            reconstructed[row:row + block_size, col:col + block_size] = block

    reconstructed = reconstructed[:original_shape[0], :original_shape[1]]
    return np.clip(np.rint(reconstructed), 0, 255).astype(np.uint8)
