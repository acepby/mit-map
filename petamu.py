import geopandas as gpd
import pandas as pd
import numpy as np
import folium
from folium.features import GeoJsonTooltip
from flask import Flask, render_template

app = Flask(__name__)

#read geojson
geojson = gpd.read_file(r'geojson/kabukota-id.json')
geojson = geojson[['ADM2_PCODE','geometry']]

#read csv data
datamu = pd.read_csv(r'data/data-dummy.csv')

#join data to geojson
df = geojson.merge(datamu, left_on="ADM2_PCODE", right_on="ADM2_PCODE", how="outer")
df = df[~df['geometry'].isna()]

@app.route('/')
def index():
    id_map = folium.Map(location=[-1.7,118], zoom_start=5, tiles= 'openstreetmap')
    
    folium.Choropleth(
            geo_data=geojson,
            data=datamu,
            columns=['ADM2_PCODE', 'ADHA'],  #Here we tell folium to get the county fips and plot new_cases_7days metric for each county
            key_on='feature.properties.ADM2_PCODE', #Here we grab the geometries/county boundaries from the geojson file using the key 'coty_code' which is the same as county fips
            fill_color='RdYlGn',
            nan_fill_color="White", #Use white color if there is no data available for the county
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Jumlah Lokasi Salat Ied Adha 1444H ', #title of the legend
            highlight=True,
            line_color='black',
            bins=[0,10,50,100,250,500]
            ).add_to(id_map) 

    #id_map.save('index.html')
    #id_map
    return render_template('index.html', petamu=id_map._repr_html_())

if __name__ == '__main__' :
    app.run(debug=True)