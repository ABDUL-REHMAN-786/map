# app.py

import streamlit as st
import folium
import geopandas as gpd
from folium import plugins
import pandas as pd
import plotly.express as px
from folium.plugins import HeatMap
from streamlit_folium import folium_static

# Sample Data (replace this with real dataset)
data = {
    'lat': [37.7749, 34.0522, 40.7128, 51.5074],
    'lon': [-122.4194, -118.2437, -74.0060, -0.1278],
    'price': [500000, 800000, 700000, 1200000],
    'city': ['San Francisco', 'Los Angeles', 'New York', 'London']
}

df = pd.DataFrame(data)
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))

# Streamlit Layout
st.title("Interactive Geo-Spatial Analysis Tool")
st.write("Real Estate Data Points on a Map")

# Add price filter
min_price, max_price = st.slider(
    "Select Price Range:",
    min_value=int(df['price'].min()),
    max_value=int(df['price'].max()),
    value=(int(df['price'].min()), int(df['price'].max()))
)

# Filter data based on price
filtered_df = df[(df['price'] >= min_price) & (df['price'] <= max_price)]

# Create a folium map
m = folium.Map(location=[filtered_df['lat'].mean(), filtered_df['lon'].mean()], zoom_start=4)

# Add markers to the map
for index, row in filtered_df.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=f"City: {row['city']}<br>Price: ${row['price']}",
        icon=folium.Icon(color='green')
    ).add_to(m)

# Add a heatmap
heat_data = [[point[1], point[0]] for point in zip(filtered_df['lat'], filtered_df['lon'])]
HeatMap(heat_data).add_to(m)

# Render the map
folium_static(m)

# Plot housing price trends
fig = px.line(filtered_df, x='city', y='price', title="Housing Prices by City", labels={'price': 'Price ($)', 'city': 'City'})
st.plotly_chart(fig)
