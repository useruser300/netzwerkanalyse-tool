# gui_main.py

import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QTabWidget, QStatusBar
)
from PyQt5.QtCore import Qt

from frontend.components.toolbar import Toolbar
from frontend.components.upload_panel import UploadPanel
from frontend.components.single_graph_tab import SingleGraphTab
from frontend.components.dataset_analysis_tab import DatasetAnalysisTab
#from frontend.components.report_section import ReportSection
######


class NetworkAnalysisGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Netzwerkanalyse-Tool (neue HCI-GUI)")
        self.setGeometry(100, 100, 1200, 800)

        # 1) Zentrales Widget + Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # -------------------------------------------
        # A) Universeller Bereich (links)
        # -------------------------------------------
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)
        self.left_widget.setLayout(self.left_layout)

        # Beispiel: UploadPanel im linken Bereich
        self.upload_panel = UploadPanel(self)
        self.left_layout.addWidget(self.upload_panel)

        # Füge den linken Bereich ins Hauptlayout ein
        main_layout.addWidget(self.left_widget)

        # -------------------------------------------
        # B) Tabs (rechts)
        # -------------------------------------------
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs, stretch=1)

        # Tab 1: Einzelgraph-Analyse
        self.single_graph_tab = SingleGraphTab(self)
        self.tabs.addTab(self.single_graph_tab, "Einzelgraph-Analyse")

        # Tab 2: Datensatz-Analyse
        self.dataset_tab = DatasetAnalysisTab(self)
        self.tabs.addTab(self.dataset_tab, "Datensatz-Analyse")

        # 2) Toolbar klassisch oben im Hauptfenster
        self._init_toolbar()

        # 3) Statusbar (unten)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Abschließend zeigen wir das Fenster an
        self.show()

    def _init_toolbar(self):
        """
        Erzeugt/Bindet deine vorhandene Toolbar-Klasse oben an das QMainWindow an.
        """
        self.toolbar = Toolbar(self)   # vorhandene Toolbar-Klasse
        self.addToolBar(self.toolbar)  # Dockt die Toolbar oben an


def main():
    app = QApplication(sys.argv)
    gui = NetworkAnalysisGUI()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
