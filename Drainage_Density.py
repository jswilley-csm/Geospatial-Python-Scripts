
##########################################################################################
#                                                                                        #
#      -------------------->  Drainage Density Calculations  <----------------           #
#                                                                                        #                                      
##########################################################################################

 
#--------------------------- Here we read in useful libraries ---------------------------#

import geopandas as gpd
import pandas as pd
import rtree
import numpy as np


#---------------------------- Here we read in HUC shapefile -----------------------------#

HUC_copy = gpd.read_file('FINAL_CONUS.shp')                  # Reading in HUC shape
areas = HUC_copy.area                                        # Calculating HUC areas
areas = areas.array                                          # Converting to array
HUC_copy['areaJS'] = areas                                   # Appending areas


#--------------------------- Here we read in stream shapefile ---------------------------#

stream = gpd.read_file('NHD_Plus_Streams.shp')


#---------------------------- Here we join the two shapefiles ---------------------------#

joined = gpd.sjoin(stream, HUC_copy, op='within')


#------------------------- Here we dissolve the Streams by HUC --------------------------#

dissolved=joined.dissolve(by='id')                            # Dissolving streams by HUC
lengths = dissolved.length                                    # Calculating Lengths
lengths = lengths.array * 2                                   # Draining from both sides
dissolved['lengthJS'] = lengths                               # Appending lengths


#--------------------------- Here calculate drainage density ----------------------------#

densities = dissolved.lengthJS/dissolved.areaJS               # Density equation
dissolved['densities'] = densities                            # Appending values to shape
dissolved.to_file('dissolved_Streams.shp',
	 driver='ESRI Shapefile') 	                              # Writing shape to file
dissolved = gpd.read_file('dissolved_streams.shp')            # Reading back in
joined_2 =  gpd.sjoin(HUC_copy, dissolved, op='contains')     # Joining by location


#--------------------------- Here we write our final results ----------------------------#

HUC = gpd.read_file('FINAL_CONUS.shp')                        # Reading final result file
HUC['D (1/m)'] = joined_2.densities                           # Appending results to final
HUC.to_file('FINAL_CONUS_test.shp',
	 driver='ESRI Shapefile')                                 # writing final result file

#----------------------------------------------------------------------------------------#
#     >>>>>>>>>>>>>>>>>>>>>  TH-th-th-th-that's All Folks!  <<<<<<<<<<<<<<<<<<<<<<<      #
#----------------------------------------------------------------------------------------#
