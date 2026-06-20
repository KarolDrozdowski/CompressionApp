from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QTextEdit, QComboBox, QDoubleSpinBox,
    QHBoxLayout, QGroupBox, QFormLayout, QTabWidget,
    QTableWidget, QSizePolicy, QSpinBox, QScrollArea
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def build_main_ui(window, data_label):
    root_layout = QHBoxLayout()
    root_layout.setContentsMargins(12, 12, 12, 12)
    root_layout.setSpacing(12)

    sidebar = QVBoxLayout()
    sidebar.setContentsMargins(0, 0, 0, 0)
    sidebar.setSpacing(8)

    settings_box = QGroupBox("Ustawienia")
    settings_layout = QVBoxLayout()
    settings_layout.setSpacing(8)

    window.mode_box = QComboBox()
    window.mode_box.addItems(["1D", "2D"])

    window.method_box = QComboBox()
    window.method_box.addItems(["RLE", "DCT", "Huffman"])

    form_layout = QFormLayout()
    form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
    form_layout.setVerticalSpacing(6)
    form_layout.setHorizontalSpacing(8)
    form_layout.addRow("Tryb danych", window.mode_box)
    form_layout.addRow("Metoda", window.method_box)

    window.keep_ratio_label = QLabel("DCT keep ratio")
    window.keep_ratio_box = QDoubleSpinBox()
    window.keep_ratio_box.setRange(0.05, 1.0)
    window.keep_ratio_box.setSingleStep(0.05)
    window.keep_ratio_box.setValue(0.5)
    window.keep_ratio_box.setDecimals(2)
    form_layout.addRow(window.keep_ratio_label, window.keep_ratio_box)

    settings_layout.addLayout(form_layout)

    source_box = QGroupBox("Zrodlo")
    source_layout = QVBoxLayout()
    source_layout.setSpacing(6)

    window.load_btn = QPushButton("Wczytaj CSV")
    window.load_image_btn = QPushButton("Wczytaj obraz")
    window.generate_btn = QPushButton("Wygeneruj dane 1D")

    window.generator_type_box = QComboBox()
    window.generator_type_box.addItems(["Losowe probki", "Sinus"])

    window.sample_count_box = QSpinBox()
    window.sample_count_box.setRange(2, 100000)
    window.sample_count_box.setValue(100)
    window.sample_count_box.setSingleStep(10)

    window.max_value_box = QSpinBox()
    window.max_value_box.setRange(1, 1000000)
    window.max_value_box.setValue(100)
    window.max_value_box.setSingleStep(10)

    window.generator_type_label = QLabel("Generator")
    window.sample_count_label = QLabel("Liczba probek")
    window.max_value_label = QLabel("Maks. wartosc")

    window.generator_form = QFormLayout()
    window.generator_form.setVerticalSpacing(6)
    window.generator_form.setHorizontalSpacing(8)
    window.generator_form.addRow(window.generator_type_label, window.generator_type_box)
    window.generator_form.addRow(window.sample_count_label, window.sample_count_box)
    window.generator_form.addRow(window.max_value_label, window.max_value_box)

    source_layout.addWidget(window.load_btn)
    source_layout.addWidget(window.load_image_btn)
    source_layout.addLayout(window.generator_form)
    source_layout.addWidget(window.generate_btn)
    source_box.setLayout(source_layout)

    window.compress_btn = QPushButton("Kompresuj")
    window.compress_btn.setObjectName("primaryButton")
    window.compress_btn.setMinimumHeight(34)

    settings_layout.addWidget(source_box)
    settings_layout.addWidget(window.compress_btn)
    settings_box.setLayout(settings_layout)

    data_box = QGroupBox("Aktualne dane")
    data_layout = QVBoxLayout()
    window.current_data_label = QLabel(data_label)
    window.current_data_label.setWordWrap(True)
    window.current_data_label.setObjectName("mutedLabel")
    data_layout.addWidget(window.current_data_label)
    data_box.setLayout(data_layout)

    results_box = QGroupBox("Wyniki")
    results_layout = QVBoxLayout()
    window.results_table = QTableWidget(5, 2)
    window.results_table.setHorizontalHeaderLabels(["Metryka", "Wartosc"])
    window.results_table.verticalHeader().setVisible(False)
    window.results_table.horizontalHeader().setStretchLastSection(True)
    window.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    window.results_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
    window.results_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    window.results_table.setMinimumHeight(154)
    window.results_table.setMaximumHeight(172)
    results_layout.addWidget(window.results_table)
    results_box.setLayout(results_layout)

    sidebar.addWidget(settings_box)
    sidebar.addWidget(data_box)
    sidebar.addWidget(results_box)
    sidebar.addStretch()

    sidebar_widget = QWidget()
    sidebar_widget.setLayout(sidebar)
    sidebar_widget.setMinimumWidth(300)

    window.sidebar_scroll = QScrollArea()
    window.sidebar_scroll.setWidgetResizable(True)
    window.sidebar_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    window.sidebar_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    window.sidebar_scroll.setWidget(sidebar_widget)
    window.sidebar_scroll.setMinimumWidth(320)
    window.sidebar_scroll.setMaximumWidth(360)

    window.figure = Figure(figsize=(7, 5), tight_layout=True)
    window.canvas = FigureCanvas(window.figure)
    window.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    window.preview_tab = QWidget()
    preview_layout = QVBoxLayout()
    preview_layout.setContentsMargins(8, 8, 8, 8)
    preview_layout.addWidget(window.canvas)
    window.preview_tab.setLayout(preview_layout)

    window.info = QTextEdit()
    window.info.setReadOnly(True)

    window.preview_tabs = QTabWidget()
    window.preview_tabs.addTab(window.preview_tab, "Podglad")
    window.preview_tabs.addTab(window.info, "Log")

    root_layout.addWidget(window.sidebar_scroll)
    root_layout.addWidget(window.preview_tabs, 1)

    window.setLayout(root_layout)
