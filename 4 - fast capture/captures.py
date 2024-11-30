import cv2 as cv
import numpy as np
import os
import pyautogui

os.chdir(os.path.dirname(os.path.abspath(__file__)))

while(True):
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

    cv.imshow('Computer Vision', screenshot)

    # 'q' to break out of the loop and close the window
    if cv.waitKey(1) & 0xFF == ord('q'):  
        cv.destroyAllWindows()
        break

print('Done.')