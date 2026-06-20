import heapq
from collections import Counter

import numpy as np


class Node:
    def __init__(self, symbol=None, freq=0):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def _as_uint8_image(image):
    return np.asarray(image, dtype=np.uint8)


def _build_tree(values):
    frequencies = Counter(values)
    heap = [Node(symbol, frequency) for symbol, frequency in frequencies.items()]
    heapq.heapify(heap)

    if not heap:
        return None

    if len(heap) == 1:
        node = heapq.heappop(heap)
        root = Node()
        root.left = node
        return root

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]


def _build_codes(node, prefix="", codes=None):
    if codes is None:
        codes = {}

    if node is None:
        return codes

    if node.symbol is not None:
        codes[node.symbol] = prefix or "0"
        return codes

    _build_codes(node.left, prefix + "0", codes)
    _build_codes(node.right, prefix + "1", codes)
    return codes


def huff_encode_image(image):
    image = _as_uint8_image(image)
    values = [int(value) for value in image.reshape(-1)]
    tree = _build_tree(values)
    codes = _build_codes(tree)
    encoded = "".join(codes[value] for value in values)

    return encoded, tree, image.shape


def huff_decode_image(encoded, tree, shape):
    if tree is None:
        return np.asarray([], dtype=np.uint8).reshape(shape)

    decoded = []
    node = tree

    for bit in encoded:
        node = node.left if bit == "0" else node.right

        if node.symbol is not None:
            decoded.append(node.symbol)
            node = tree

    return np.asarray(decoded, dtype=np.uint8).reshape(shape)
