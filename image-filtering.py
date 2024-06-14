import cv2
import numpy as np
from matplotlib import pyplot as plt

def apply_box_blur(image, ksize=100):
    return cv2.blur(image, (ksize, ksize))

def apply_bilateral_filter(image, d=9, sigmaColor=200, sigmaSpace=200):
    return cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)

def apply_sharpen_filter(image):
    sharpen_kernel = np.array([[-1, -1, -1], 
                               [-1,  9, -1],
                               [-1, -1, -1]])
    return cv2.filter2D(image, -1, sharpen_kernel)

def apply_gaussian_blur(image, ksize=10):
    return cv2.GaussianBlur(image, (ksize, ksize), 0)

def apply_median_filter(image, ksize=100):
    return cv2.medianBlur(image, ksize)

# Load a noisy image
noisy_image = cv2.imread('salt_and_pepper_noise.png')

# Apply filters
box_blur_image = apply_box_blur(noisy_image, ksize=5)
bilateral_filter_image = apply_bilateral_filter(noisy_image, d=9, sigmaColor=75, sigmaSpace=75)
sharpen_image = apply_sharpen_filter(noisy_image)
gaussian_blur_image = apply_gaussian_blur(noisy_image, ksize=5)
median_filter_image = apply_median_filter(noisy_image, ksize=5)

# Display the filtered images
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.ravel()

images = [noisy_image, box_blur_image, bilateral_filter_image, sharpen_image, gaussian_blur_image, median_filter_image]
titles = ['Noisy Image', 'Box Blur', 'Bilateral Filter', 'Sharpen Filter', 'Gaussian Blur', 'Median Filter']

for i in range(6):
    axes[i].imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))
    axes[i].set_title(titles[i])
    axes[i].axis('off')

plt.tight_layout()
plt.show()