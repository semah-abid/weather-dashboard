

import sqlite3


def init_database():
    # Verbindung zur Datenbank herstellen
    connection = sqlite3.connect("weather.db")
    cursor = connection.cursor()

    # Tabelle erstellen, falls sie noch nicht existiert
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature REAL,
            humidity INTEGER,
            timestamp TEXT
        )
    """)

    connection.commit()
    connection.close()


# Funktion zum Speichern von Wetterdaten
def save_weather(city, temperature, humidity):

    # Verbindung zur Datenbank herstellen
    connection = sqlite3.connect("weather.db")
    cursor = connection.cursor()

    # Wetterdaten mit Datum und Uhrzeit speichern
    cursor.execute("""
    INSERT INTO weather_data (city, temperature, humidity, timestamp)
    VALUES (?, ?, ?, datetime('now', 'localtime'))
    """, (city, temperature, humidity))

    # Änderungen speichern
    connection.commit()

    # Verbindung schließen
    connection.close()

    print("Weather data saved successfully!")





# Gespeicherte Wetterdaten anzeigen
if __name__ == "__main__":

    # Verbindung zur Datenbank herstellen
    connection = sqlite3.connect("weather.db")
    cursor = connection.cursor()

    # Nur den neuesten Datensatz abfragen
    cursor.execute("""
    SELECT * FROM weather_data
    ORDER BY id DESC
    LIMIT 1
    """)

    # Ergebnis abrufen
    rows = cursor.fetchall()

    # Datensatz im Terminal anzeigen
    for row in rows:
        print(row)

    # Verbindung schließen
    connection.close()
