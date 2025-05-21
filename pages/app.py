
import streamlit as st
import geemap
import ee
import os
import pandas as pd
import seaborn as sns

# Initialize Earth Engine
ee.Initialize()

# Initialize the map
Map = geemap.Map()

# Create sidebar controls
st.sidebar.header("Cropland Analysis")
selected_year = st.sidebar.selectbox("Select Year for ESRI Data", [2017, 2018, 2019, 2020, 2021])

# Add map layers for ESA and ESRI data
esa = ee.ImageCollection("ESA/WorldCover/v100").first()
esa_vis = {"bands": ["Map"]}
Map.addLayer(esa, esa_vis, "ESA Land Cover")
Map.add_basemap("HYBRID")

# Clip to coastal districts
gaul = ee.FeatureCollection('FAO/GAUL_SIMPLIFIED_500m/2015/level2')
odisha = gaul.filter(ee.Filter.eq('ADM1_NAME', 'Orissa'))
ganjam = gaul.filter(ee.Filter.eq('ADM2_NAME', 'Ganjam'))
puri = gaul.filter(ee.Filter.eq('ADM2_NAME', 'Puri'))
jagatsinghpur = gaul.filter(ee.Filter.eq('ADM2_NAME', 'Jagatsinghpur'))
kendrapada = gaul.filter(ee.Filter.eq('ADM2_NAME', 'Kendrapada'))
bhadrak = gaul.filter(ee.Filter.eq('ADM2_NAME', 'Bhadrak'))
baleswar = gaul.filter(ee.Filter.eq('ADM2_NAME', 'Baleshwar'))
coastal_dist = ganjam.merge(puri).merge(jagatsinghpur).merge(kendrapada).merge(bhadrak).merge(baleswar)

# ESA Cropland
cropland_esa = esa.eq(40).clipToCollection(coastal_dist).selfMask()
Map.addLayer(cropland_esa, {"palette": ["f096ff"]}, "ESA Cropland", False)

# ESRI data
esri = ee.ImageCollection("projects/sat-io/open-datasets/landcover/ESRI_Global-LULC_10m_TS")
esri_image = esri.filterDate(f"{selected_year}-01-01", f"{selected_year}-12-31").mosaic()
cropland_esri = esri_image.eq(5).clipToCollection(coastal_dist).selfMask()
Map.addLayer(cropland_esri, {"palette": ["#ab6c28"]}, f"ESRI Cropland {selected_year}", True)

# Gain and loss analysis
esri_2017 = esri.filterDate("2017-01-01", "2017-12-31").mosaic()
esri_2021 = esri.filterDate("2021-01-01", "2021-12-31").mosaic()
gain = esri_2017.neq(5).And(esri_2021.eq(5)).clipToCollection(coastal_dist).selfMask()
loss = esri_2017.eq(5).And(esri_2021.neq(5)).clipToCollection(coastal_dist).selfMask()
geemap.zonal_stats(gain, coastal_dist, "gain.csv", stat_type="SUM", scale=1000)
geemap.zonal_stats(loss, coastal_dist, "loss.csv", stat_type="SUM", scale=1000)

# Load into DataFrames
gain_df = geemap.csv_to_df("gain.csv")[["ADM2_NAME", "sum"]].rename(columns={"sum": "Gain"})
loss_df = geemap.csv_to_df("loss.csv")[["ADM2_NAME", "sum"]].rename(columns={"sum": "Loss"})

summary = pd.merge(gain_df, loss_df, on="ADM2_NAME", how="outer")
summary["Net Change"] = summary["Gain"] - summary["Loss"]
summary.fillna(0, inplace=True)

st.subheader("Cropland Gain/Loss Summary")
st.dataframe(summary)

# Download CSV
st.download_button(
    label="📥 Download Summary CSV",
    data=summary.to_csv(index=False).encode("utf-8"),
    file_name="cropland_gain_loss_summary.csv",
    mime="text/csv"
)

# Map display
Map.to_streamlit(height=600)
