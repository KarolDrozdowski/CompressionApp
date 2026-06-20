import random
import math

# Generates list size of list_size(by deafault 10000) from 1 to max_number(by default 1000)
def generate_1d_data(list_size: int=100, max_number: int=100):
    return [random.randint(1, max_number) for _ in range(list_size)]


def generate_sine_data(list_size: int=100, max_number: int=100):
    if list_size <= 0:
        return []

    amplitude = max_number / 2
    offset = max_number / 2

    return [
        offset + amplitude * math.sin(2 * math.pi * i / list_size)
        for i in range(list_size)
    ]
