##########################################################################################
#                                                                                        #
#        ----------------->  Machine Learning Interpolation  <-----------------          #
#                                                                                        #                                      
##########################################################################################
                                                                                        
                                                                                      
#--------------------------- Here we read in useful libraries ---------------------------#

import gdal
import numpy as np
import os, glob
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline


#----------------------------- Here we define our function ------------------------------#

def createTif(fname, res_arr, geom, prj, dtype=gdal.GDT_Float32, ndata=-99):
	driver = gdal.GetDriverByName('GTiff')
	dataset = driver.Create(
			fname,
			res_arr.shape[1],
			res_arr.shape[0],
			1,
			dtype,
			options = ['COMPRESS=LZW'])
	dataset.SetGeoTransform(geom)
	dataset.SetProjection(prj)
	dataset.GetRasterBand(1).WriteArray(res_arr)
	dataset.GetRasterBand(1).SetNoDataValue(ndata)
	dataset.FlushCache()


#----------------------------- Reading and processing data ------------------------------#

inf = np.inf                                              # Will be used in processing

# Reading in first training dataset
train_1= gdal.Open('final_PME_1km.tif').ReadAsArray()     # Used to train algorithm
ds=gdal.Open('final_PME_1km.tif')                         # Linearly related to K
train_1 = np.round(train_1,8)                             # Removing extra decimal places 
train_1 = np.nan_to_num(train_1)                          # Removing NaNs
train_1[train_1 == inf] = 0                               # Removing infinities
train_1[train_1 == -inf] = 0                              # Removing negative infinities

# reading second training dataset
train_2 = gdal.Open('CONUS_DEM_1km.tif').ReadAsArray()    # Used to train algorithm
train_2 = np.round(train_2,5)                             # Removing extra decimal places
train_2 = np.nan_to_num(train_2)                          # Removing NaNs
train_2[train_2 == inf] = 0                               # Removing infinities
train_2[train_2 == -inf] = 0                              # Removing negative infinities

# drainage density is only used to determine where interpolation should be done
train_3 = gdal.Open('drainage_density.tif').ReadAsArray() # Used in masking only
train_3 = np.round(train_3,8)                             # Removing extra decimal places
train_3 = np.nan_to_num(train_3)                          # Removing NaNs
train_3[train_3 == inf] = 0                               # Removing infinities
train_3[train_3 == -inf] = 0                              # Removing negative infinities


#--------------------------- Now we loop through interpolate ----------------------------#

for i in range(1,9):                                      # Looping through the cases
	
	# reading in file to be interpolated
	i = str(i)                                            # To be used in naming
	name = 'K_Case_'+i+'.tif'
	data = gdal.Open(name).ReadAsArray()                  # Dataset to be interpolated
	data = np.round(data,5)                               # Removing extra decimal places
	data = np.nan_to_num(data)                            # Removing NaNs
	data[data == inf] = 0                                 # Removing infinities
	data[data == -inf] = 0                                # Removing negative infinities
	data[data > 100] = 0                                  # reclassifying NoDatat  

	# creating mask; learning is done where data is available
	mask_data = np.logical_and(data != 0, train_1 > -99, train_3 > 0.0001)

	# analyzing the masked data
	big_X = np.hstack([train_2[mask_data].reshape(-1,1),
		train_1[mask_data].reshape(-1,1)]).astype(np.float32)
	big_Y = data[mask_data].astype(np.float32)

	# training the 2nd-order model and then interpolating erroneous or missing data
	order = 2
	model = make_pipeline(PolynomialFeatures(order), Ridge())
	model.fit(big_X,big_Y)
	loss_data = np.logical_and( train_3 < 0.0001, train_1 > -99)
	forecast_X = np.hstack([train_2[loss_data].reshape(-1,1),
		train_1[loss_data].reshape(-1,1)]).astype(np.float32)
	final_Y = model.predict(forecast_X)
	data_copy = data.copy()
	data_copy[loss_data]=final_Y
	createTif(name,data_copy,ds.GetGeoTransform(),
		ds.GetProjection())										


#----------------------------------------------------------------------------------------#
#     >>>>>>>>>>>>>>>>>>>>>  TH-th-th-th-that's All Folks!  <<<<<<<<<<<<<<<<<<<<<<<      #
#----------------------------------------------------------------------------------------#

