import numpy as np


def _as_uint8_image(image):
    return np.asarray(image, dtype=np.uint8)


def rle_encode_image(image):
    image = _as_uint8_image(image)
    flat = image.reshape(-1)

    if flat.size == 0:
        return [], image.shape

    encoded = []
    previous = int(flat[0])
    count = 1

    for value in flat[1:]:
        value = int(value)
        if value == previous:
            count += 1
        else:
            encoded.append((previous, count))
            previous = value
            count = 1

    encoded.append((previous, count))
    return encoded, image.shape


def rle_decode_image(encoded, shape):
    decoded = []

    for value, count in encoded:
        decoded.extend([value] * count)

    return np.asarray(decoded, dtype=np.uint8).reshape(shape)
