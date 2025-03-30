# Netzwerk-Analyse-Tool

## Einführung zum Tool & Hinweis zur Testversion

### Zweck des Tools
Dieses Netzwerk-Analyse-Tool wurde entwickelt, um große Netzwerkdatensätze **einfach und interaktiv analysieren und visualisieren** zu können – auch ohne tiefes technisches Vorwissen.

Es kombiniert eine **benutzerfreundliche grafische Oberfläche (GUI)** mit bewährten Prinzipien der **Mensch-Computer-Interaktion (HCI)** und moderner **Netzwerkanalyse in Python**.

### Ziele:
- Einfache Analyse großer Netzwerkdaten (Graphen)
- Berechnung wichtiger Metriken (z. B. Knotenzahl, Dichte, Zentralität, Konnektivität)
- Visualisierung von Netzwerkstrukturen und Analyseergebnissen
- Export von Analyseergebnissen (z. B. als JSON)
- Filterung und gezielte Suche nach Netzwerkeigenschaften

### Der Fokus liegt auf:
- einer intuitiven grafischen Benutzeroberfläche (GUI)
- automatisierter Analyse von Netzwerkdateien in verschiedenen Formaten
- dynamischer Filterung & Visualisierung der Analyseergebnisse
- Beachtung von HCI-Prinzipien für optimale Bedienbarkeit

> ⚠️ **Hinweis:**  
> Das Tool ist **noch nicht vollständig implementiert**.  
> Funktionen in der Toolbar (wie JSON/PDF-Export) sind **derzeit Platzhalter**.  
> Die Entwicklung konzentrierte sich auf die **Kernfunktionen**.

---

## Bedienungsschritte – So nutzt du das Tool

### Schritt 1: Start & Übersicht
Nach dem Öffnen erscheint die Hauptansicht mit:

- **Linker Bereich:** Upload-Bereich für Netzwerkdateien
- **Rechter Bereich:** Zwei Analyse-Tabs
  - Einzelgraph-Analyse
  - Datensatz-Analyse
- **Oben:** Toolbar (Menüleiste)
---

### Schritt 2: Dateien hochladen
Klicke im linken Bereich auf **„Datei hochladen“**  
und wähle eine oder mehrere Netzwerkdateien aus (`.graphml`, `.xml`, `.txt`, `.cch`).

---

### Schritt 3: Analyse starten
Klicke auf **„Analyse starten“**.

- Die Analyse läuft **asynchron im Hintergrund**
- Die GUI bleibt dabei reaktionsfähig
- Der Status wird automatisch aktualisiert (z. B. „in Analyse…“, „analysiert“)
- Nach Abschluss kannst du mit den Analyseergebnissen weiterarbeiten

---

### Schritt 4: Einzelgraph-Analyse
Im Tab **„Einzelgraph-Analyse“** findest du:

- Eine **Filtersektion**
- Eine **Tabelle mit Analyseergebnissen**

#### Funktionen:
- **Schnellsuche** nach Dateinamen / Projekten
- **Erweiterte Filter:** z. B. Knotenzahl, Kantenanzahl, Dichte, Zentralität
- **Metrikauswahlmenü:** Wähle aus, welche Metriken angezeigt werden sollen

In der Tabelle:
- **Spalten und Zeilen lassen sich manuell in der Größe anpassen**
- Mit dem **QSplitter** kannst du die Größe zwischen Analyse & Visualisierung flexibel anpassen
- **Doppelklicke** auf einen Dateinamen, um die Visualisierung zu öffnen

---

### Schritt 5: Visualisierung

Nach dem Doppelklick erscheint die Visualisierung des Netzwerkgraphen im unteren Bereich.

#### Die Visualisierung:
- basiert auf **Matplotlib**
- ist **statisch** – keine Zoom- oder Drag-Funktionen
- zeigt **Knoten als blaue Punkte** und **Kanten als graue Linien**

> 📐 Mit dem **QSplitter** kannst du die Ansicht beliebig vergrößern oder verkleinern.

#### Hinweis zur Technologie:
Das Tool nutzt **Matplotlib**, um:
- maximale **Systemkompatibilität** zu erreichen
- Abhängigkeiten minimal zu halten

> 🔬 **VisPy** (für interaktive Graphen) wurde bewusst nicht eingebunden.  
> Wer dies ausprobieren möchte, kann eine eigene Umgebung (z. B. mit Conda) aufsetzen.  
> In anderen GitHub-Projekten findest du Anleitungen zur **manuellen Integration von VisPy**.

---

### Schritt 6: Datensatz-Analyse

Im Tab **„Datensatz-Analyse“**:

1. **Wähle** im Dropdown eine Datenquelle (z. B. „TopologyZoo“, „SNDlib“) oder **„Alle“**
2. **Klicke auf „Analyse laden“**

#### Du erhältst zwei Diagramme:
- **Diagramm 1**: Metriken mit Werten zwischen 0–1 (z. B. Dichte, Effizienz)
- **Diagramm 2**: Reelle Werte (z. B. Knotenzahl, Durchmesser)

> Über das Metrikauswahlmenü kannst du:
> - Metriken **ein-/ausblenden**
> - Die Auswahl auf **Standardwerte zurücksetzen**  
> Die Diagramme **aktualisieren sich automatisch**

---

## Feedback geben

Bitte gib uns Feedback zu folgenden Punkten:
👉 **Gib dein Feedback hier ab:** [Feedback-Seite öffnen](https://umfragen.tu-dortmund.de/index.php/614683?lang=de)

| Bereich         | Beispielhafte Fragen |
|----------------|----------------------|
| **Bedienbarkeit** | War die Oberfläche verständlich? Hast du dich gut zurechtgefunden? |
| **Visualisierung** | Reicht die Darstellung aus? Wünschst du interaktive Features? |
| **Filter & Suche** | Waren die Filteroptionen nützlich und nachvollziehbar? |
| **Performance** | Gab es Verzögerungen oder Hänger? |
| **Erweiterungswünsche** | Welche Funktionen würdest du dir in der finalen Version wünschen? |

---

## Download & Test

Das Tool steht als **Release auf GitHub** zur Verfügung:

🔗 **[→ Zum GitHub Release](https://github.com/useruser300/Netzwerkanalyse/releases)**

🔹 **Testdaten für das Tool findest du im Repository unter [`datasets-testen`](https://github.com/useruser300/Netzwerkanalyse/tree/main/datasets-testen)**

➡️ Diese Daten kannst du nutzen, um die Analyse- und Visualisierungsfunktionen auszuprobieren.

Dort findest du:
- vorkompilierte Versionen für **Windows, macOS und Linux**
- alternativ ein `.zip`-Archiv zum manuellen Start

---

## 🙏 Vielen Dank fürs Testen!

Dein Feedback hilft uns, das Tool weiter zu verbessern und eine finale Version mit vollständigem Funktionsumfang zu entwickeln.

---

