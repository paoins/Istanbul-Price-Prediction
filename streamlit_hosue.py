import streamlit as st
import pandas as pd
import joblib
import folium
import branca.colormap as cm

# Load Model
model = joblib.load('real_estate_price_model.pkl')

# App Title
st.title("Real Estate Price Estimator")
st.write("Provide the details of the house and click Predict.")

# Input
st.sidebar.header("Property Details")

# Numeric inputs
size = st.sidebar.slider("Size (m²)", 30, 500, 100)
floor = st.sidebar.slider("Floor", -3, 50, 0)
toilet_count = st.sidebar.slider("Toilet Count", 1, 5, 1)
bedrooms = st.sidebar.slider("Bedrooms", 0, 10, 2)
living_rooms = st.sidebar.slider("Living Rooms", 0, 3, 1)
building_age = st.sidebar.slider("Building Age", 0, 100, 10)

# Categorical inputs
heating_type = st.sidebar.selectbox("Heating Type", ['Kombi', 'Kömür-Odun', 'missing', 'other'])
building_type = st.sidebar.selectbox("Building Type", ['Daire', 'Bina', 'Villa'])
neighborhood = st.sidebar.selectbox("Neighborhood", sorted(['Beylikdüzü', 'Esenyurt', 'Üsküdar', 'Adalar', 'Kadıköy',
       'Bağcılar', 'Zeytinburnu', 'Büyükçekmece', 'Küçükçekmece', 'Şişli',
       'Pendik', 'Şile', 'Beşiktaş', 'Bakırköy', 'Maltepe', 'Avcılar',
       'Bahçelievler', 'Arnavutköy', 'Ataşehir', 'Sarıyer', 'Eyüpsultan',
       'Kağıthane', 'Beykoz', 'Gaziosmanpaşa', 'Fatih', 'Başakşehir',
       'Ümraniye', 'Sancaktepe', 'Sultanbeyli']))

# Prepare input
input_data = pd.DataFrame([{
    'bedrooms': bedrooms,
    'living_rooms': living_rooms,
    'toilet_count': toilet_count,
    'floor': floor,
    'size': size,
    'building_age': building_age,
    'heating_type': heating_type,
    'building_type': building_type,
    'neighborhood': neighborhood
}])

# Predict
if st.button("Predict Price"):
    prediction = model.predict(input_data)[0]
    st.success(f"Estimated Price: **{int(prediction):,} TL**")


# Compute price per m²
df1 = pd.read_csv('scraped_data3_clean.csv')
# 1. Compute price per m²
df1['price_per_m2'] = df1['price'] / df1['size']

# Group by neighborhood
grouped = df1.groupby('neighborhood').agg({
    'price_per_m2': 'mean'
}).reset_index()

# Add coordinates
neighborhood_coords = {
    'Esenyurt': [41.0380, 28.6781],
    'Beylikdüzü': [41.0014, 28.6412],
    'Kağıthane': [41.0779, 28.9670],
    'Büyükçekmece': [41.0201, 28.5840],
    'Üsküdar': [41.0259, 29.0175],
    'Adalar': [40.8667, 29.1000],
    'Kadıköy': [40.9833, 29.0333],
    'Bağcılar': [41.0344, 28.8564],
    'Zeytinburnu': [40.9933, 28.9083],
    'Küçükçekmece': [40.9992, 28.8000],
    'Şişli': [41.0775, 28.9836],
    'Pendik': [40.8747, 29.2350],
    'Şile': [41.1731, 29.6111],
    'Beşiktaş': [41.0425, 29.0072],
    'Bakırköy': [40.9831, 28.8861],
    'Maltepe': [40.9247, 29.1311],
    'Avcılar': [40.9792, 28.7214],
    'Bahçelievler': [40.9949, 28.8639],
    'Arnavutköy': [41.0681, 29.0431],
    'Ataşehir': [40.9833, 29.1278],
    'Sarıyer': [41.1669, 29.0572],
    'Eyüpsultan': [41.0389, 28.9347],
    'Beykoz': [41.1342, 29.0922],
    'Gaziosmanpaşa': [41.0492, 28.9014],
    'Fatih': [41.0178, 28.9500],
    'Başakşehir': [41.0833, 28.8167],
    'Ümraniye': [41.0164, 29.1248],
    'Sancaktepe': [40.9833, 29.2000],
    'Sultanbeyli': [40.9645, 29.2657]
}

grouped['lat'] = grouped['neighborhood'].map(lambda x: neighborhood_coords.get(x, [None, None])[0])
grouped['lon'] = grouped['neighborhood'].map(lambda x: neighborhood_coords.get(x, [None, None])[1])

# Drop rows without coordinates
grouped.dropna(subset=['lat', 'lon'], inplace=True)

# Map Creation
istanbul_map = folium.Map(location=[41.015137, 28.979530], zoom_start=10)


# Create color scale
min_val = grouped['price_per_m2'].min()
max_val = grouped['price_per_m2'].max()
colormap = cm.linear.YlOrRd_09.scale(min_val, max_val)

# Create map
istanbul_map = folium.Map(location=[41.015137, 28.979530], zoom_start=10)

# Add circle markers
for _, row in grouped.iterrows():
    folium.CircleMarker(
        location=(row['lat'], row['lon']),
        radius=10,
        color=colormap(row['price_per_m2']),
        fill=True,
        fill_color=colormap(row['price_per_m2']),
        fill_opacity=0.8,
        popup=f"{row['neighborhood']}<br>{int(row['price_per_m2']):,} TL/m²",
        tooltip=f"{row['neighborhood']} - {int(row['price_per_m2']):,} TL/m²"
    ).add_to(istanbul_map)

# Add the color scale
colormap.caption = 'Average Price per m²'
colormap.add_to(istanbul_map)

# Show map in Streamlit
import streamlit.components.v1 as components
components.html(istanbul_map._repr_html_(), width=700, height=500)