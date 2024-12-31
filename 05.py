import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point

# Load datasets
train_data = pd.read_csv(r"5th_task\traffic_accidents_training.csv")
test_data = pd.read_csv(r"5th_task\traffic_accidents_testing.csv")

# Explore the data
print("Preview of training data:")
print(train_data.head())

# Visualize distribution of accident severity
plt.figure(figsize=(8, 6))
sns.countplot(data=train_data, x="Accident_Severity", palette="viridis")
plt.title("Accident Severity Distribution")
plt.xlabel("Accident Severity")
plt.ylabel("Count")
plt.show()

# Analyze accidents by weather and road conditions
pivot_table = pd.crosstab(train_data['Weather'], train_data['Road_Condition'])
print("\nAccident Distribution by Weather and Road Conditions:")
print(pivot_table)

# Prepare data for mapping
train_data['Coordinates'] = list(zip(train_data['Longitude'], train_data['Latitude']))
train_data['Coordinates'] = train_data['Coordinates'].apply(Point)

# Convert to GeoDataFrame
geo_df = gpd.GeoDataFrame(train_data, geometry='Coordinates')

# Debugging: Check coordinates
print("Latitude range:", train_data['Latitude'].min(), "to", train_data['Latitude'].max())
print("Longitude range:", train_data['Longitude'].min(), "to", train_data['Longitude'].max())

# Load world shapefile
# Replace with your actual path to 'ne_10m_admin_0_countries.shp'
world = gpd.read_file(r"5th_task\ne_10m_admin_0_countries.shp")
print("World shapefile preview:")
print(world.head())
print("World CRS:", world.crs)

# Debugging: Check CRS of the accident data
print("Accident Data CRS:", geo_df.crs)

# Ensure CRS matches
if geo_df.crs is None:
    print("Setting CRS of accident data to EPSG:4326...")
    geo_df.set_crs(epsg=4326, inplace=True)  # WGS84 projection

# Ensure both GeoDataFrames (accident data and world shapefile) have the same CRS
if geo_df.crs != world.crs:
    print(f"Transforming accident data CRS from {geo_df.crs} to {world.crs}...")
    geo_df = geo_df.to_crs(world.crs)

# Plot the world map with accident hotspots
plt.figure(figsize=(12, 8))
base = world.plot(color='white', edgecolor='black')
geo_df.plot(ax=base, marker='o', color='red', markersize=15, alpha=0.6)  # Increased marker size and transparency
plt.title("Traffic Accident Hotspots", fontsize=16)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()

# Optional: Filter by region (e.g., USA)
usa = world[world['ADMIN'] == 'United States of America']
plt.figure(figsize=(12, 8))
base = usa.plot(color='white', edgecolor='black')
geo_df.plot(ax=base, marker='o', color='red', markersize=15, alpha=0.6)
plt.title("Traffic Accident Hotspots in the USA", fontsize=16)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
