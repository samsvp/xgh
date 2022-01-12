#%%
import cv2
import numpy as np
import matplotlib.pyplot as plt

def gabor(x, y, lmbda, theta, psi, sigma, gamma) -> np.ndarray:
    xline = x * np.cos(theta) + x * np.sin(theta)
    yline = -y * np.sin(theta) + y * np.cos(theta)

def create_gaborfilter():
    # This function is designed to produce a set of GaborFilters 
    # an even distribution of theta values equally distributed amongst pi rad / 180 degree
     
    filters = []
    num_filters = 32
    ksize = 5  # The local area to evaluate
    sigma = 20.0  # Larger Values produce more edges
    lambd = 10.0
    gamma = 0.5
    psi = 0  # Offset value - lower generates cleaner results
    for theta in np.arange(0, np.pi, np.pi / num_filters):  # Theta is the orientation for edge detection
        kern = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_64F)
        kern /= 1.0 * kern.sum()  # Brightness normalization
        filters.append(kern)
    return filters

def apply_filter(img, filters):
# This general function is designed to apply filters to our image
     
    # First create a numpy array the same size as our input image
    newimage = np.zeros_like(img)
     
    # Starting with a blank image, we loop through the images and apply our Gabor Filter
    # On each iteration, we take the highest value (super impose), until we have the max value across all filters
    # The final image is returned
    depth = -1 # remain depth same as original image
     
    for kern in filters:  # Loop through the kernels in our GaborFilter
        image_filter = cv2.filter2D(img, depth, kern)  #Apply filter to image
         
        # Using Numpy.maximum to compare our filter and cumulative image, taking the higher value (max)
        np.maximum(newimage, image_filter, newimage)
    return newimage

img = cv2.imread("van_gogh.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

ksize = (3, 3)
sigma = 10
lmbda = 30
theta = 1/np.sqrt(2)
gamma = 0.25
psi = 0
# We create our gabor filters, and then apply them to our image
gfilters = create_gaborfilter()
image_g = apply_filter(img, gfilters)
plt.imshow(image_g)
plt.show()
plt.imshow(img)
plt.show()

min_interval = 120
max_interval = 250
image_edge_g = cv2.Canny(image_g,min_interval,max_interval)
 
# Using Numpy's function to append the two images horizontally
image_edge = cv2.Canny(img,min_interval,max_interval)
side_by_side = np.hstack((image_edge,image_edge_g))
plt.imshow(side_by_side)

# filters = create_gaborfilter()

# for f in filters:
#     img = cv2.filter2D(img, -1, f)

# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# plt.imshow(img)
# %%
