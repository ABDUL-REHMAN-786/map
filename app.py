# app.py

import streamlit as st
import folium
import geopandas as gpd
import pandas as pd
import plotly.express as px
from folium.plugins import HeatMap
from streamlit_folium import folium_static

# Global dataset - Simulated example (Replace with a real dataset)
data = {
    'lat': [37.7749, 34.0522, 40.7128, 51.5074, -33.8688, 48.8566, 35.6895, 39.9042],
    'lon': [-122.4194, -118.2437, -74.0060, -0.1278, 151.2093, 2.3522, 139.6917, 116.4074],
    'price': [500000, 800000, 700000, 1200000, 900000, 1500000, 1100000, 950000],
    'city': ['San Francisco', 'Los Angeles', 'New York', 'London', 'Sydney', 'Paris', 'Tokyo', 'Beijing'],
    'country': ['USA', 'USA', 'USA', 'UK', 'Australia', 'France', 'Japan', 'China']
}

# Convert data into DataFrame
df = pd.DataFrame(data)

# Convert DataFrame to GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))

# Streamlit Layout
st.title("Global Interactive Geo-Spatial Analysis Tool")
st.write("Global Real Estate Data Points on a Map")

# Show the first few rows of the data
st.write(df.head())

# Add price filter
min_price, max_price = st.slider(
    "Select Price Range:",
    min_value=int(df['price'].min()),
    max_value=int(df['price'].max()),
    value=(int(df['price'].min()), int(df['price'].max()))
)

# Filter data based on price
filtered_df = df[(df['price'] >= min_price) & (df['price'] <= max_price)]

# Create a folium map centered globally
m = folium.Map(location=[20, 0], zoom_start=2)  # Global view, center the map around the equator

# Add markers to the map for filtered data
for index, row in filtered_df.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=f"City: {row['city']}<br>Country: {row['country']}<br>Price: ${row['price']}",
        icon=folium.Icon(color='green')
    ).add_to(m)

# Add a heatmap layer with filtered data
heat_data = [[point[1], point[0]] for point in zip(filtered_df['lat'], filtered_df['lon'])]
HeatMap(heat_data).add_to(m)

# Render the map in Streamlit
folium_static(m)

# Plot housing price trends (optional global chart)
fig = px.line(filtered_df, x='city', y='price', title="Housing Prices by City", labels={'price': 'Price ($)', 'city': 'City'})
st.plotly_chart(fig)
