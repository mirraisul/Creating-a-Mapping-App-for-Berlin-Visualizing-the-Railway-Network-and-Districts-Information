import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import leafmap.foliumap as leafmap

#set the name of the tab
st.set_page_config(page_title='Berlin Map', layout='wide')

st.title('Railways and Districts in Berlin')

#st.sidebar.title('About')
st.sidebar.info('This app visualizes the districts and railway network in Berlin')

#path= "E:/Study/ONLINE_COURSE/1_PythonDataviz/Day_25/Personal_dashboard/QGIS/"
area_file= "Berlin_districts.shp" #area file of Berlin
#roads_file= "Roads_Berlin.shp" #road network of Berlin
railways_file= "Railways_Berlin.shp" #railway network in Berlin

@st.cache_data
def read_gdf(file_path):
    gdf = gpd.read_file(file_path)
    return gdf


#Now read the files using function
#berlin_path= path + area_file
berlin_path= area_file
#roads_path= path + roads_file
#railway_path= path + railways_file
railway_path= railways_file

berlin= read_gdf(berlin_path)
berlin = berlin.rename(columns={"Gemeinde_n": "District"}) #rename the column Gemeinde_n as District
berlin = berlin[["District", "Area_km2", "geometry"]]
#road= read_gdf(roads_path)
railway= read_gdf(railway_path)


# Create the chart
districts = berlin.District.values
district = st.sidebar.selectbox('Select a District', districts)
overlay = st.sidebar.checkbox('Overlay Railway Network')


#Now create the side bar plot of KPI
district_area = berlin[berlin["District"]==district].Area_km2.values[0]
total_area= berlin.Area_km2.values.sum()
district_area_perc= district_area/total_area
rest_area_perc= 1 - district_area_perc
#district_area = lengths_df[lengths_df['DISTRICT'] == district]

# Define your values and labels
values = [district_area_perc, rest_area_perc]
labels = [district, 'Rest of the Berlin']
colors = ['#A7D8F4', '#9E7F61']

# Create the pie chart
fig, ax = plt.subplots()
ax.pie(values, labels=None, colors=colors, autopct='%1.1f%%', startangle=90)
# Add a legend with the labels
ax.legend(labels, loc="upper right", fontsize= 7)

# Display the pie chart in the Streamlit sidebar
st.sidebar.pyplot(fig)


## Create the map
#first create a select box to create a basemap
basemap= st.selectbox('Select a Basemap', ['CartoDB.DarkMatter', 'OpenStreetMap', 'CartoDB.Positron',])
m = leafmap.Map(
    layers_control=True,
    draw_control=False,
    measure_control=False,
    fullscreen_control=False,
)
m.add_basemap(basemap)

m.add_gdf(
    gdf=berlin,
    zoom_to_layer=True,
    layer_name='Districts',
    info_mode='on_hover',
    style={'color': 'white', 'fillOpacity': 0.4, 'weight': 0.9, 'fillColor': "#9E7F61"},
    )

selected_gdf = berlin[berlin['District'] == district]

m.add_gdf(
    gdf=selected_gdf,
    layer_name='selected',
    zoom_to_layer=False,
    info_mode="on_hover",
    style={'color': '#A7D8F4', 'fillColor': '#A7D8F4', 'fillOpacity': 0.7, 'weight': 2}
    #style={'fillColor': 'blue', 'fill': 0.9, 'weight': 2}
 )

if overlay:
    m.add_gdf(
        gdf=railway,
        zoom_to_layer=False,
        layer_name='Railway',
        info_mode=None,
        style={'color': 'red', 'weight': 0.5},
    )


m_streamlit = m.to_streamlit(900, 650)