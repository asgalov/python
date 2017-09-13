import scipy.misc as mi
import numpy as np
from scipy.misc.pilutil import Image
import scipy.ndimage as nd
from skimage import filters
from skimage import feature
import matplotlib.pyplot as plt
from skimage.morphology import watershed
#from skimage.filter.thresholding import threshold_otsu


a = Image.open('resize.jpg').convert('L')
a = mi.fromimage(a)

thresh = filters.threshold_otsu(a)
im_otsu = a > thresh
im_otsu = mi.toimage(im_otsu)
im_otsu.save('otsu_semoutput.png')

im_canny = feature.canny(a, sigma=3)
fill_holes = nd.binary_fill_holes(im_canny)
fill_holes = mi.toimage(fill_holes)
im_canny = mi.toimage(im_canny)
im_canny.save('test_canny.jpg')

#to remove bushes try to adopt canny edges for leaves, fill holes and then negate obtained mask
fill_holes.save('fill_holes.jpg')

im_laplace = nd.gaussian_laplace(a, 3)
im_laplace = mi.toimage(im_laplace)
im_laplace.save('test_laplace.jpg')

im_elevation_map = filters.sobel(a)
markers = np.zeros_like(a)
markers[a < 30] = 1
markers[a > 150] = 2
segmentation = watershed(im_elevation_map, markers)
im_sobel = mi.toimage(segmentation)
im_sobel.save('im_sobel.jpg')
