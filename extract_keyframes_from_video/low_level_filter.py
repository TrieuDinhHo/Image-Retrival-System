import numpy as np
import cv2
from skimage import feature

def filter_blurry(images,threshold_percent):
	var_list =[]
	for i,image in enumerate(images):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		fm = cv2.Laplacian(gray, cv2.CV_64F).var()
		var_list.append(fm)
	threshold = np.max(var_list)*(1-threshold_percent)
	return np.where(np.array(var_list) > threshold)[0]

def filter_histogram(images,color = None):
	hist_list = []
	if color =='gray':
		for image in images:
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
			hist_list.append(hist)
	elif color =='red':
		for image in images:
			red = image[:,:,0]
			hist = cv2.calcHist([red], [0], None, [256], [0, 256]).reshape(-1)
			hist_list.append(hist)
	elif color =='green':
		for image in images:
			green = image[:,:,1]
			hist = cv2.calcHist([green], [0], None, [256], [0, 256]).reshape(-1)
			hist_list.append(hist)
	elif color =='blue':
		for image in images:
			blue = image[:,:,2]
			hist = cv2.calcHist([blue], [0], None, [256], [0, 256]).reshape(-1)
			hist_list.append(hist)
	return hist_list # hist is a vector of 256 values


def histogram_color_red(image, shape):
	hist_r = np.array(filter_histogram(image,color = 'red'))
	hist_g = np.array(filter_histogram(image,color = 'green'))
	hist_b = np.array(filter_histogram(image,color = 'blue'))
	a = np.arange(256)/255
	hist = (2*hist_r-hist_g-hist_b)*a
	hist = hist/(shape[0]*shape[1])
	hist = np.where(hist<0,0,hist)
	
	return hist

def process_hog(image, orientations=9, pixels_per_cell=(11, 11), cells_per_block=(2, 2), transform_sqrt=True, block_norm="L1"):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (H, hogImage) = feature.hog(img, orientations=9, pixels_per_cell=(11, 11),
        cells_per_block=(2, 2), transform_sqrt=True, block_norm="L1",
        visualize=True)
    feature_vector = H.reshape(-1, 1656)
    return feature_vector
def process_hist(image):
	hist = histogram_color_red([image[105:125,:,:]], image[105:125,:,:].shape)
	return hist

def create_gaussian_window(size, sigma, mean):
	x = np.arange(size)
	gaussian_array = np.exp(-((x - mean) ** 2) / (2 * sigma ** 2))
	return gaussian_array