import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from shapely.geometry import Point, LineString, Polygon


def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

# create a scale bar of length 20 km in the upper right corner of the map
# adapted this question: https://stackoverflow.com/q/32333870
# answered by SO user Siyh: https://stackoverflow.com/a/35705477
def scale_bar(ax, location=(0.92, 0.95)):
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]

    tmc = ccrs.TransverseMercator(sbllx, sblly)
    x0, x1, y0, y1 = ax.get_extent(tmc)
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    plt.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=tmc)
    plt.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=6, transform=tmc)
    plt.plot([sbx-10000, sbx - 20000], [sby, sby], color='w', linewidth=6, transform=tmc)

    plt.text(sbx, sby-4500, '20 km', transform=tmc, fontsize=8)
    plt.text(sbx-12500, sby-4500, '10 km', transform=tmc, fontsize=8)
    plt.text(sbx-24500, sby-4500, '0 km', transform=tmc, fontsize=8)

#load data

NIOutline = gpd.read_file('Shapefiles/NI_Outline.shp')  #Outline of Northern Ireland
MPAs = gpd.read_file('Shapefiles/UKSeaMap 2018 NI Inshore Clip.shp') #Marine Protected Areas along NI Coast

#Shark, Skate and Ray point data
Bullhuss = gpd.read_file('Shapefiles/Bullhuss.shp')
Flapperskate = gpd.read_file('Shapefiles/Flapperskate.shp')
SSHound = gpd.read_file('Shapefiles/SSHound.shp')
Spurdog = gpd.read_file('Shapefiles/Spurdog.shp')
Thornback = gpd.read_file('Shapefiles/Thornback.shp')


#make sure the shapefiles have the correct crs. Using WGS84 UTM Zone 29N.

NIOutline = NIOutline.to_crs(epsg=32629)
MPAs = MPAs.to_crs(epsg=32629)
Bullhuss = Bullhuss.to_crs(epsg=32629)
Flapperskate = Flapperskate.to_crs(epsg=32629)
SSHound = SSHound.to_crs(epsg=32629)
Spurdog = Spurdog.to_crs(epsg=32629)
Thornback = Thornback.to_crs(epsg=32629)



#creating the figure for the map

myFig = plt.figure(figsize=(10, 10))  # create a figure of size 10x10 (representing the page size in inches)

mycrs = ccrs.UTM(29)  # create a Universal Transverse Mercator reference system to transform our data.
# be sure to fill in XX above with the correct number for the area we're working in.

ax = plt.axes(projection=ccrs.Mercator())

outline_feature = shapelyfeature(NIOutline['geometry'], mycrs, edgecolor= 'k', facecolor= 'w')
xmin, ymin, xmax, ymax = NIOutline.total_bounds
ax.add_feature(outline_feature)

ax.set_extent([xmin, xmax, ymin, ymax], crs=mycrs)


print(myFig)





