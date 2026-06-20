import math

import matplotlib
matplotlib.use("QtAgg")

import numpy as np

from PyQt6.QtWidgets import QWidget, QFileDialog

from compression1D.rle import rle_encode, rle_decode
from compression1D.dct import dct_compress, dct_decompress
from compression1D.huffman import huff_encode, huff_decode
from compression2D.dct import dct_compress_image, dct_decompress_image
from compression2D.huffman import huff_decode_image, huff_encode_image
from compression2D.rle import rle_decode_image, rle_encode_image
from gui.plots import PlotController
from gui.results import append_log_results, clear_results, set_results
from gui.styles import APP_STYLESHEET
from gui.ui_builder import build_main_ui
from utils.loader import load_csv, load_image
from utils.generate_data import generate_1d_data, generate_sine_data
from utils.metrics import mse, size_bytes, compression_percent


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kompresja danych")
        self.resize(1180, 760)

        self.data = None
        self.data_mode = None
        self.data_label = "Brak danych"

        build_main_ui(self, self.data_label)
        self.plotter = PlotController(self.figure, self.canvas, self.preview_tabs)
        self.setStyleSheet(APP_STYLESHEET)

        self.connect_signals()
        self.update_controls()
        clear_results(self.results_table)

    def connect_signals(self):
        self.mode_box.currentTextChanged.connect(self.update_controls)
        self.method_box.currentTextChanged.connect(self.update_controls)
        self.load_btn.clicked.connect(self.load_data)
        self.load_image_btn.clicked.connect(self.load_image_data)
        self.generate_btn.clicked.connect(self.on_generate_btn_clicked)
        self.compress_btn.clicked.connect(self.compress_data)

    def update_controls(self):
        is_1d = self.mode_box.currentText() == "1D"
        is_dct = self.method_box.currentText() == "DCT"

        self.load_btn.setVisible(is_1d)
        self.generate_btn.setVisible(is_1d)
        self.load_image_btn.setVisible(not is_1d)
        self.generator_type_box.setVisible(is_1d)
        self.sample_count_box.setVisible(is_1d)
        self.max_value_box.setVisible(is_1d)
        self.generator_type_label.setVisible(is_1d)
        self.sample_count_label.setVisible(is_1d)
        self.max_value_label.setVisible(is_1d)

        self.keep_ratio_label.setVisible(is_dct)
        self.keep_ratio_box.setVisible(is_dct)

    def load_data(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz plik CSV",
            "",
            "CSV (*.csv);;All files (*)"
        )

        if file_name:
            self.data = load_csv(file_name).tolist()
            self.data_mode = "1D"
            self.data_label = f"CSV: {len(self.data)} probek"
            self.mode_box.setCurrentText("1D")
            self.current_data_label.setText(self.data_label)
            self.info.append(f"Zaladowano dane: {len(self.data)} probek")
            clear_results(self.results_table)

    def load_image_data(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz obraz",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )

        if file_name:
            self.data = load_image(file_name)
            self.data_mode = "2D"
            self.mode_box.setCurrentText("2D")
            height, width = self.data.shape
            self.data_label = f"Obraz: {width}x{height} px"
            self.current_data_label.setText(self.data_label)
            self.info.append(f"Zaladowano obraz: {width}x{height} px")
            clear_results(self.results_table)
            self.plotter.plot_loaded_image(self.data)

    def on_generate_btn_clicked(self):
        sample_count = self.sample_count_box.value()
        max_value = self.max_value_box.value()
        generator_type = self.generator_type_box.currentText()

        if generator_type == "Sinus":
            self.data = generate_sine_data(sample_count, max_value)
        else:
            self.data = generate_1d_data(sample_count, max_value)

        self.data_mode = "1D"
        self.data_label = (
            f"Dane wygenerowane: {generator_type}, "
            f"{len(self.data)} probek, max={max_value}"
        )
        self.mode_box.setCurrentText("1D")
        self.current_data_label.setText(self.data_label)
        self.info.append(
            f"Wygenerowano dane: {generator_type}, "
            f"{len(self.data)} probek, max={max_value}"
        )
        clear_results(self.results_table)
        self.plotter.plot_source_1d(self.data)

    def compress_data(self):
        if self.data is None:
            self.info.append("Najpierw wczytaj dane!")
            return

        selected_mode = self.mode_box.currentText()

        if selected_mode != self.data_mode:
            if selected_mode == "2D":
                self.info.append("Dla trybu 2D wczytaj obraz.")
            else:
                self.info.append("Dla trybu 1D wczytaj CSV lub wygeneruj dane.")
            return

        if selected_mode == "2D":
            self.compress_image_data()
            return

        self.compress_1d_data()

    def compress_1d_data(self):
        method = self.method_box.currentText()
        orig_size = size_bytes(self.data)

        if method == "RLE":
            encoded = rle_encode(self.data)
            decoded = rle_decode(encoded)
            comp_size = size_bytes(encoded)
        elif method == "DCT":
            encoded, original_length = dct_compress(
                self.data,
                keep_ratio=self.keep_ratio_box.value()
            )
            decoded = dct_decompress(encoded, original_length=original_length)
            comp_size = size_bytes(encoded)
        elif method == "Huffman":
            encoded, tree = huff_encode(self.data)
            decoded = huff_decode(encoded, tree)
            comp_size = size_bytes(encoded)
        else:
            return

        self.show_compression_results(method, orig_size, comp_size, self.data, decoded)
        self.plotter.plot_comparison_1d(self.data, decoded)

    def compress_image_data(self):
        method = self.method_box.currentText()
        image = np.asarray(self.data, dtype=np.uint8)
        orig_size = image.nbytes

        if method == "RLE":
            encoded, shape = rle_encode_image(image)
            decoded = rle_decode_image(encoded, shape)
            comp_size = len(encoded) * 5 + 8
        elif method == "DCT":
            encoded, metadata = dct_compress_image(
                image,
                keep_ratio=self.keep_ratio_box.value()
            )
            decoded = dct_decompress_image(encoded, metadata)

            block_size = metadata["block_size"]
            keep_count = metadata["keep_count"]
            blocks_y = metadata["padded_shape"][0] // block_size
            blocks_x = metadata["padded_shape"][1] // block_size
            comp_size = blocks_y * blocks_x * keep_count * keep_count * 4 + 16
        elif method == "Huffman":
            encoded, tree, shape = huff_encode_image(image)
            decoded = huff_decode_image(encoded, tree, shape)
            comp_size = math.ceil(len(encoded) / 8)
        else:
            return

        self.show_compression_results(f"{method} 2D", orig_size, comp_size, image, decoded)
        self.plotter.plot_comparison_2d(image, decoded)

    def show_compression_results(self, method, orig_size, comp_size, original, decoded):
        error = mse(original, decoded)
        percent = compression_percent(orig_size, comp_size)

        append_log_results(self.info, method, orig_size, comp_size, percent, error)
        set_results(self.results_table, method, orig_size, comp_size, percent, error)
