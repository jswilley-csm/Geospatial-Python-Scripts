##########################################################################################
#                                                                                        #
#      ----------------->  Black Top Hat Transform for CONUS  <------------------        #
#                                                                                        #                                      
##########################################################################################
                                                                                        
                                                                                      
#--------------------------- Here we read in useful libraries ---------------------------#

import numpy as np
import urllib.request
import gdal
import os
import rasterio
from rasterio.merge import merge
from rasterio.plot import show
from skimage.morphology import black_tophat                # Computes our BTH transform
from skimage.morphology import disk                        # Creates structuring element


# ------------ Here we grab our mapping information from the CONUS grid ---------------- #
DEM_GeoTiff = gdal.Open('CONUS_DEM_250.tif',0)   
Projection = DEM_GeoTiff.GetProjection()                   # Grabbing projection
Geotransform = DEM_GeoTiff.GetGeoTransform()               # Grabbing geo-transform
Width = DEM_GeoTiff.RasterXSize                            # Array dimensions
Height = DEM_GeoTiff.RasterYSize                           # Array dimensions
X_res = Geotransform[1]                                    # X-resolution
Y_res = Geotransform[5]                                    # Y-resolution
X_min = Geotransform[0]                                    # Used to determine extent
Y_max = Geotransform[3]                                    # Used to determine extent
X_max = X_min+X_res*Width                                  # Used to determine extent
Y_min = Y_max+Y_res*Height                                 # Used to determine extent
Extent = (X_min,Y_min,X_max,Y_max)                         # Used when creating mosaic
Resolution = (X_res,-Y_res)                                # Used when creating mosaic


# --------------- We use these hyperlinks to pull down USGS DEM data ------------------- #

textfile = open('Links_to_USGS_30m_DEM.txt','r')           # Reads in hyperlink textfile
list = textfile.read().splitlines()                        # Creates indexed list of links


# --------------- We use these hyperlinks to pull down USGS DEM data ------------------- #

for i in range(1,len(list)):                               # This loops through every link
	
	print(i)                                               # Helpful if code crashes
	
	url = list[i]                                       
	urllib.request.urlretrieve(url,
		'/Users/jackson/Desktop/BTH/working/Tile.tif')     # Pulls in the 30m DEM "Tile"
	gdal.Warp('Tile.tif','Tile.tif',dstSRS = Projection)   # Re-projecting 30m DEM

	Tile_GeoTiff = gdal.Open('Tile.tif',0)                 # Reading the reprojected tile
	T = Tile_GeoTiff.GetGeoTransform()                     # Getting transform
	P = Tile_GeoTiff.GetProjection()                       # Getting projection
	DEM_Array = Tile_GeoTiff.ReadAsArray()                 # Reading tile as array
	window = disk(20)                                      # Setting search radius for BTH
	BTH_Array = black_tophat(DEM_Array,window)             # Performing Black Top Hat 

	filename = 'Tile.tif'                                  # Writing out BTH results      
	driver = gdal.GetDriverByName('GTiff')                 
	dataset = driver.Create(filename,BTH_Array.shape[1],
		BTH_Array.shape[0], 1,gdal.GDT_Float32)                                    
	dataset.GetRasterBand(1).WriteArray(BTH_Array)            
	dataset.SetGeoTransform(T)                              # Setting geo-transform                                       
	dataset.SetProjection(P)                                # Setting the projection                     
	dataset.FlushCache()                                    # Saving tiff to disk                                       
	dataset=None                                            # Clearing variable name                                              

	src_files_to_mosaic = []                                # Initializing mosaic input
	src = rasterio.open('Tile.tif')                         # Grabbing the BTH results
	src_files_to_mosaic.append(src)                         # Appending BTH results
	src = rasterio.open('BTH.tif')                          # Grabbing results geo tiff
	src_files_to_mosaic.append(src)                         # Appending results geo tiff

	mosaic, out = merge(src_files_to_mosaic,
		method='first',
		bounds=Extent, res=Resolution,
		nodata=None)                                       # Mosaic-ing in BTH results 
	mosaic = np.reshape(mosaic,(Height,Width))             # Reshaping results

	filename = 'BTH.tif'                                    # Tiff holding Black Top Hat
	driver = gdal.GetDriverByName('GTiff')                  # Driver for writing geo-tiffs
	dataset = driver.Create(filename,Width, Height, 
		1,gdal.GDT_Float32)                                 # Creating our tiff file
	dataset.GetRasterBand(1).WriteArray(mosaic)             # Writing values to our tiff
	dataset.SetGeoTransform(Geotransform)                   # Setting geo-transform
	dataset.SetProjection(Projection)                       # Setting the projection
	dataset.FlushCache()                                    # Saving tiff to disk
	dataset=None                                            # Clearing variable name
	
	os.remove('Tile.tif')                                   # Removing the tile DEM


#----------------------------------------------------------------------------------------#
#     >>>>>>>>>>>>>>>>>>>>>  TH-th-th-th-that's All Folks!  <<<<<<<<<<<<<<<<<<<<<<<      #
#----------------------------------------------------------------------------------------#



