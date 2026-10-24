
import sqlite3

# Verbindung zur bestehenden Datenbank herstellen
connection = sqlite3.connect("weather.db")
cursor = connection.cursor()

# Prüfen, welche Spalten bereits existieren
cursor.execute("PRAGMA table_info(weather_data)")
columns = [row[1] for row in cursor.fetchall()]

# Neue Spalte nur hinzufügen, wenn sie noch nicht existiert
if "timestamp" not in columns:
    cursor.execute("""
    ALTER TABLE weather_data
    ADD COLUMN timestamp TEXT
    """)

    print("Timestamp column added successfully!")
else:
    print("Timestamp column already exists!")

# Änderungen speichern
connection.commit()

# Verbindung schließen
connection.close()
