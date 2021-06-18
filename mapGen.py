import folium       #used for visualizing geospatial data
import pandas       #data analysis and manipulation tool or library


data = pandas.read_csv( "importedFiles/Volcanoes.txt" )     #creates a data frame

theLatitudes = list(data["LAT"])                #makes a list from the LON column from Volcanoes.txt
theLongitudes = list(data["LON"])               
theVolcanoesName = list(data["NAME"])           
theElevation = list(data["ELEV"])               

def color_producer( elevation ):        #function for volcano marker colours by elevation
    if elevation < 1000:
        return 'green'
    
    elif 1000 <= elevation < 3000:
        return 'orange'
    
    else:
        return 'red'


html = """

Hi! I'm <br>
Volcano: <a href="https://www.google.com/search?q=%%22%s%%22" 
            target="_blank">%s</a> 
            <br>
Height: %s m

"""     #for iframe for each volcano markers


map = folium.Map(                       #map object created in folium. Feature groups will be added to it.
    location = [ 38.58 , -99.09 ],      #kansas center lat and lon
    zoom_start = 5,                     #zoom_start = 4 for North America view, 5 for USA view
    tiles = "Stamen Terrain" )          #other tileset options built into folium

theFeatureGroupPopulation = folium.FeatureGroup( name = "2005 Population" )     #for more layers and organization

theFeatureGroupPopulation.add_child(                                          
    folium.GeoJson(                                                 #GeoJson polygon 2005 data
        data = open( 'importedFiles/world_2005.json' , 
                     'r' , 
                      encoding='utf-8-sig').read() ,
        
        # style_function = lambda x: {      #By different colours
        #     'fillColor' : '#FFCC00' if x[ 'properties' ][ 'POP2005' ] < 10000000 
        #     else '#FF9900' if 10000000 <= x[ 'properties' ][ 'POP2005' ] < 20000000
        #     else '#FF6600' if 20000000 <= x[ 'properties' ][ 'POP2005' ] < 100000000
        #     else '#FF0000' if 100000000 <= x[ 'properties' ][ 'POP2005' ] < 500000000
        #     else '#990000' , 'fillOpacity' : '.5'
        #     },
        
        style_function = lambda x: {        #By single colour opacities
            'fillColor' : '#FF6600',       
            'fillOpacity' : '0.1' if x[ 'properties' ][ 'POP2005' ] < 5000000 
            else '0.15' if 5000000 <= x[ 'properties' ][ 'POP2005' ] < 10000000
            else '0.3' if 10000000 <= x[ 'properties' ][ 'POP2005' ] < 20000000
            else '0.45' if 20000000 <= x[ 'properties' ][ 'POP2005' ] < 100000000
            else '0.6' if 100000000 <= x[ 'properties' ][ 'POP2005' ] < 500000000
            else '0.75'
            },
        
        # zoom_on_click = True ,
                
        ))      

theFeatureGroupVolcanoes = folium.FeatureGroup( name = "Volcanoes" )        

for theLat, theLon, theName, theElev in zip( theLatitudes, 
                                             theLongitudes, 
                                             theVolcanoesName, 
                                             theElevation ):       #To iterate multiple values in an array or list
    
    iframe = folium.IFrame( html = html % ( theName , theName , theElev ), 
                            width = 200, 
                            height = 100 )      #to google search by clicking volcano name in popup
    
    # theFeatureGroup.add_child(folium.Marker(location=[theLat, theLon], popup="Hi! I'm %s with an elevation of %s" % (theName,theElev), icon=folium.Icon(color='green')))
    
    theFeatureGroupVolcanoes.add_child(
        folium.CircleMarker(
            location = [ theLat , theLon ], 
            popup = folium.Popup( iframe ),
            radius = 10,
            color = 'black', 
            opacity = 1, 
            fill_color = color_producer( theElev ), 
            fill_opacity = 0.75 ),)


map.add_child( theFeatureGroupPopulation )
map.add_child( theFeatureGroupVolcanoes )

map.add_child( folium.LayerControl() )      #To select the visible layers, top right corner

map.save( "generatedFiles/Map.html" )

