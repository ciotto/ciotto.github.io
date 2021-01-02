"""
This code is partially derived from
https://www.pyimagesearch.com/2016/10/03/bubble-sheet-multiple-choice-scanner-and-test-grader-using-omr-python-and-opencv/
"""
import cv2
import numpy as np
import math
import imutils
from imutils import contours

colors = [
    (255,255,0),
    (255,0,0),
    (0,255,0),
    (0,255,255),
]

# Answers columns count
cols_count = 6

# Checkbox size
min_w = 20
min_h = 20
min_ar = 0.7
max_ar = 1.3

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

    # find contours in the thresholded image, then initialize
    # the list of contours that correspond to questions
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questionCnts = []
     
    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour, then use the
        # bounding box to derive the aspect ratio
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
     
        # in order to label the contour as a question, region
        # should be sufficiently wide, sufficiently tall, and
        # have an aspect ratio approximately equal to 1
        if w >= min_w and h >= min_h and ar >= min_ar and ar <= max_ar:
            questionCnts.append(c)

    contours_len = len(questionCnts)
    cols_count = 6
    rows_count = int(math.ceil(contours_len / float(cols_count)))

    results = np.zeros((rows_count, cols_count))
    sorted_questionCnts = []

    print('Find %s contours' % contours_len)
    if questionCnts:
        # sort the question contours top-to-bottom, then initialize
        # the total number of correct answers
        questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]
        correct = 0

        # each question has 6 possible answers, to loop over the
        # question in batches of 6
        for (q, i) in enumerate(np.arange(0, len(questionCnts), cols_count)):
            # sort the contours for the current question from
            # left to right, then initialize the index of the
            # bubbled answer
            cnts = contours.sort_contours(questionCnts[i:i + cols_count])[0]
            sorted_questionCnts += cnts
            bubbled = None

            # loop over the sorted contours
            for (j, c) in enumerate(cnts):
                # construct a mask that reveals only the current
                # "bubble" for the question
                mask = np.zeros(thresh.shape, dtype="uint8")
                cv2.drawContours(mask, [c], -1, 255, -1)
         
                # apply the mask to the thresholded image, then
                # count the number of non-zero pixels in the
                # bubble area
                mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                results[q][j] = cv2.countNonZero(mask)

                # Get the bounding rectangle
                x, y, w, h = cv2.boundingRect(c)
                p1 = x, y
                p2 = x + w, y + h

                # Draw the bounding rectangle
                cv2.rectangle(img, p1, p2, colors[q], 2)

        for j in range(rows_count):
            threshold = results[j].mean() * threshold_multiplier
            for i in range(cols_count):
                total = results[j][i]

                if total >= threshold:
                    # Get the bounding rectangle
                    x, y, w, h = cv2.boundingRect(sorted_questionCnts[j * cols_count + i])
                    p1 = x, y
                    p2 = x + w, y + h

                    # Draw the bounding rectangle in cyan
                    cv2.rectangle(img, p1, p2, (0,0,255), 2)

    # Save the image with the bounding rectangles
    cv2.imwrite('images/res/res_%s.png' % base_name, img)
