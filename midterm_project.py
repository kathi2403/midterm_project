
## Mid-Term Project, Group 2 ##

import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from rasterio.features import shapes
from shapely.geometry import shape
import numpy as np

## City und districts ##
place = "Graz, Austria"
main_crs = "EPSG:31256"

gdf_boundaries = ox.features_from_place(
    place,
    tags={"boundary": "administrative"}
)
## with filter, just districts graz
df_districts = gdf_boundaries[gdf_boundaries["admin_level"] == "9"]
df_districts = df_districts.to_crs(main_crs)


## OSM Tags ##
tags_osm = {
    "leisure": ["park", "pitch", "playground", "sports_centre", "stadium"],
    "natural": ["water", "wetland"],
    #"route": ["hiking", "foot", "bicycle", "mtb"], => empty
}
graz_tags = ox.features_from_place(place, tags=tags_osm).to_crs(main_crs)

graz_leisure = graz_tags[graz_tags["leisure"].notna()]
graz_water = graz_tags[graz_tags["natural"].notna()]
#graz_routes = graz_tags[graz_tags["route"].notna()]

## Plot
#fig, ax = plt.subplots(figsize=(12,12))
#df_districts.boundary.plot(ax=ax, color="black", linewidth=1)
#graz_leisure.plot(ax=ax, color="green", alpha=0.6, edgecolor="none")
#graz_water.plot(ax=ax, color="blue", alpha=0.6, edgecolor="none")
#graz_routes.plot(ax=ax, color="black", alpha=0.6, edgecolor="none")
#ax.set_title("leisure, natural, routes, Graz, districts")
#ax.set_axis_off()
#plt.show()

## Graph ##

#version 1, everything what is permitted for pedestrians
#graph = ox.graph_from_place(place, network_type='walk', simplify=True)
#graph = ox.project_graph(graph, to_crs=main_crs)
#fig, ax = ox.plot_graph( graph, node_size=5, bgcolor="white", node_color="black", edge_color="black")

#version 2, only dedicated pedestrian paths
filter = '["highway"~"footway|path|pedestrian"]'
graph2 = ox.graph_from_place(place, network_type="walk", custom_filter=filter, simplify=True)
graph2 = ox.project_graph(graph2, to_crs=main_crs)
fig, ax = ox.plot_graph(graph2, node_size=0, bgcolor="white", edge_color="black")

## Land Cover ##

raster_path = r"data/2021350_Mosaik_LC.tif"

graz_boundary = ox.geocode_to_gdf(place).to_crs(main_crs)

with rasterio.open(raster_path) as src:
    out_image, out_transform = mask(src, [graz_boundary.geometry.iloc[0]], crop=True)  #clip raster to city boundary
    lc = out_image[0] #extract land cover layer
    valid_mask = lc != src.nodata if src.nodata else np.ones_like(lc, dtype=bool) #no nan data (filter valid data)

gdf = gpd.GeoDataFrame([
    {"geometry": shape(geom), "lc": int(value)} 
    for geom, value in shapes(lc, mask=valid_mask, transform=out_transform) #raster to polygon 
], crs=main_crs)

gdf.to_file(r"LC_graz.gpkg", driver="GPKG")



