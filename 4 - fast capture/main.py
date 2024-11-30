import cv2 as cv
import numpy as np
from time import time
from windowcapture import WindowCapture

# Initialize the WindowCapture class
window_name = "Albion Online Client"  # Replace with the name of your target window
wincap = WindowCapture(window_name)

loop_time = time()
while True:
    # Get an updated image of the game
    screenshot = wincap.get_screenshot()

    # Display the screenshot
    cv.imshow('Computer Vision', screenshot)

    # Debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # Press 'q' to exit the loop
    if cv.waitKey(1) == ord('1'):
        cv.destroyAllWindows()
        break

print('Done.')