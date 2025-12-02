
import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio
from rasterio.mask import mask

## City und districts ##
place = "Graz, Austria"
main_crs = "EPSG:31256"

#admin_osm_tags = {
#    "boundary": "administrative",
    #"admin_level": "9"
#}
#df_districts = ox.features_from_place(place, tags=admin_osm_tags).to_crs(main_crs)

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

#place = "Graz, Austria"
#main_crs = "EPSG:31256"
#raster_path = r"data/2021350_Mosaik_LC.tif"

#graz_boundary = ox.geocode_to_gdf(place)         # EPSG:4326
#graz_boundary = graz_boundary.to_crs(main_crs)   # EPSG:31256

#with rasterio.open(raster_path) as src:
#    print("Raster CRS:", src.crs)        #  EPSG:31256
#    print("Boundary CRS:", graz_boundary.crs)

#    shapes = [graz_boundary.geometry.iloc[0]]
#    out_image, out_transform = mask(src, shapes, crop=True)

#    out_meta = src.meta.copy()
#    out_meta.update({
#        "height": out_image.shape[1],
#        "width": out_image.shape[2],
#        "transform": out_transform
#    })

#output_raster = r"data/LC_graz2.tif"
#with rasterio.open(output_raster, "w", **out_meta) as dest:
#    dest.write(out_image)

