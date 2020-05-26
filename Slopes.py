# Here we are importing useful libraries
import numpy as np
import richdem as rd
import urllib.request
import gdal
import os
import rasterio
import time
import concurrent.futures
from rasterio.merge import merge


# This is where we prepare to download the DEMs
textfile = open('Links_to_USGS_30m_DEM.txt','r')
urls = textfile.read().splitlines()


# Here we grab our mapping information from the CONUS grid
DEM_GeoTiff = gdal.Open('CONUS_DEM_250.tif',0)   
Projection = DEM_GeoTiff.GetProjection()                   # Grabbing projection
Geotransform = DEM_GeoTiff.GetGeoTransform()               # Grabbing geo-transform
Width = DEM_GeoTiff.RasterXSize                            # X-resolution
Height = DEM_GeoTiff.RasterYSize                           # Y-resolution
X_res = Geotransform[1]                                    # X-resolution
Y_res = Geotransform[5]                                    # Y-resolution
X_min = Geotransform[0]
Y_max = Geotransform[3]
X_max = X_min+X_res*Width
Y_min = Y_max+Y_res*Height
Extent = (X_min,Y_min,X_max,Y_max)
Resolution = (X_res,-Y_res)

i = 0

for url in urls:

	tile_id = url.split('/')[7]
	name = f'{tile_id}.tif'
	urllib.request.urlretrieve(url,'/Users/jackson/Desktop/Execute/'+tile_id+'.tif')

	# We must reproject our DEM tile
	gdal.Warp(name,name,dstSRS = Projection)

	# Now we run the the BTH over our DEM tile
	Tile_GeoTiff = gdal.Open(name,0)
	T = Tile_GeoTiff.GetGeoTransform()
	P = Tile_GeoTiff.GetProjection()
	Tile_Array = rd.LoadGDAL(name)


	Slopes = rd.TerrainAttribute(Tile_Array, attrib = 'slope_riserun')


	filename = name                                       
	driver = gdal.GetDriverByName('GTiff')                   
	dataset = driver.Create(filename,Slopes.shape[1],
		Slopes.shape[0], 1,gdal.GDT_Float32)                                    
	dataset.GetRasterBand(1).WriteArray(Slopes)            
	dataset.SetGeoTransform(T)                   
	dataset.SetProjection(P)                      
	dataset.FlushCache()                                       
	dataset=None                                              

	# Preparing to add our new tile to the mosaic
	src_files_to_mosaic = []
	src = rasterio.open('Topo_Slope.tif')
	src_files_to_mosaic.append(src)
	src = rasterio.open(name)
	src_files_to_mosaic.append(src)

	os.remove('/Users/jackson/Desktop/Execute/'+tile_id+'.tif')

	# Adding to Mosaic
	mosaic, out = merge(src_files_to_mosaic, method='first',
		bounds=Extent, res=Resolution,nodata=-9999)
	mosaic = np.reshape(mosaic,(Height,Width))

	# Using GDAL to write the output raster
	filename = 'Topo_Slope.tif'                               # Tiff holding Black Top Hat
	driver = gdal.GetDriverByName('GTiff')                    # Driver for writing geo-tiffs
	dataset = driver.Create(filename,Width, Height, 
		1,gdal.GDT_Float32)                                    # Creating our tiff file
	dataset.GetRasterBand(1).WriteArray(mosaic)                # Writing values to our tiff
	dataset.SetGeoTransform(Geotransform)                      # Setting geo-transform
	dataset.SetProjection(Projection)                          # Setting the projection
	dataset.FlushCache()                                       # Saving tiff to disk
	dataset=None

	i = i+1
	j = str(i)
	print(j)