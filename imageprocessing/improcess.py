import scipy.misc as mi
import numpy as np
from scipy.misc.pilutil import Image
import scipy.ndimage as nd
from skimage import filters
from skimage import feature
import matplotlib.pyplot as plt


a = Image.open('resize.jpg').convert('L')
a = mi.fromimage(a)
im_canny = feature.canny(a, sigma=3)
im_canny = mi.toimage(im_canny)
im_canny.save('test_canny.jpg')

im_laplace = nd.gaussian_laplace(a, 3)
im_laplace = mi.toimage(im_laplace)
im_laplace.save('test_laplace.jpg')

