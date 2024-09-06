import os
import cv2
from tqdm import tqdm


# Function to resize images
def resize_images(input_dir, output_dir, size=(500, 500)):
    for folder in ["train", "valid"]:
        images_dir = os.path.join(input_dir, folder, "images")
        output_images_dir = os.path.join(output_dir, folder, "images")

        if not os.path.exists(output_images_dir):
            os.makedirs(output_images_dir)

        # Get a list of all image files for progress tracking
        image_files = [f for f in os.listdir(images_dir) if f.endswith(".jpg") or f.endswith(".png")]

        # Using tqdm to show progress
        for file in tqdm(image_files, desc=f"Resizing images in {folder}/images"):
            # Read the image
            img_path = os.path.join(images_dir, file)
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)

            # Resize the image
            img_resize = cv2.resize(img, size, cv2.INTER_LINEAR)
            resized_image_path = os.path.join(output_images_dir, file)
            cv2.imwrite(resized_image_path, img_resize)

    print(f"Resizing complete! Resized images saved in {output_dir}")


# Function to upsample images
def upsample_images(input_dir, output_dir, model_path="./models/EDSR_x4.pb", scale=4):
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model_path)
    sr.setModel("edsr", scale)

    for folder in ["train", "valid"]:
        images_dir = os.path.join(input_dir, folder, "images")
        output_images_dir = os.path.join(output_dir, folder, "images")

        if not os.path.exists(output_images_dir):
            os.makedirs(output_images_dir)

        # Get a list of all image files for progress tracking
        image_files = [f for f in os.listdir(images_dir) if f.endswith(".jpg") or f.endswith(".png")]

        # Using tqdm to show progress
        for file in tqdm(image_files, desc=f"Upsampling images in {folder}/images"):
            # Read the resized image
            img_path = os.path.join(images_dir, file)
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)

            # Upscale the image
            result_EDSR = sr.upsample(img)
            upscaled_image_path = os.path.join(output_images_dir, file)
            cv2.imwrite(upscaled_image_path, result_EDSR)

    print(f"Upsampling complete! Upscaled images saved in {output_dir}")


# Define input and output directories
input_directory = "./airplane-original-dataset"
rz_output_directory = "./resized-dataset"
upsample_output_directory = "./upsampled-dataset"

# Process images (resizing first, then upsampling from the same output directory)
resize_images(input_directory, rz_output_directory)
upsample_images(rz_output_directory, upsample_output_directory)
