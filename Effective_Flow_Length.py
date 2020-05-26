##########################################################################################
#                                                                                        #
#       ----------------->  Average Flow Length Calculations  <-----------------         #
#                                                                                        #                                      
##########################################################################################
                                                                                        
                                                                                      
#--------------------------- Here we read in useful libraries ---------------------------#

import numpy as np                                         # Useful for arrays and math
import gdal                                                # Useful for rasters
import geopandas as gpd                                    # Useful for shapefiles
from osgeo import ogr                                      # Useful for driver


#----------------------------- Here we read in our datasets -----------------------------#

DEM_GeoTiff= gdal.Open('DEM.tif',1)                        # DEM geo-tif
DEM_Array = DEM_GeoTiff.ReadAsArray()                      # DEM array
driver = ogr.GetDriverByName("ESRI Shapefile")             # Grabbing ERRI driver
Stream_Shape = driver.Open('USGS_Streams.shp', 0)          # Use driver to open shapefile
HUC_Shape = gpd.read_file('CONUS_HUCs.shp')                # Use pandas to open shapefile



#----------------------------- Here we grab some useful info ----------------------------#

[height,width] = DEM_Array.shape                           # Grabbing array dimensions
Projection = DEM_GeoTiff.GetProjection()                   # Grabbing projection
Geotransform = DEM_GeoTiff.GetGeoTransform()               # Grabbing geo-transform
x_res = DEM_GeoTiff.RasterXSize                            # X-resolution
y_res = DEM_GeoTiff.RasterYSize                            # Y-resolution
layer = Stream_Shape.GetLayer()                            # Shapefile layer to be written



#--------------------------- Here we write a stream mask file ---------------------------#

Stream_GeoTiff = gdal.GetDriverByName('GTiff').Create(
	'Stream_Mask.tif', x_res, y_res, 1, gdal.GDT_Byte)     # Here we create our blank tif
Stream_GeoTiff.SetGeoTransform(Geotransform)               # Now we assign a geo-transform
Stream_GeoTiff.SetProjection(Projection)                   # We set our tif's projection
gdal.RasterizeLayer(Stream_GeoTiff, [1], layer, 
	None, None, [1], ['ALL_TOUCHED=TRUE'])                 # We rasterize the streams
Stream_Array = Stream_GeoTiff.ReadAsArray()                # Create an array from streams
Stream_GeoTiff.FlushCache()                                # This saves our tif
Stream_GeoTiff = None                                      # This clears the variable name



#-------------------------- Here we find our proximity values ---------------------------#

Drainage_GeoTiff = gdal.GetDriverByName('GTiff').Create(
	'Stream_Mask.tif', x_res, y_res, 1, gdal.GDT_Byte)     # Here we create our blank tif
Drainage_GeoTiff.SetGeoTransform(Geotransform)             # Now we assign a geo-transform
Drainage_GeoTiff.SetProjection(Projection)                 # We set our tif's projection
Drainage_GeoTiff.FlushCache()                              # This saves our tif
Drainage_GeoTiff = None                                    # This clears the variable name


# gdal_proximity.py Stream_Mask.tif proximity.tif          # I ended up needing to run the 
                                                           # command seen here in terminal
                                                           # to get the syntax to work

#----------------------------------------------------------------------------------------#
#     >>>>>>>>>>>>>>>>>>>>>  TH-th-th-th-that's All Folks!  <<<<<<<<<<<<<<<<<<<<<<<      #
#----------------------------------------------------------------------------------------#


