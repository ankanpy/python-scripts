import cv2

# Initialize global variables
cropping = False
x_start, y_start, x_end, y_end = 0, 0, 0, 0
image = None

def click_and_crop(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping, image

    # if the left mouse button was clicked, record the starting (x, y) coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False

        # draw a rectangle around the region of interest
        cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
        cv2.imshow("image", image)

def main():
    global image
    # load the image, clone it, and setup the mouse callback function
    image = cv2.imread("/home/ankan_opencv/officework/VS_Code/python-scripts/DSC_1427.jpg")
    image = cv2.resize(image, (200,400))
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop)

    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            image = clone.copy()

        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            break

    # if there are two reference points, then crop the region of interest
    # from the image and display it
    if len({x_start, y_start, x_end, y_end}) == 4:
        roi = clone[y_start:y_end, x_start:x_end]
        cv2.imshow("ROI", roi)
        cv2.waitKey(0)

        # Save the cropped region
        cv2.imwrite("cropped_face.jpg", roi)

    # close all open windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
