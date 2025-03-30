# upload_panel.py

import os
import shutil
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QHBoxLayout,
    QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import QThread, pyqtSignal

from backend import pipeline

def guess_data_source_by_extension(filename):
    """
    Bestimmt anhand der Dateiendung die Datenquelle:
      .graphml -> "TopologyZoo"
      .xml     -> "SNDlib"
      .cch     -> "Rocketfuel"
      .txt     -> "CAIDA_AS"
    Ansonsten -> "Unbekannt".
    """
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".graphml":
        return "TopologyZoo"
    elif ext == ".xml":
        return "SNDlib"
    elif ext == ".cch":
        return "Rocketfuel"
    elif ext == ".txt":
        return "CAIDA_AS"
    else:
        return "Unbekannt"


class AnalysisThread(QThread):
    finished = pyqtSignal()

    def __init__(self, file_paths):
        super().__init__()
        self.file_paths = file_paths

    def run(self):
        # Pipeline-Aufruf 
        pipeline.process_files(self.file_paths)
        self.finished.emit()


class UploadPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.uploaded_files = []  # Liste mit Pfaden zu den hochgeladenen Dateien

        # Hauptlayout
        layout = QVBoxLayout(self)

        # --- 1. Button-Bereich ---
        button_layout = QHBoxLayout()
        
        self.upload_button = QPushButton("📂 Dateien hochladen")
        self.upload_button.clicked.connect(self.upload_files)
        button_layout.addWidget(self.upload_button)

        self.analyze_button = QPushButton("🔍 Analyse starten")
        self.analyze_button.clicked.connect(self.start_analysis)
        button_layout.addWidget(self.analyze_button)

        layout.addLayout(button_layout)

        # --- 2. Status-Label ---
        self.status_label = QLabel("Status: Keine Datei hochgeladen.")
        layout.addWidget(self.status_label)

        # --- 3. Tabelle der hochgeladenen Dateien ---
        self.files_table = QTableWidget()
        self.files_table.setColumnCount(3)
        self.files_table.setHorizontalHeaderLabels(["Dateiname", "Quelle", "Status"])
        layout.addWidget(self.files_table)

    def upload_files(self):
        """
        Öffnet einen Dateidialog und kopiert ausgewählte Dateien in 'temp_uploads'.
        Aktualisiert die Tabelle mit neuen Einträgen (Dateiname, Quelle, Status).
        """
        files, _ = QFileDialog.getOpenFileNames(
            self, "Dateien auswählen", "",
            "Unterstützte Dateien (*.graphml *.xml *.cch *.txt);;Alle Dateien (*)"
        )
        if files:
            destination_folder = "temp_uploads"
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            for file_path in files:
                base_name = os.path.basename(file_path)
                destination_path = os.path.join(destination_folder, base_name)

                try:
                    shutil.copy(file_path, destination_path)
                    self.uploaded_files.append(destination_path)

                    # Hier bestimmen wir anhand der Endung die Quelle
                    guessed_source = guess_data_source_by_extension(base_name)

                    # Fügen den Eintrag in die Tabelle ein
                    self.add_file_to_table(base_name, guessed_source, "Bereit")

                except Exception as e:
                    self.status_label.setText(f"⚠ Fehler beim Kopieren von {base_name}: {str(e)}")
                    return

            self.status_label.setText(f"✅ {len(files)} Datei(en) erfolgreich gespeichert.")

    def add_file_to_table(self, filename, source, status):
        """
        Fügt einen neuen Eintrag in die Tabelle ein.
        """
        row_count = self.files_table.rowCount()
        self.files_table.insertRow(row_count)

        # Spalte 0: Dateiname
        item_name = QTableWidgetItem(filename)
        self.files_table.setItem(row_count, 0, item_name)

        # Spalte 1: Datenquelle (aus guess_data_source_by_extension)
        item_source = QTableWidgetItem(source)
        self.files_table.setItem(row_count, 1, item_source)

        # Spalte 2: Status
        item_status = QTableWidgetItem(status)
        self.files_table.setItem(row_count, 2, item_status)

    def start_analysis(self):
        """
        Startet die Analyse asynchron.
        Setzt den Status aller Dateien in der Tabelle auf 'Analyse läuft...' o.Ä.
        """
        if not self.uploaded_files:
            self.status_label.setText("⚠ Keine Datei hochgeladen!")
            return

        # Status in der Tabelle anpassen
        for row in range(self.files_table.rowCount()):
            self.files_table.setItem(row, 2, QTableWidgetItem("🔄 in Analyse..."))

        self.analysis_thread = AnalysisThread(self.uploaded_files)
        self.analysis_thread.finished.connect(self.analysis_finished)
        self.analysis_thread.start()
        self.status_label.setText("🔍 Analyse gestartet...")

    def analysis_finished(self):
        """
        Wird aufgerufen, wenn die Analyse abgeschlossen ist.
        Setzt den Status aller Dateien auf '✔️ analysiert'.
        """
        self.status_label.setText("✅ Analyse abgeschlossen!")
        for row in range(self.files_table.rowCount()):
            self.files_table.setItem(row, 2, QTableWidgetItem("analysiert"))
        # Greife auf das AnalysisSection des SingleGraphTab zu, das über das Parent-Widget erreichbar ist.
        if hasattr(self.parent, "single_graph_tab") and hasattr(self.parent.single_graph_tab, "analysis_section"):
            self.parent.single_graph_tab.analysis_section.load_analysis_results()
            # Leere die Liste der hochgeladenen Dateien
        self.uploaded_files.clear()
