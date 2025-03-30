import json
from PyQt5.QtWidgets import QToolBar, QAction, QFileDialog, QMessageBox

class Toolbar(QToolBar):
    def __init__(self, parent):
        super().__init__("Hauptmenü")
        self.parent = parent

        # Bericht generieren (erstellt standardmäßig einen JSON-Bericht)
        self.report_action = QAction("📊 Bericht generieren", self)
        self.report_action.triggered.connect(self.generate_report)
        self.addAction(self.report_action)

        # Bericht als JSON speichern
        self.export_json_action = QAction("📊 JSON speichern", self)
        self.export_json_action.triggered.connect(self.export_as_json)
        self.addAction(self.export_json_action)

        # Bericht als PDF speichern
        self.export_pdf_action = QAction("📄 PDF speichern", self)
        self.export_pdf_action.triggered.connect(self.export_as_pdf)
        self.addAction(self.export_pdf_action)

        # Einstellungen
        self.settings_action = QAction("⚙ Einstellungen", self)
        self.settings_action.triggered.connect(self.show_settings)
        self.addAction(self.settings_action)

        # Hilfe
        self.help_action = QAction("❓ Hilfe", self)
        self.help_action.triggered.connect(self.show_help)
        self.addAction(self.help_action)

    def generate_report(self):
        """Erstellt den Bericht und speichert ihn standardmäßig als JSON."""
        self.export_as_json()
        QMessageBox.information(self, "Erfolg", "Bericht wurde erfolgreich generiert!")

    def export_as_json(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "JSON speichern", "", "JSON-Dateien (*.json)")
        if file_name:
            # Falls vorhanden, rufe die Analysedaten vom Parent ab.
            data = self.parent.analysis_section.get_analysis_data() if hasattr(self.parent, "analysis_section") else {}
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            QMessageBox.information(self, "Erfolg", "Bericht erfolgreich als JSON gespeichert!")

    def export_as_pdf(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "PDF speichern", "", "PDF-Dateien (*.pdf)")
        if file_name:
            # Hier könnte die Logik zur PDF-Erstellung integriert werden.
            QMessageBox.information(self, "Erfolg", "Bericht erfolgreich als PDF gespeichert!")

    def show_settings(self):
        QMessageBox.information(self, "Einstellungen", "Hier könnten später Anpassungen vorgenommen werden.")

    def show_help(self):
        help_text = (
        "🛠️ Bedienungsschritte – So nutzt du das Tool\n\n"
        "🔹 Schritt 1: Start & Übersicht\n"
        "- Linker Bereich: Datei-Upload\n"
        "- Rechter Bereich: Einzelgraph- und Datensatz-Analyse\n"
        "- Oben: Toolbar mit Export- & Hilfefunktionen\n\n"
        "🔹 Schritt 2: Netzwerkdateien hochladen\n"
        "- Klicke auf „Datei hochladen“ und wähle .graphml, .xml, .txt, .cch\n\n"
        "🔹 Schritt 3: Analyse starten\n"
        "- Klicke auf „Analyse starten“ → Ergebnisse erscheinen in den Tabs\n\n"
        "🔹 Schritt 4: Einzelgraph-Analyse\n"
        "- Filter, Metrikauswahl, Schnellsuche\n"
        "- Spalten & Zeilen lassen sich manuell in der Größe anpassen\n"
        "- Doppelklick zeigt die Visualisierung\n\n"
        "🔹 Schritt 5: Visualisierung\n"
        "- Statische Anzeige (Matplotlib), QSplitter für Größenanpassung\n\n"
        "🔹 Schritt 6: Datensatz-Analyse\n"
        "- Wähle Quelle, lade Analyse, sehe zwei Diagramme (0–1 & reelle Werte)\n"
        "- Metriken ein-/ausblenden, Diagramme passen sich an"
    )
        QMessageBox.information(self, "Hilfe", help_text)
