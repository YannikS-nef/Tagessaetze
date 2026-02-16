# Tagessatz Dashboard

Einfache Flask-Webanwendung zur Verwaltung von Kunden, Tagessätzen und Umsätzen mit Ampel-Vergleich und Ziel-Rechner.

## Features
- Kunden anlegen (Name, Tagessatz, Umsatz, Haupt-/Nebenkunde)
- Übersichtstabelle mit Ampelstatus zur Tagessatz-Einordnung
- Berechnung optimaler Tages-/Stundensätze anhand Jahresziel und Verfügbarkeit
- Persistenz über SQLite (`data/customers.db`)

## Lokal starten
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Dann öffnen: `http://localhost:8080`

## Docker (z. B. Unraid)
```bash
docker compose up -d --build
```

Die Daten liegen im gemounteten Ordner `./data`.

## Hinweise
- Ampel basiert auf einem einfachen Vergleich der Tagessatz-Spanne (unteres/mittleres/oberes Drittel).
- Für echte Steuerberechnungen bitte steuerliche Beratung nutzen.
