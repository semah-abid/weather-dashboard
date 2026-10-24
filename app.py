
import streamlit as st

import sqlite3

import requests

import pandas as pd

from database import save_weather, init_database

# Datenbank beim Start der App vorbereiten
init_database()
 

# Städte und ihre Koordinaten
cities = {
    "Aachen": (50.7753, 6.0839),
    "Cologne": (50.9375, 6.9603),
    "Berlin": (52.5200, 13.4050),
    "Munich": (48.1351, 11.5820)
}

# Stadt auswählen
city = st.selectbox("Choose a city", list(cities.keys()))

# Koordinaten der ausgewählten Stadt holen
latitude, longitude = cities[city]

# Wetterdaten von der Open-Meteo API abrufen
url = "https://api.open-meteo.com/v1/forecast"

parameters = {
    "latitude": latitude,
    "longitude": longitude,
    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
    "daily": "temperature_2m_max,temperature_2m_min",
    "timezone": "auto"
}  



# Wetterdaten sicher von der API abrufen
try:
    response = requests.get(
        url,
        params=parameters,
        timeout=10
    )

    # Check whether the API request succeeded
    response.raise_for_status()

    data = response.json()

except requests.exceptions.RequestException:
    st.error("⚠️ Could not load weather data. Please check your internet connection or try again later.")
    st.stop()

#response = requests.get(url, params=parameters, timeout=10) 
#response.raise_for_status()

# JSON-Antwort in ein Python-Dictionary umwandeln
#data = response.json() #convert API into python data

# Wettervorhersage für morgen auslesen
tomorrow_max = data["daily"]["temperature_2m_max"][1]
tomorrow_min = data["daily"]["temperature_2m_min"][1]

# Forecast data for the next 7 days
forecast_dates = data["daily"]["time"][:7]
forecast_max = data["daily"]["temperature_2m_max"][:7]
forecast_min = data["daily"]["temperature_2m_min"][:7]


# Organize forecast data into a table
forecast_df = pd.DataFrame({
    "Date": forecast_dates,
    "Max Temperature": forecast_max,
    "Min Temperature": forecast_min
})

forecast_df["Date"] = pd.to_datetime(forecast_df["Date"])
forecast_df = forecast_df.set_index("Date")


# Aktuelle Wetterwerte auslesen
temperature = data["current"]["temperature_2m"]
humidity = data["current"]["relative_humidity_2m"]
wind_speed = data["current"]["wind_speed_10m"]
weather_code = data["current"]["weather_code"]


# Passendes Icon für das aktuelle Wetter auswählen
if weather_code == 0:
    weather_icon = "☀️"
    weather_description = "Clear sky"

elif weather_code in [1, 2]:
    weather_icon = "🌤️"
    weather_description = "Partly cloudy"

elif weather_code == 3:
    weather_icon = "☁️"
    weather_description = "Cloudy"

elif weather_code in [45, 48]:
    weather_icon = "🌫️"
    weather_description = "Foggy"

elif weather_code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:
    weather_icon = "🌧️"
    weather_description = "Rainy"

elif weather_code in [71, 73, 75, 77, 85, 86]:
    weather_icon = "❄️"
    weather_description = "Snowy"

elif weather_code in [95, 96, 99]:
    weather_icon = "⛈️"
    weather_description = "Thunderstorm"

else:
    weather_icon = "🌍"
    weather_description = "Unknown weather"
 


# Titel der Webseite anzeigen
st.title(f"{weather_icon} Weather Dashboard")
st.write(f"Current conditions: {weather_description}")
st.caption(f"Live weather conditions in {city}")


# Drei Spalten für die Wetterdaten erstellen
col1, col2, col3 = st.columns(3)

# Temperatur in der ersten Spalte anzeigen
with col1:
    st.metric("Temperature", f"{temperature} °C")

# Luftfeuchtigkeit in der zweiten Spalte anzeigen
with col2:
    st.metric("Humidity", f"{humidity} %")

# Windgeschwindigkeit in der dritten Spalte anzeigen
with col3:
    st.metric("Wind Speed", f"{wind_speed} km/h")



# Wettervorhersage für morgen anzeigen
st.subheader("🌤️ Tomorrow's Forecast")

col1, col2 = st.columns(2)

with col1:
    st.metric("🌡️ Max Temperature", f"{tomorrow_max} °C")

with col2:
    st.metric("❄️ Min Temperature", f"{tomorrow_min} °C")

# Display the 7-day forecast
st.subheader("📈 7-Day Temperature Forecast")

st.line_chart(forecast_df)


# Button zum Speichern der aktuellen Wetterdaten
if st.button("💾 Save Weather Data", type="primary"):

    # Wetterdaten der ausgewählten Stadt speichern
    save_weather(city, temperature, humidity)

    # Erfolgsmeldung anzeigen
    st.success("Weather data saved successfully!")





# Verbindung zur SQLite-Datenbank herstellen
connection = sqlite3.connect("weather.db")

# Anzahl der gespeicherten Wetterdatensätze abfragen
cursor = connection.cursor()

# Nur die Datensätze der ausgewählten Stadt zählen
cursor.execute(
    "SELECT COUNT(*) FROM weather_data WHERE city = ?",
    (city,)
)

count = cursor.fetchone()[0]

# Anzahl auf der Webseite anzeigen
st.write(f"Saved weather records for {city}: {count}")

# Nur Wetterdaten der ausgewählten Stadt abrufen
query = """
SELECT timestamp, temperature
FROM weather_data
WHERE timestamp IS NOT NULL
AND city = ?
ORDER BY timestamp
"""


# SQL-Ergebnisse in eine Pandas-Tabelle laden
df = pd.read_sql_query(query, connection, params=(city,))

# Datenbankverbindung schließen
connection.close()


# Überschrift für das Diagramm
st.subheader("Temperature History")

# Prüfen, ob Datensätze mit Zeitstempel vorhanden sind
if not df.empty:

    # Zeitstempel in Datumswerte umwandeln
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Zeitstempel als X-Achse verwenden
    df = df.set_index("timestamp")

    # Temperaturdiagramm anzeigen
    st.line_chart(df["temperature"])

else:
    st.info("No weather history with timestamps yet.")
