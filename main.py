
import requests
from database import save_weather

url = "https://api.open-meteo.com/v1/forecast"

# Städte und ihre geografischen Koordinaten
cities = {
    "Aachen": (50.7753, 6.0839),
    "Cologne": (50.9375, 6.9603),
    "Berlin": (52.5200, 13.4050),
    "Munich": (48.1351, 11.5820)
}

# Benutzer kann eine Stadt auswählen
city = st.selectbox("Choose a city", list(cities.keys()))

# Koordinaten der ausgewählten Stadt holen
latitude, longitude = cities[city]

parameters = {
    "latitude": latitude,
    "longitude": longitude,
    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
}

response = requests.get(url, params=parameters, timeout=10)

data = response.json()

temperature = data["current"]["temperature_2m"]
relative_humidity= data["current"]["relative_humidity_2m"]
wind_speed= data["current"]["wind_speed_10m"]

print("Weather in Aachen")
print(f"Temperature: {temperature} °C")
print(f"Humidity: {relative_humidity} %")
print(f"Wind Speed: {wind_speed} km/h")

save_weather("Aachen", temperature, relative_humidity)