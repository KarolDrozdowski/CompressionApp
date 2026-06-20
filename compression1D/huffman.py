import heapq
from collections import defaultdict, Counter

class Node:
    def __init__(self, symbol=None, freq=0):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_tree(data):
    freq = Counter(data)
    heap = [Node(sym, fr) for sym, fr in freq.items()]
    heapq.heapify(heap)

    if len(heap) == 1:
        node = heapq.heappop(heap)
        root = Node()
        root.left = node
        return root

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)

        merged = Node(freq=n1.freq + n2.freq)
        merged.left = n1
        merged.right = n2

        heapq.heappush(heap, merged)

    return heap[0]


def build_codes(node, prefix="", codes=None):
    if codes is None:
        codes = {}

    if node.symbol is not None:
        codes[node.symbol] = prefix or "0"
        return codes

    if node.left:
        build_codes(node.left, prefix + "0", codes)
    if node.right:
        build_codes(node.right, prefix + "1", codes)

    return codes


def huff_encode(data):
    tree = build_tree(data)
    codes = build_codes(tree)

    encoded = "".join(codes[x] for x in data)
    return encoded, tree


def huff_decode(encoded, tree):
    result = []
    node = tree

    for bit in encoded:
        node = node.left if bit == "0" else node.right

        if node.symbol is not None:
            result.append(node.symbol)
            node = tree

    return result