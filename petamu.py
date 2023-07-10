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


@app.route('/')
def index():
    id_map = folium.Map(location=[-1.7,118], zoom_start=5, tiles=None, overlay= False, prefer_canvas=True)
    fg1 = folium.FeatureGroup(name='Jumlah Lokasi Idul Adha 1444H', overlay=False).add_to(id_map)
    fg2 = folium.FeatureGroup(name='Penghimpunan Zakat', overlay=False).add_to(id_map)
    
    idAdha = folium.Choropleth(
            geo_data=df,
            data=df,
            columns=['ADM2_PCODE', 'ADHA'],  #Here we tell folium to get id of kabupaten/kota and data which we want to display
            key_on='feature.properties.ADM2_PCODE', #Here we grab the geometries/county boundaries from the geojson file using the key ADM2_PCODE 
            fill_color='RdYlGn',
            nan_fill_color="White", #Use white color if there is no data available for the county
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Jumlah Lokasi Salat Ied Adha 1444H ', #title of the legend
            highlight=True,
            line_color='black',
            bins=[0,10,50,100,250,500]
            ).geojson.add_to(fg1)
    
    #feature tooltips
    folium.features.GeoJson(
                    data=df,
                    name='Jumlah Lokasi Salat Idul Adha 1444H',
                    smooth_factor=2,
                    style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['ADM2_EN',
                                'ADHA'
                               ],
                        aliases=["Daerah:",
                                 "Jml Lokasi Ied:"
                                ], 
                        localize=True,
                        sticky=False,
                        labels=True,
                        style="""
                            background-color: #F0EFEF;
                            border: 2px solid black;
                            border-radius: 3px;
                            box-shadow: 3px;
                        """,
                        max_width=800,),
                            highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
                        ).add_to(idAdha)
    
    zakat = folium.Choropleth(
            geo_data=df,
            data=df,
            columns=['ADM2_PCODE', 'ZAKAT'],  #Here we tell folium to get id of kabupaten/kota and data which we want to display
            key_on='feature.properties.ADM2_PCODE', #Here we grab the geometries/county boundaries from the geojson file using the key ADM2_PCODE 
            fill_color='RdYlGn',
            nan_fill_color="White", #Use white color if there is no data available for the county
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Jumlah Penghimpunan Zakat ', #title of the legend
            highlight=True,
            line_color='black',
            bins= 5
            ).geojson.add_to(fg2)
    
    #feature tooltips
    folium.features.GeoJson(
                    data=df,
                    name='Jumlah Penghimpunan Zakat',
                    smooth_factor=2,
                    style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['ADM2_EN',
                                'ZAKAT'
                               ],
                        aliases=["Daerah:",
                                 "Zakat terhimpun:"
                                ], 
                        localize=True,
                        sticky=False,
                        labels=True,
                        style="""
                            background-color: #F0EFEF;
                            border: 2px solid black;
                            border-radius: 3px;
                            box-shadow: 3px;
                        """,
                        max_width=800,),
                            highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
                        ).add_to(zakat)
    
    folium.TileLayer('cartodbdark_matter',overlay=True,name="View in Dark Mode").add_to(id_map)
    folium.TileLayer('cartodbpositron',overlay=True,name="Viw in Light Mode").add_to(id_map)
    folium.LayerControl(collapsed=False).add_to(id_map)

    #id_map.save('index.html')
    #id_map
    return render_template('index.html', petamu=id_map._repr_html_())

if __name__ == '__main__' :
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)