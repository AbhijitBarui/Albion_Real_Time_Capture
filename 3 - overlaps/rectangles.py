import cv2 as cv
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def findclickpositions(needle_img, haystack_img, threshold=0.5, debug_mode=None):

    haystack_img = cv.imread(haystack_img, cv.IMREAD_UNCHANGED)
    needle_img = cv.imread(needle_img, cv.IMREAD_UNCHANGED)

    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]

    method = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(haystack_img, needle_img, method)

    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
        rectangles.append(rect)
        rectangles.append(rect)

    rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

    points = []
    if len(rectangles):
        print('found')
        
        line_color = (0,255,0)
        line_type = cv.LINE_4
        marker_color = (255,0,255)
        marker_type = cv.MARKER_CROSS

        for (x,y,w,h) in rectangles:

            center_x = x  + int(w/2)
            center_y = y  + int(h/2)
            points.append((center_x, center_y))

            if debug_mode == 'rectangles':
                top_left = (x,y)
                bottom_right = (x + w, y + h)
                cv.rectangle(haystack_img, 
                        top_left, 
                        bottom_right, 
                        line_color,
                        line_type)
            elif debug_mode == 'points':
                cv.drawMarker(haystack_img, (center_x,center_y), color=marker_color, markerType=marker_type)
        
        if debug_mode:
            cv.imshow('Result', haystack_img)
            cv.waitKey()
            # cv.imwrite('result.jpg', haystack_img)

    return points


# points = findclickpositions('cabbage.jpeg', 'farm.jpeg', debug_mode='points')
points = findclickpositions('turnip.jpeg', 'farm.jpeg', debug_mode='rectangles', threshold=0.67)
print(points)