
##########################################################################################
#                                                                                        #
#        -------------------->  Valley Depth Calculations  <----------------             #
#                                                                                        #                                      
##########################################################################################

                                                                                                                                                       
#--------------------------- Here we read in useful lybraries ---------------------------#

import numpy as np                                         # Useful for arrays and math
import gdal                                                # Useful for rasters
import geopandas as gpd                                    # Useful for shapefiles
import matplotlib.pyplot as plt                            # Useful for visualization
from osgeo import ogr                                      # Useful for driver
from rasterstats import zonal_stats                        # Useful for zonal statistics
from skimage.morphology import black_tophat                # Computes our BTH transform
from skimage.morphology import disk                        # Creates structuring element


#----------------------------- Here we read in our datasets -----------------------------#

DEM_GeoTiff= gdal.Open('CONUS_DEM_250.tif',1)              # Black Top Hat geo-tif
DEM_Array = DEM_GeoTiff.ReadAsArray()                      # Black Top Hat array
BTH_GeoTiff= gdal.Open('CONUS_BTH_250.tif',1)              # Black Top Hat geo-tif
BTH_Array = BTH_GeoTiff.ReadAsArray()                      # Black Top Hat array
driver = ogr.GetDriverByName("ESRI Shapefile")             # Grabbing ERRI driver
Stream_Shape = driver.Open('NHD_Plus_Streams.shp', 0)      # Use driver to open shapefile
HUC_Shape = gpd.read_file('HUC_Valley_Depth.shp')           # Use driver to open shapefile


#----------------------------- Here we grab some useful info ----------------------------#

[height,width] = DEM_Array.shape                           # Grabbing array dimensions
Projection = DEM_GeoTiff.GetProjection()                   # Grabbing projection
Geotransform = DEM_GeoTiff.GetGeoTransform()               # Grabbing geo-transform
x_res = DEM_GeoTiff.RasterXSize                            # X-resolution
y_res = DEM_GeoTiff.RasterYSize                            # Y-resolution
layer = Stream_Shape.GetLayer()                            # Shapefile layer to be written


#--------------------------- Here we write a stream mask file ---------------------------#

Stream_GeoTiff = gdal.GetDriverByName('GTiff').Create(
	'Stream_Mask_tif', x_res, y_res, 1, gdal.GDT_Byte)     # Here we create our blank tif
Stream_GeoTiff.SetGeoTransform(Geotransform)               # Now we assign a geo-transform
Stream_GeoTiff.SetProjection(Projection)                   # We set our tif's projection
gdal.RasterizeLayer(Stream_GeoTiff, [1], layer, 
	None, None, [1], ['ALL_TOUCHED=TRUE'])                 # We rasterize the streams
Stream_Array = Stream_GeoTiff.ReadAsArray()                # Create an array from streams
Stream_GeoTiff.FlushCache()                                # This saves our tif
Stream_GeoTiff = None                                      # This clears the variable name


#-------------------------- We find valley depth along streams --------------------------#

BTH_Array = np.where(BTH_Array<0, 0.0, BTH_Array)
Stream_Array = Stream_Array * BTH_Array                    # Depth of incision at streams
filename = 'Depth_Along_Streams.tif'                       # Tiff holding valley depths
driver = gdal.GetDriverByName('GTiff')                     # Driver for writing geo-tiffs
dataset = driver.Create(filename,x_res, y_res, 
	1,gdal.GDT_Float32)                                    # Creating our tiff file
dataset.GetRasterBand(1).WriteArray(Stream_Array)          # Writing values to our tiff
dataset.SetGeoTransform(Geotransform)                      # Setting geo-transform
dataset.SetProjection(Projection)                          # Setting the projection
dataset.FlushCache()                                       # Saving tiff to disk
dataset=None                                               # Clearing variable name



#------------------------------ We find stats for each HUC ------------------------------#

statistics = zonal_stats('HUC_Valley_Depth.shp', 
	'Depth_Along_Streams.tif', nodata = 0, 
	stats = ['mean'])                                      # Zonal statistics from python



#------------------------ We write valley depth to a shapefile --------------------------#	
	
means = np.zeros([len(statistics),1],dtype = float)        # Creating a blank array
for i in range(0,len(statistics)):	
	if(str(statistics[i])[9:13]!='None'):                  
		stop = len( str( statistics[i] ) ) - 2
		means[i] = float( str( statistics[i] )[9:stop] )                               
	else: means[i] = None 
HUC_Shape['valley_d'] = means                              # Appending valley depths
HUC_Shape.to_file('HUC_Valley_Depth.shp',
	 driver='ESRI Shapefile')                              # Here we write our shapefile
	 
	 
#----------------------------------------------------------------------------------------#
#     >>>>>>>>>>>>>>>>>>>>>  TH-th-th-th-that's All Folks!  <<<<<<<<<<<<<<<<<<<<<<<      #
#----------------------------------------------------------------------------------------#
