##########################################################################################
#                                                                                        #
#    ----------------->  Morphological Approaches for Finding K  <------------------     #
#                                                                                        #                                      
##########################################################################################
                                                                                        
                                                                                      
#--------------------------- Here we read in useful libraries ---------------------------#

import geopandas as gpd
import numpy as np
import array


#------------------------------ Here we read in useful data -----------------------------#

# reading in the shapefile & grabbing the projection
shapefile = gpd.read_file('FINAL_CONUS.shp')
CRS = shapefile.crs

# pulling useful attributes
H = shapefile['H (m)']
d = shapefile['d (m)']
W = shapefile['W (m)']
D = shapefile['D (1/m)']
R = shapefile['R (m/s)']
S = shapefile['S (m/m)']


#-------------------------- This is where calculations are made -------------------------#

# Case 1: Luo method with drainage density
# Assumption No.1) H >= 100 
H_A1 = np.where(H<100, 100, H)
log_K_A1 = np.log10( R / ( D**2 * ( H_A1**2 - ( H_A1 - d)**2 ) ) ) 


# Case 2: Luo method with drainage density
# Assumption No.2) d <= H 
d_A2 = np.where(d>H, H, d)
log_K_A2 = np.log10( R / ( D**2 * ( H**2 - ( H - d_A2)**2 ) ) ) 


# Case 3: Luo method with drainage density
# Assumption No.3) H = 200 
H_A3 = np.where(H!=200, 200, H)
log_K_A3 = np.log10( R / ( D**2 * ( H_A3**2 - ( H_A3 - d)**2 ) ) ) 


# Case 4: Luo method with average effective flow length
# Assumption No.1) H >= 100 
log_K_A4 = np.log10( R / ( (1/2/W)**2 * ( H_A1**2 - ( H_A1 - d)**2 ) ) ) 


# Case 5: Luo method with average effective flow length
# Assumption No.2) d <= H 
log_K_A5 = np.log10( R / ( (1/2/W)**2 * ( H**2 - ( H - d_A2)**2 ) ) ) 


# Case 6: Luo method with average effective flow length
# Assumption No.3) H = 200 
log_K_A6 = np.log10( R / ( (1/2/W)**2 * ( H_A3**2 - ( H_A3 - d)**2 ) ) ) 

# Case 7: Luo method using slope as hydraulic gradient and not H - (H-d)
# We make use of average effective flow length and not drainage drainage density
log_K_A7 = np.log10(R*W/(S*H))

# Case 8: Luo method using slope as hydraulic gradient and not H - (H-d)
# We make use of drainage density and not flow length
log_K_A8 = np.log10(R/(D*S*H))

# Case 9: Luo method using slopes as hydraulic gradient to find transmissivity
# We make use of effective flow length and not drainage density
Log_T_A1 = np.log10(R*W/S)

# Case 10: Luo method using slopes as hydraulic gradient to find transmissivity
# We make use of drainage density and not effective flow length
Log_T_A2 = np.log10(R/(D*S))


#------------------------- Values are appended to dataframe here ------------------------#

shapefile['K case 1'] = log_K_A1

shapefile['K case 2'] = log_K_A2

shapefile['K case 3'] = log_K_A3

shapefile['K case 4'] = log_K_A4

shapefile['K case 5'] = log_K_A5

shapefile['K case 6'] = log_K_A6

shapefile['K case 7'] = log_K_A7

shapefile['K case 8'] = log_K_A8

shapefile['T case 1'] = Log_T_A1

shapefile['T case 2'] = Log_T_A2


#------------------------ Dataframe is written to shapefile here ------------------------#

# organizing columns
shapefile = shapefile[['README','ID','R (m/s)','H (m)','d (m)','S (m/m)',
	'D (1/m)','W (m)','K case 1','K case 2','K case 3','K case 4',
	'K case 5','K case 6','K case 7','K case 8','T case 1','T case 2',
	'geometry',]]

# writing results to file
geo_DF = gpd.GeoDataFrame(shapefile, geometry = 'geometry')
geo_DF.crs = CRS
geo_DF.to_file('FINAL_CONUS_test.shp',
	 driver='ESRI Shapefile')                              

#----------------------------------------------------------------------------------------#
#     >>>>>>>>>>>>>>>>>>>>>  TH-th-th-th-that's All Folks!  <<<<<<<<<<<<<<<<<<<<<<<      #
#----------------------------------------------------------------------------------------#

