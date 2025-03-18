# app.py

import streamlit as st
import folium
import requests
import pandas as pd
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import plotly.express as px

# OpenWeatherMap API Key
API_KEY = "ea815a44ac089b6f28d755bacec67f30"  # Replace with your OpenWeatherMap API key

# List of cities from around the world (You can expand this list)
cities = [
    {'city': 'San Francisco', 'lat': 37.7749, 'lon': -122.4194},
    {'city': 'Los Angeles', 'lat': 34.0522, 'lon': -118.2437},
    {'city': 'New York', 'lat': 40.7128, 'lon': -74.0060},
    {'city': 'London', 'lat': 51.5074, 'lon': -0.1278},
    {'city': 'Sydney', 'lat': -33.8688, 'lon': 151.2093},
    {'city': 'Paris', 'lat': 48.8566, 'lon': 2.3522},
    {'city': 'Tokyo', 'lat': 35.6895, 'lon': 139.6917},
    {'city': 'Beijing', 'lat': 39.9042, 'lon': 116.4074},
    {'city': 'Moscow', 'lat': 55.7558, 'lon': 37.6173},
    {'city': 'Cairo', 'lat': 30.0444, 'lon': 31.2357}
]

# Function to fetch weather data from OpenWeatherMap
def get_weather_data(city, lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        # Extracting the relevant weather information
        weather_data = {
            'city': city,
            'lat': lat,
            'lon': lon,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'weather': data['weather'][0]['description'],
        }
        return weather_data
    else:
        st.warning(f"Could not retrieve weather data for {city}")
        return None

# Fetch weather data for each city
weather_info = []
for city_data in cities:
    weather_data = get_weather_data(city_data['city'], city_data['lat'], city_data['lon'])
    if weather_data:
        weather_info.append(weather_data)

# Convert weather data to a DataFrame
weather_df = pd.DataFrame(weather_info)

# Streamlit Layout
st.title("Global Weather Map")
st.write("Weather conditions across the world")

# Display weather data in a table
st.write(weather_df)

# Create a Folium map centered globally
m = folium.Map(location=[20, 0], zoom_start=2)  # Global view, center the map around the equator

# Add weather markers to the map
for index, row in weather_df.iterrows():
    # Choose color based on temperature
    if row['temperature'] > 30:
        color = 'red'
    elif row['temperature'] > 20:
        color = 'orange'
    elif row['temperature'] > 10:
        color = 'yellow'
    else:
        color = 'blue'
    
    # Add a marker with temperature and weather info
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=f"City: {row['city']}<br>Temperature: {row['temperature']}°C<br>Weather: {row['weather']}<br>Humidity: {row['humidity']}%",
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6
    ).add_to(m)

# Render the map in Streamlit
folium_static(m)

# Plot weather conditions trend (Temperature vs City)
fig = px.bar(weather_df, x='city', y='temperature', title="Temperature by City", labels={'temperature': 'Temperature (°C)', 'city': 'City'})
st.plotly_chart(fig)
