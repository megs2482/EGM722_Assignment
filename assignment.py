import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
from shapely.geometry import Point, LineString, Polygon
import numpy as np

plt.ion()

# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):

    """For generating a legend

       Args: labels are the data labels
             colors will assign a colour
             edge is the colour of the label boundary
             alpha controls the transparency
    """
    lcolors = len(colors)
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lcolors], edgecolor=edge, alpha=alpha))
    return handles

# create a scale bar of length 20 km in the upper right corner of the map
# adapted this question: https://stackoverflow.com/q/32333870
# answered by SO user Siyh: https://stackoverflow.com/a/35705477

def scale_bar(ax, length=None, location=(0.85, 0.05), unit='km', linewidth='4'):

    """This function creates a scale bar

        args: ax is the axis to draw the scale bar
              length is the length of the scale bar in km
              location the  center of the scalebar in the axis coordinates
              linewidth is the thickness of the scalebar
              units is the name of the unit


    """

    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    sbllx = (llx1 + llx0) / 2  # centres the scale bar
    sblly = lly0 + (lly1 - lly0) * location[1]

    tmc = ccrs.TransverseMercator(sbllx, sblly)
    x0, x1, y0, y1 = ax.get_extent(tmc)  # extent of the map in metres.
    sbx = x0 + (x1 - x0) * location[0]  # plot the x location
    sby = y0 + (y1 - y0) * location[1]  # ploy the y location

    plt.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=6, transform=tmc)
    plt.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=4, transform=tmc)
    plt.plot([sbx-10000, sbx - 20000], [sby, sby], color='w', linewidth=4, transform=tmc)

    plt.text(sbx, sby-4500, '20 km', transform=tmc, fontsize=8)
    plt.text(sbx-12500, sby-4500, '10 km', transform=tmc, fontsize=8)
    plt.text(sbx-24500, sby-4500, '0 km', transform=tmc, fontsize=8)

# ---------------------------------------------------------------------------------------------------------------------------------------
# load the data

NIOutline = gpd.read_file('Shapefiles/NI_Outline.shp')   # Outline of Northern Ireland
MPAs = gpd.read_file('Shapefiles/UKSeaMap 2018 NI Inshore Clip.shp')  # Marine Protected Areas along NI Coast

# make sure the shapefiles have the correct are in the right coordinate system.

NIOutline = NIOutline.to_crs(epsg=32629)
MPAs = MPAs.to_crs(epsg=32629)

if NIOutline.crs == MPAs.crs:    # test the crs
    print('The NIOutline and MPAs crs are the same:', NIOutline.crs, MPAs.crs)
else:
    print('They do not have the same crs.')

# Once the datasets are loaded create a figure

myFig = plt.figure(figsize=(15, 15))  # create a figure of size 15x15 (page size in inches)
mycrs = ccrs.UTM(29)  # create a Universal Transverse Mercator reference system to transform our data.

ax = plt.axes(projection=ccrs.Mercator())

# Add the outline of Ireland and the Marine Protected Areas with Cartopy's ShapelyFeature

outline_feature = ShapelyFeature(NIOutline['geometry'], mycrs, edgecolor='black', facecolor='thistle')
xmin, ymin, xmax, ymax = NIOutline.total_bounds
ax.add_feature(outline_feature)

mpa_feature = ShapelyFeature(MPAs['geometry'], mycrs, edgecolor='paleturquoise', facecolor='paleturquoise', linewidth=1)
xmin, ymin, xmax, ymax = MPAs.total_bounds
ax.add_feature(mpa_feature)
ax.set_extent([xmin, xmax, ymin, ymax], crs=mycrs)  # Zoom into the area of interest

print(myFig)

# Load point data
# Shark, Skate and Ray point data
Flapperskate = gpd.read_file('Shapefiles/Flapperskate.shp')
SSHound = gpd.read_file('Shapefiles/SSHound.shp')
Spurdog = gpd.read_file('Shapefiles/Spurdog.shp')
Thornback = gpd.read_file('Shapefiles/Thornback.shp')

# Make sure the point data is in the same projection as the NI Outline and MPAs
Flapperskate = Flapperskate.to_crs(epsg=32629)
SSHound = SSHound.to_crs(epsg=32629)
Spurdog = Spurdog.to_crs(epsg=32629)
Thornback = Thornback.to_crs(epsg=32629)

if Flapperskate.crs == Spurdog.crs:
    print('The Flapperskate and Spurdog crs are the same:', Flapperskate.crs, Spurdog.crs)
else:
    print('They do not have the same crs.')

print(Spurdog.crs == MPAs.crs)

#  Plot points on the map

ax.plot(Flapperskate.geometry.x, Flapperskate.geometry.y, 'o', color='darkmagenta', linestyle='', transform=mycrs)
ax.plot(SSHound.geometry.x, SSHound.geometry.y, 'o', color='g', linestyle='', transform=mycrs)
ax.plot(Spurdog.geometry.x, Spurdog.geometry.y, 'o', color='crimson', linestyle='', transform=mycrs)
ax.plot(Thornback.geometry.x, Thornback.geometry.y, 'o', color='orange', linestyle='', transform=mycrs)


# Generate handles for the legend

Flapperskate_handle = generate_handles(['Flapperskate'], ['darkmagenta'], alpha=1)
SSHound_handle = generate_handles(['SSHound'], ['g'], alpha=1)
Spurdog_handle = generate_handles(['Spurdog'], ['crimson'], alpha=1)
Thornback_handle = generate_handles(['Thornback'], ['orange'], alpha=1)
MPA_handle = generate_handles(['Marine Protected Areas'], ['paleturquoise'], alpha=1)
NI_handle = generate_handles(['Northern Ireland Outline'], ['thistle'], alpha=1)

handles = Flapperskate_handle + SSHound_handle + Spurdog_handle \
          + Thornback_handle + MPA_handle + NI_handle
labels = ['Flapperskate', 'Starry-Smooth Hound', 'Spurdog', 'Thornback',
          'Marine Protected Areas', 'Northern Ireland Outline']

# create a legend
ax.legend(handles, labels, fontsize=10, loc='upper left', frameon=True, framealpha=1,
          title="Legend", title_fontsize=12)

# Add a title
plt.title('Map of Shark, Skate and Ray tagging locations off the NI Coast')

# Add a scale bar
scale_bar(ax, 20)

#  Add gridlines

gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-8, -7.5, -7, -6.5, -6, -5.5],
                         ylocs=[54, 54.5, 55, 55.5])
gridlines.right_labels = False  # turn off the right-side labels
gridlines.top_labels = False  # turn off the top labels

myFig.savefig('map.png', bbox_inches='tight', dpi=300)   # save figure


# ------------------------------------------------------------------------------------------------------------------
# Analysis

# Carry out a spatial join with the MPAs for Flapperskate data and Spurdog.

Spurdogjoin = gpd.sjoin(MPAs, Spurdog, how='inner', op='intersects')
print(Spurdogjoin)

FSkatejoin = gpd.sjoin(MPAs, Flapperskate, how='inner', op='intersects')
print(FSkatejoin)

# rename Sex__M_F_U column to Male_Female
FSkatejoin.rename(columns={'Sex__M_F_U': 'Male_Female', 'Decimal_De': 'DD'}, inplace=True)
Spurdogjoin.rename(columns={'Sex__M_F_U': 'Male_Female', 'Decimal_De': 'DD'}, inplace=True)

# Find out the total number of Spurdog tags located with in the MPA
Spurdogjoin['const'] = 1
Spurdogjoin.groupby(['Species']).sum()

# Calculate how many of the total Spurdog tags are Female
MaleOrFemale = Spurdogjoin.Male_Female.value_counts().F
print(MaleOrFemale)

# Then find out the total number of Flapperskate tags located with in the MPA
FSkatejoin['const'] = 1
FSkatejoin.groupby(['Species']).sum()

# and how many are female
MOrF = FSkatejoin.Male_Female.value_counts().F
print(MOrF)

# Plot the number of females tagged on a bar chart

data_dict = {'Flapperskate': 59, 'Spurdog': 44}
Species = list(data_dict.keys())
Values = list(data_dict.values())

plt.bar(Species, Values, color='green', width=0.5)
plt.ylabel('Number of tags')
plt.xlabel('Species')
plt.title('Number of Females tagged from each species')

plt.show


