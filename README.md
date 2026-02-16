# Tagessatz Dashboard

Einfache Flask-Webanwendung zur Verwaltung von Kunden, Tagessätzen und Umsätzen mit Ampel-Vergleich und Ziel-Rechner.

## Features
- Kunden anlegen (Name, Tagessatz, Umsatz, Haupt-/Nebenkunde)
- Übersichtstabelle mit Ampelstatus zur Tagessatz-Einordnung
- Berechnung optimaler Tages-/Stundensätze anhand Jahresziel und Verfügbarkeit
- Persistenz über SQLite (`data/customers.db` im Container)

## Lokal starten
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Dann öffnen: `http://localhost:8081`

## Docker per Compose (generisch)
```bash
docker compose up -d --build
```

## Unraid-Installation (Docker)

### Variante A: Über `docker-compose.yml` auf Unraid
1. Lege das Projekt z. B. unter `/mnt/user/appdata/tagessaetze/project` ab.
2. Passe in `docker-compose.yml` das Volume auf den gewünschten Host-Pfad an:
   ```yaml
   volumes:
     - /mnt/user/appdata/tagessaetze:/app/data
   ```
3. Starte den Container auf dem Unraid-Host:
   ```bash
   cd /mnt/user/appdata/tagessaetze/project
   docker compose up -d --build
   ```
4. Öffne im Browser: `http://<UNRAID-IP>:8081`

### Variante B: Manuell über Unraid WebUI (Add Container)
Wenn du lieber direkt in Unraid klickst:
1. **Docker** → **Add Container**
2. Name: `tagessaetze-app`
3. Image: entweder selbst gebautes Image oder vorher via CLI bauen (`docker build -t tagessaetze:latest .`)
4. Port-Mapping:
   - **Container Port**: `8081`
   - **Host Port**: `8081` (wie gewünscht statt 8080)
5. Path-Mapping:
   - **Host Path**: `/mnt/user/appdata/tagessaetze`
   - **Container Path**: `/app/data`
6. Restart Policy: `unless-stopped`
7. Container starten.

Damit liegen alle persistenten Daten wie gewünscht unter:

`/mnt/user/appdata/tagessaetze/`

## Hinweise
- Ampel basiert auf einem einfachen Vergleich der Tagessatz-Spanne (unteres/mittleres/oberes Drittel).
- Für echte Steuerberechnungen bitte steuerliche Beratung nutzen.
