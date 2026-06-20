from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem

from utils.metrics import format_size


def clear_results(table):
    rows = [
        ("Algorytm", "-"),
        ("Rozmiar przed", "-"),
        ("Rozmiar po", "-"),
        ("Stopien kompresji", "-"),
        ("MSE", "-"),
    ]
    fill_results_table(table, rows)


def set_results(table, method, orig_size, comp_size, percent, error):
    rows = [
        ("Algorytm", method),
        ("Rozmiar przed", format_size(orig_size)),
        ("Rozmiar po", format_size(comp_size)),
        ("Stopien kompresji", f"{percent:.2f}%"),
        ("MSE", f"{error:.6g}"),
    ]
    fill_results_table(table, rows)


def append_log_results(info, method, orig_size, comp_size, percent, error):
    info.append(f"=== {method} ===")
    info.append(f"Rozmiar przed: {format_size(orig_size)}")
    info.append(f"Rozmiar po: {format_size(comp_size)}")
    info.append(f"Stopien kompresji: {percent:.2f}%")
    info.append(f"MSE: {error}")


def fill_results_table(table, rows):
    for row_index, (name, value) in enumerate(rows):
        name_item = QTableWidgetItem(name)
        value_item = QTableWidgetItem(value)
        name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        table.setItem(row_index, 0, name_item)
        table.setItem(row_index, 1, value_item)

    table.resizeColumnsToContents()
