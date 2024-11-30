import cv2 as cv
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

haystack_img = cv.imread('farm.jpeg', cv.IMREAD_UNCHANGED)
needle_img = cv.imread('cabbage.jpeg', cv.IMREAD_UNCHANGED)

# haystack_img = cv.cvtColor(haystack_img, cv.COLOR_BGR2GRAY)
# needle_img = cv.cvtColor(needle_img, cv.COLOR_BGR2GRAY)

result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)

# cv.imshow('Result', result)
# cv.waitKey()

min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
print(min_val, max_val, min_loc, max_loc)



threshold = 0.8
if max_val >= threshold:
    print('found')

    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]

    top_left = max_loc
    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

    cv.rectangle(haystack_img, 
                 top_left, 
                 bottom_right, 
                 color=(0,255,0), 
                 thickness=2, 
                 lineType=cv.LINE_4)
    
    # cv.imshow('Result', haystack_img)
    # cv.waitKey()
    cv.imwrite('result.jpg', haystack_img)

else:
    print('not found')
