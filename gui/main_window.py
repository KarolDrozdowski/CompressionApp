import matplotlib
matplotlib.use("QtAgg")

import matplotlib.pyplot as plt

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QTextEdit, QComboBox
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from compression.rle import rle_encode, rle_decode
from compression.dct import dct_compress, dct_decompress
from compression.huffman import huff_encode, huff_decode
from utils.loader import load_csv
from utils.generate_data import generate_1d_data
from utils.metrics import (
    mse,
    size_bytes,
    format_size,
    compression_ratio,
    compression_percent
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kompresja danych")

        self.layout = QVBoxLayout()

        self.load_btn = QPushButton("Wczytaj CSV")
        self.generate_btn = QPushButton("Wygeneruj dane")
        self.compress_btn = QPushButton("Kompresuj")

        self.method_box = QComboBox()
        self.method_box.addItems(["RLE", "DCT", "Huffman"])

        self.info = QTextEdit()
        self.info.setReadOnly(True)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.layout.addWidget(self.load_btn)
        self.layout.addWidget(self.generate_btn)
        self.layout.addWidget(self.method_box)
        self.layout.addWidget(self.compress_btn)
        self.layout.addWidget(QLabel("Wyniki:"))
        self.layout.addWidget(self.info)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

        self.data = None

        self.load_btn.clicked.connect(self.load_data)
        self.generate_btn.clicked.connect(self.on_generate_btn_clicked)
        self.compress_btn.clicked.connect(self.compress_data)

    def load_data(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Wybierz plik CSV")

        if file_name:
            self.data = load_csv(file_name).tolist()
            self.info.append(f"Załadowano dane: {len(self.data)} próbek")


    def on_generate_btn_clicked(self):
        self.data = generate_1d_data()
        self.info.append(f"Wygenerowano dane: {len(self.data)} próbek")

    def compress_data(self):
        if self.data is None:
            self.info.append("Najpierw wczytaj dane!")
            return

        method = self.method_box.currentText()

        orig_size = size_bytes(self.data)

        if method == "RLE":
            encoded = rle_encode(self.data)
            decoded = rle_decode(encoded)

            comp_size = size_bytes(encoded)

            error = mse(self.data, decoded)
            ratio = compression_ratio(orig_size, comp_size)
            percent = compression_percent(orig_size, comp_size)

            self.info.append("=== RLE ===")
            self.info.append(f"Rozmiar przed: {format_size(orig_size)}")
            self.info.append(f"Rozmiar po: {format_size(comp_size)}")
            self.info.append(f"Stopień kompresji: {percent:.2f}%")
            self.info.append(f"MSE: {error}")

            self.plot(self.data, decoded)

        elif method == "DCT":
            compressed = dct_compress(self.data, keep_ratio=0.5)
            decoded = dct_decompress(compressed)

            comp_size = size_bytes(compressed)

            error = mse(self.data, decoded)
            ratio = compression_ratio(orig_size, comp_size)
            percent = compression_percent(orig_size, comp_size)

            self.info.append("=== DCT ===")
            self.info.append(f"Rozmiar przed: {format_size(orig_size)}")
            self.info.append(f"Rozmiar po: {format_size(comp_size)}")
            self.info.append(f"Stopień kompresji: {percent:.2f}%")
            self.info.append(f"MSE: {error}")

            self.plot(self.data, decoded)

        elif method == "Huffman":
            encoded, tree = huff_encode(self.data)
            decoded = huff_decode(encoded, tree)

            comp_size = size_bytes(encoded)

            error = mse(self.data, decoded)
            ratio = compression_ratio(orig_size, comp_size)
            percent = compression_percent(orig_size, comp_size)

            self.info.append("=== Huffman ===")
            self.info.append(f"Rozmiar przed: {format_size(orig_size)}")
            self.info.append(f"Rozmiar po: {format_size(comp_size)}")
            self.info.append(f"Stopień kompresji: {percent:.2f}%")
            self.info.append(f"MSE: {error}")

            self.plot(self.data, decoded)

    def plot(self, original, reconstructed):
        self.figure.clear()

        ax = self.figure.add_subplot(111)

        ax.plot(original)
        ax.plot(reconstructed, linestyle='dashed')

        ax.legend(["Original", "Reconstructed"])
        ax.set_title("Compression comparison")
        ax.grid(True)

        self.canvas.draw()