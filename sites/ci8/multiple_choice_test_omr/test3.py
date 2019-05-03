"""
This code is partially derived from
https://www.pyimagesearch.com/2016/10/03/bubble-sheet-multiple-choice-scanner-and-test-grader-using-omr-python-and-opencv/
"""
import cv2
import numpy as np

colors = [
    (255,255,0),
    (255,0,0),
    (0,255,0),
    (0,255,255),
]

# Answers count
rows_count = 4
cols_count = 6

# The multiplier used for each row average value in order to define the threshold value
threshold_multiplier = 1.15

for base_name in [
    'test1-4a',
    'test1-4b',
    'test2-4',
    'test3-s',
    'test4',
    'test5',
]:
    # Open image
    img = cv2.imread('images/src/%s.jpg' % base_name)
    # Convert image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Convert image in black/white
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Save the black and white image
    cv2.imwrite('images/res/thresh_%s.png' % base_name, thresh)

    h, w = gray.shape

    # The size of the checkboxes
    bw = w / cols_count
    bh = h / rows_count

    results = np.zeros((rows_count, cols_count))

    # each question has 6 possible answers, to loop over the
    # question in batches of 6
    for j in range(rows_count):
        for i in range(cols_count):
            # construct a mask that reveals only the current
            # "bubble" for the question
            mask = np.zeros(thresh.shape, dtype="uint8")
            
            p1 = i * bw, j * bh
            p2 = i * bw + bw, j * bh + bh
            cv2.rectangle(mask, p1, p2, 255, -1)
     
            # apply the mask to the thresholded image, then
            # count the number of non-zero pixels in the
            # bubble area
            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            results[j][i] = cv2.countNonZero(mask)

            # Draw the bounding rectangle
            cv2.rectangle(img, p1, p2, colors[j], 2)

    for j in range(rows_count):
        threshold = results[j].mean() * threshold_multiplier
        for i in range(cols_count):
            total = results[j][i]

            if total >= threshold:
                p1 = i * bw, j * bh
                p2 = i * bw + bw, j * bh + bh

                # Draw the bounding rectangle in cyan
                cv2.rectangle(img, p1, p2, (0,0,255), 2)

    # Save the image with the bounding rectangles
    cv2.imwrite('images/res/res_%s.png' % base_name, img)
