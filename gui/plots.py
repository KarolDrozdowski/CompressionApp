import numpy as np


class PlotController:
    def __init__(self, figure, canvas, preview_tabs):
        self.figure = figure
        self.canvas = canvas
        self.preview_tabs = preview_tabs

    def plot_source_1d(self, original):
        self.figure.clear()

        ax = self.figure.add_subplot(111)
        ax.plot(original, color="#2563eb", linewidth=1.5)
        ax.set_title("Dane 1D")
        ax.set_xlabel("Probka")
        ax.set_ylabel("Wartosc")
        ax.grid(True, alpha=0.3)

        self._draw()

    def plot_loaded_image(self, image):
        self.figure.clear()

        ax = self.figure.add_subplot(111)
        ax.imshow(image, cmap="gray", vmin=0, vmax=255)
        ax.set_title("Obraz wejsciowy")
        ax.axis("off")

        self._draw()

    def plot_comparison_1d(self, original, reconstructed):
        self.figure.clear()

        ax = self.figure.add_subplot(111)
        ax.plot(original, label="Original", color="#2563eb", linewidth=1.5)
        ax.plot(reconstructed, label="Reconstructed", linestyle="dashed", color="#dc2626")
        ax.legend()
        ax.set_title("Compression comparison")
        ax.set_xlabel("Probka")
        ax.set_ylabel("Wartosc")
        ax.grid(True, alpha=0.3)

        self._draw()

    def plot_comparison_2d(self, original, reconstructed):
        self.figure.clear()

        original_ax = self.figure.add_subplot(131)
        reconstructed_ax = self.figure.add_subplot(132)
        error_ax = self.figure.add_subplot(133)

        error_map = np.abs(original.astype(float) - reconstructed.astype(float))

        original_ax.imshow(original, cmap="gray", vmin=0, vmax=255)
        original_ax.set_title("Original")
        original_ax.axis("off")

        reconstructed_ax.imshow(reconstructed, cmap="gray", vmin=0, vmax=255)
        reconstructed_ax.set_title("Reconstructed")
        reconstructed_ax.axis("off")

        error_ax.imshow(error_map, cmap="inferno")
        error_ax.set_title("Error")
        error_ax.axis("off")

        self._draw()

    def _draw(self):
        self.preview_tabs.setCurrentIndex(0)
        self.canvas.draw()
