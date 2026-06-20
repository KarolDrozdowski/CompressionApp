APP_STYLESHEET = """
    QWidget {
        background: #f5f7fb;
        color: #20242a;
        font-size: 13px;
    }
    QScrollArea {
        background: transparent;
        border: 0;
    }
    QScrollArea > QWidget > QWidget {
        background: transparent;
    }
    QGroupBox {
        background: #ffffff;
        border: 1px solid #d9dee8;
        border-radius: 8px;
        margin-top: 10px;
        padding: 10px;
        font-weight: 600;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 4px;
    }
    QPushButton, QComboBox, QDoubleSpinBox, QSpinBox {
        min-height: 26px;
        border: 1px solid #c8d0dc;
        border-radius: 6px;
        padding: 3px 8px;
        background: #ffffff;
    }
    QPushButton:hover {
        background: #eef3fb;
    }
    QPushButton#primaryButton {
        background: #2563eb;
        color: #ffffff;
        border-color: #2563eb;
        font-weight: 700;
    }
    QPushButton#primaryButton:hover {
        background: #1d4ed8;
    }
    QTextEdit, QTableWidget, QTabWidget::pane {
        background: #ffffff;
        border: 1px solid #d9dee8;
        border-radius: 8px;
    }
    QHeaderView::section {
        background: #edf1f7;
        border: 0;
        padding: 6px;
        font-weight: 600;
    }
    QLabel#mutedLabel {
        color: #5f6978;
        font-weight: 400;
    }
"""
