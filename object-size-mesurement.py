import cv2
from object_detector import *
import numpy as np


# Load Aruco Detector
parameters0 = cv2.aruco.DetectorParameters()
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)


# Load Object Detector
detector = HomogeneousBgDetector()



# Load Cap3
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


while True:

    _, img = cap.read()
    
    # Get aruco Marker
    corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters0)
    if corners:

        # Draw Polygon around the marker
        int_corners = np.int0(corners)
        cv2.polylines(img, int_corners, True, (0 , 255, 0), 5)

        # Aruco Perimeter
        aruco_perimeter = cv2.arcLength(corners[0], True)

        # Pixel to cm ratio
        pixel_cm_ratio = aruco_perimeter / 20


        contours = detector.detect_objects(img)


        #Draw Objects Boundries
        for cnt in contours:

            # Get Rect
            rect = cv2.minAreaRect(cnt)
            (x,y), (w,h), angle = rect

            # Get width and height of the object by appling the ratio pixl to cm
            object_width = w / pixel_cm_ratio
            object_height = h / pixel_cm_ratio

            # Display Rectangle
            box = cv2.boxPoints(rect)
            box = np.int0(box)


            cv2.circle(img, (int(x) , int(y)), 5 ,(0 , 0 , 255), -1)
            cv2.polylines(img , [box], True , (255 , 0 , 0 ,4))
            cv2.putText(img, "Width {} cm".format(round(object_width , 1)), (int (x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100 ,200 , 0), 2)
            cv2.putText(img, "Height {} cm".format(round(object_height , 1)), (int (x - 100), int(y + 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100 ,200 , 0), 2)



    cv2.imshow("image :" ,img)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows