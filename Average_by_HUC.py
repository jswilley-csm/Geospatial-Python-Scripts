##########################################################################################
#                                                                                        #
#                  -------------->  Average By HUC    <---------------                   #
#                                                                                        #                                      
##########################################################################################


#--------------------------- Here we read in useful lybraries ---------------------------#

import numpy as np                                         # Useful for arrays and math
import gdal                                                # Useful for rasters
import geopandas as gpd                                    # Useful for shapefiles
from osgeo import ogr                                      # Useful for driver
from rasterstats import zonal_stats                        # Useful for zonal statistics


#----------------------------- Here we read in our datasets -----------------------------#

GeoTiff= gdal.Open('Topo_Slope.tif',1)                     # Recharge geo-tif
Array = GeoTiff.ReadAsArray()                              # Recharge array
HUC_Shape = gpd.read_file('FINAL_CONUS.shp')               # Use driver to open shapefile


#----------------------------- Here we grab some useful info ----------------------------#

[height,width] = Array.shape                               # Grabbing array dimensions
Projection = GeoTiff.GetProjection()                       # Grabbing projection
Geotransform = GeoTiff.GetGeoTransform()                   # Grabbing geo-transform
x_res = GeoTiff.RasterXSize                                # X-resolution
y_res = GeoTiff.RasterYSize                                # Y-resolution


#------------------------------ Here we do some processing ------------------------------#

Array = np.where(Array < 0, 0.0, Array)
#Array = Array/3600                                        # converting from m/hr to m/s
Array = Array*10**3                                        # will divide by 10^3 later
                                                           # this avoids scientific 
                                                           # notation in stats output
#-------------------------- Here we write our processed raster --------------------------#

filename = 'Processed_Slope.tif'                           # Tiff holding slopes
driver = gdal.GetDriverByName('GTiff')                     # Driver for writing geo-tiffs
dataset = driver.Create(filename,x_res, y_res, 
	1,gdal.GDT_Float32)                                    # Creating our tiff file
dataset.GetRasterBand(1).WriteArray(Array)                 # Writing values to our tiff
dataset.SetGeoTransform(Geotransform)                      # Setting geo-transform
dataset.SetProjection(Projection)                          # Setting the projection
dataset.FlushCache()                                       # Saving tiff to disk
dataset=None                                               # Clearing variable name



#------------------------------ We find stats for each HUC ------------------------------#

statistics = zonal_stats('FINAL_CONUS.shp', 
	'Processed_Slope.tif', nodata = 0, 
	stats = ['mean'])                                      # Zonal statistics from python



#------------------------ We write valley depth to a shapefile --------------------------#	
	
means = np.zeros([len(statistics),1],dtype = float)        # Creating a blank array
for i in range(69980,len(statistics)):	
	if(str(statistics[i])[9:13]!='None'):                  
		stop = len( str( statistics[i] ) ) - 5
		means[i] = float( str( statistics[i] )[9:stop] )                           
	else: means[i] = None 
	
HUC_Shape['S (m/m)'] = means/10**3                         # Appending slopes
HUC_Shape.to_file('FINAL_CONUS_test.shp',
	 driver='ESRI Shapefile')                              # Here we write our shapefile
	 
	 
#----------------------------------------------------------------------------------------#
#     >>>>>>>>>>>>>>>>>>>>>  TH-th-th-th-that's All Folks!  <<<<<<<<<<<<<<<<<<<<<<<      #
#----------------------------------------------------------------------------------------#








