##########################################################################################
#                                                                                        #
#    -------------->  Mostly scratch code for consolidating data    <---------------     #
#                                                                                        #                                      
##########################################################################################


#--------------------------- Here we read in useful lybraries ---------------------------#

import geopandas as gpd
from shapely.geometry import Polygon
import array


#----------------------------- Here we read in our datasets -----------------------------#

# HUC_Shape = gpd.read_file('JS_HUCs_RHEld.shp')         # Use driver to open shapefile
# FINAL_CONUS = HUC_Shape.geometry
# FINAL_CONUS.to_file('FINAL_CONUS.shp',
# 	 driver='ESRI Shapefile')                              # Here we write our shapefile
# Valley_Shape = gpd.read_file('HUC_Valley_Depth.shp') 
# HUC_Shape = gpd.read_file('JS_HUCs_RHEld.shp')
FINAL_CONUS = gpd.read_file('FINAL_CONUS_test.shp')


#------------------ This was used to create a readme  column in FINAL_CONUS.shp----------#

# readme = FINAL_CONUS['README']
# 
# with open('readme.txt','w') as f:
# 	for item in readme:
# 		f.write('%s\n' % item)
		
# new_readme = [line.rstrip('\n') for line in open('readme.txt')]
# 
# FINAL_CONUS['README'] = new_readme


#------------------ This was used to organize columns in FINAL_CONUS.shp ----------------#

# id = FINAL_CONUS['id']
# R = FINAL_CONUS['R (m/s)']
# H = FINAL_CONUS['H (m)']
# d = FINAL_CONUS['d (m)']
# W = FINAL_CONUS['W (m)']
# D = FINAL_CONUS['D (1/m)']
# 
# del FINAL_CONUS['README']
# del FINAL_CONUS['id']
# del FINAL_CONUS['R (m/s)']
# del FINAL_CONUS['H (m)']
# del FINAL_CONUS['d (m)']
# del FINAL_CONUS['W (m)']
# del FINAL_CONUS['D (1/m)']
# del FINAL_CONUS['density (1']
# del FINAL_CONUS['density _1']

del FINAL_CONUS['K case 7']
del FINAL_CONUS['K case 8']
del FINAL_CONUS['T case 1']
del FINAL_CONUS['T case 2']

# 
# FINAL_CONUS['README'] = readme
# FINAL_CONUS['ID'] = id
# FINAL_CONUS['R (m/s)'] = R
# FINAL_CONUS['H (m)'] = H
# FINAL_CONUS['d (m)'] = d
# FINAL_CONUS['W (m)'] = W
# FINAL_CONUS['D (1/m)'] = D


#--------------------------- Here we write out our dataset ------------------------------#

FINAL_CONUS.to_file('FINAL_CONUS_test.shp',
	 driver='ESRI Shapefile')                              # Here we write our shapefile

#print(Valley_Shape.columns.values)

#----------------------------------------------------------------------------------------#
#     >>>>>>>>>>>>>>>>>>>>>  TH-th-th-th-that's All Folks!  <<<<<<<<<<<<<<<<<<<<<<<      #
#----------------------------------------------------------------------------------------#


