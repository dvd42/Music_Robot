from imutils.object_detection import non_max_suppression
import numpy as np
import imutils
import cv2


# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def process_image(image):

    # boxes = 0
    # load the image and resize it to (1) reduce detection time
    # and (2) improve detection accuracy
    image = cv2.imread(image)
    image = imutils.resize(image, width=min(400, image.shape[1]))

    # detect people in the image
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
                                            padding=(8, 8), scale=1.05)

    # apply non-maxima suppression to the bounding boxes using a
    # fairly large overlap threshold to try to maintain overlapping
    # boxes that are still people
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    # draw the final bounding boxes
    #for (xA, yA, xB, yB) in pick:
    #    cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), )

    # show the output images
    #cv2.imshow("After NMS", image)
    #cv2.waitKey(0)
    return len(pick)

