# frontend/components/visualization_section.py

import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout

# --- Funktionen zum Einlesen der GraphML-Datei ---
def load_graph(graphml_path):
    """
    Lädt den Graphen aus einer GraphML-Datei mithilfe von NetworkX.
    """
    try:
        G = nx.read_graphml(graphml_path)
        print(f"Graph geladen: {G.number_of_nodes()} Knoten, {G.number_of_edges()} Kanten")
        return G
    except Exception as e:
        print("Fehler beim Laden der GraphML-Datei:", e)
        return None

# --- Funktion zur Layout-Berechnung für Detailmodus (z.B. spring_layout) ---
def compute_layout(G):
    """
    Berechnet ein Layout für den Graphen (z. B. spring_layout).
    Bei großen Netzwerken können Parameter wie 'k' und 'iterations' angepasst werden.
    """
    try:
        pos = nx.spring_layout(G, k=0.1, iterations=50)
        return pos
    except Exception as e:
        print("Fehler bei der Layout-Berechnung:", e)
        return None

# --- Funktion zur Layout-Berechnung für aggregierte Darstellung (Platzhalter) ---
def compute_aggregated_layout(G):
    """
    Berechnet ein aggregiertes Layout für große Netzwerke.
    Hier kann später ein Clustering-Algorithmus (z. B. Louvain) integriert werden,
    um Cluster zu bilden und diese als 'Super-Knoten' anzuzeigen.
    Aktuell nutzen wir als Platzhalter das normale Layout.
    """
    # Hier sollte ein echter Aggregationsprozess erfolgen.
    # Als Platzhalter verwenden wir einfach compute_layout.
    return compute_layout(G)

# --- QThread für asynchrone Layout-Berechnung ---
class LayoutWorker(QThread):
    layout_ready = pyqtSignal(dict)
    
    def __init__(self, G, mode="detail"):
        super().__init__()
        self.G = G
        self.mode = mode  # "detail" oder "aggregated"
        
    def run(self):
        if self.mode == "detail":
            pos = compute_layout(self.G)
        else:
            pos = compute_aggregated_layout(self.G)
        self.layout_ready.emit(pos)

# --- Matplotlib-Canvas zur Darstellung des Graphen ---
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, G, pos, parent=None):
        self.figure = Figure()
        super(MatplotlibCanvas, self).__init__(self.figure)
        self.setParent(parent)
        self.G = G
        self.pos = pos
        self._draw_graph()
    
    def _draw_graph(self):
        """
        Zeichnet den Graphen:
          - Knoten werden als Punkte dargestellt.
          - Kanten werden als Linien gezeichnet.
        """
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        # Zeichne den Graphen mithilfe von networkx und matplotlib
        nx.draw_networkx(
            self.G, pos=self.pos, ax=ax,
            node_color='blue', edge_color='gray',
            node_size=50, with_labels=False
        )
        ax.set_axis_off()
        self.draw()

# --- PyQt-Widget zur Einbettung des Matplotlib-Canvas ---
class VisualizationSection(QWidget):
    # Schwellenwert, ab dem der aggregierte Modus verwendet wird z.b NODE_THRESHOLD =500
    NODE_THRESHOLD = 500

    def __init__(self, parent=None):
        """
        Dieses Widget integriert die Visualisierung in die GUI.
        Es bleibt zunächst leer und wird erst aktualisiert, wenn ein dynamischer Pfad übergeben wird.
        """
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.G = None
        self.pos = None
        self.canvas = None
        self.mode = None  # "detail" oder "aggregated"

    def load_graph_from_path(self, graphml_path):
        """
        Verarbeitet den übergebenen Pfad:
          - Lädt den Graphen neu.
          - Bestimmt den Modus basierend auf der Knotenzahl.
          - Berechnet das Layout asynchron.
          - Aktualisiert den Canvas (entfernt den alten und fügt einen neuen hinzu).
        """
        new_G = load_graph(graphml_path)
        if new_G is None:
            print("Fehler: Neuer Graph konnte nicht geladen werden.")
            return

        # Bestimme den Modus basierend auf der Knotenzahl:
        if new_G.number_of_nodes() < self.NODE_THRESHOLD:
            self.mode = "detail"
            print("Detailmodus aktiviert.")
        else:
            self.mode = "aggregated"
            print("Aggregierter Modus aktiviert (Clustering/Sampling wird angewendet).")
        
        # Starte asynchron die Layout-Berechnung im entsprechenden Modus
        self.layout_worker = LayoutWorker(new_G, mode=self.mode)
        self.layout_worker.layout_ready.connect(self.on_layout_ready)
        self.layout_worker.start()

    def on_layout_ready(self, pos):
        """
        Callback, wenn das Layout asynchron berechnet wurde.
        Hier wird der Matplotlib-Canvas erstellt und in das Widget eingebettet.
        """
        self.pos = pos
        self.G = self.layout_worker.G  # Aktualisiere den Graphen
        # Entferne den alten Canvas, falls vorhanden
        if self.canvas is not None:
            self.layout().removeWidget(self.canvas)
            self.canvas.setParent(None)
        # Erstelle einen neuen Canvas und füge ihn dem Layout hinzu
        self.canvas = MatplotlibCanvas(self.G, self.pos, parent=self)
        self.layout().addWidget(self.canvas)
        print("Graph und Layout wurden aktualisiert im Modus:", self.mode)
