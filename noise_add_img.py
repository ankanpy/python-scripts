import numpy as np
import cv2
from skimage import io, util

# Load an image using OpenCV
# Replace 'path_to_your_image.jpg' with the actual path of your image
image_path = 'dog.jpg'
image = cv2.imread(image_path)

# Ensure the image is loaded
if image is None:
    raise ValueError("Image not found or the path is incorrect")

# Convert image to float32 for noise addition, skimage expects images in [0, 1]
image_float = np.float32(image) / 255.0

# Add Gaussian noise
# You can adjust the 'var' parameter to change the noise intensity
gaussian_noise_img = util.random_noise(image_float, mode='gaussian', var=0.20)

# Add salt-and-pepper noise
# You can adjust the 'amount' parameter to change the noise intensity
salt_pepper_noise_img = util.random_noise(image_float, mode='s&p', amount=0.20)

# Convert the noisy images back to uint8
gaussian_noise_img_uint8 = np.uint8(gaussian_noise_img * 255)
salt_pepper_noise_img_uint8 = np.uint8(salt_pepper_noise_img * 255)

# Save or display the noisy images
x = cv2.imwrite('image_with_gaussian_noise.jpg', gaussian_noise_img_uint8)
y = cv2.imwrite('image_with_salt_and_pepper_noise.jpg', salt_pepper_noise_img_uint8)

# Note: You can use cv2.imshow('Title', image) to display the images if running this script locally
cv2.imshow('Gaussian', x)
cv2.imshow('salt&paper', y)