import numpy as np
from PIL import Image

def load_csv(path):
    return np.loadtxt(path, delimiter=",")

def load_image(path):
    img = Image.open(path).convert("L")
    return np.array(img)