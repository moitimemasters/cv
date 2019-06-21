from collections import deque
import numpy as np
import argparse
import imutils
import cv2
lastbox = [[], [], [], []]
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "yellow object"
# (or "ball") in the HSV color space, then initialize the
# list of tracked points
colorLower = (150, 70, 95)
colorUpper = (180, 255, 255)
cL = (105, 95, 95)
cU = (130, 255, 255)
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

# keep looping
(grabbed, frame) = camera.read()

# if we are viewing a video and we did not grab a frame,
# then we have reached the end of the video

# resize the frame, inverted ("vertical flip" w/ 180degrees),
# blur it, and convert it to the HSV color space

frame = cv2.flip(frame, 1)
#frame = cv2.GaussianBlur(frame, (15, 15), 0)
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# construct a mask for the color "green", then perform
# a series of dilations and erosions to remove any small
# blobs left in the mask
mask = cv2.inRange(hsv, colorLower, colorUpper)
mask = cv2.erode(mask, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)
mask1 = cv2.inRange(hsv, cL, cU)
mask1 = cv2.erode(mask1, None, iterations=2)
mask1 = cv2.dilate(mask1, None, iterations=2)
# find contours in the mask and initialize the current
# (x, y) center of the ball
cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)[-2]

cnts1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)[-2]
center = None

# only proceed if at least one contour was found
if len(cnts) > 0:
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid
    c = max(cnts, key=cv2.contourArea)
    rect = cv2.minAreaRect(c)
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    # only proceed if the radius meets a minimum size

        # draw the circle and centroid on the frame,
        # then update the list of tracked points
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    frame = cv2.drawContours(frame, [box], -1, (0, 255, 0), 3)
if len(cnts1) > 0:
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid
    c1 = max(cnts1, key=cv2.contourArea)
    rect1 = cv2.minAreaRect(c1)
    ((x1, y1), radius1) = cv2.minEnclosingCircle(c1)
    M1 = cv2.moments(c1)
    center1 = (int(M1["m10"] / M1["m00"]), int(M1["m01"] / M1["m00"]))

    # only proceed if the radius meets a minimum size

        # draw the circle and centroid on the frame,
        # then update the list of tracked points
    box1 = cv2.boxPoints(rect1)
    box1 = np.int0(box1)
    frame = cv2.drawContours(frame, [box1], -1, (0, 0, 255), 3)
lastbox = box1
setupbox = box1
f = True
f1 = True
# update the points queue
pts.appendleft(center)
score = 0
# loop over the set of tracked points
for i in range(1, len(pts)):
    # if either of the tracked points are None, ignore
    # them
    if pts[i - 1] is None or pts[i] is None:
        continue

    # otherwise, compute the thickness of the line and
    # draw the connecting lines
    thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)


    # show the frame to our screen
cv2.imshow("Frame", frame)
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # resize the frame, inverted ("vertical flip" w/ 180degrees),
    # blur it, and convert it to the HSV color space

    frame = cv2.flip(frame, 1)
    #frame = cv2.GaussianBlur(frame, (15, 15), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    mask1 = cv2.inRange(hsv, cL, cU)
    mask1 = cv2.erode(mask1, None, iterations=2)
    mask1 = cv2.dilate(mask1, None, iterations=2)
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]

    cnts1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        rect = cv2.minAreaRect(c)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size

            # draw the circle and centroid on the frame,
            # then update the list of tracked points
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        frame = cv2.drawContours(frame, [box], -1, (0, 255, 0), 3)
    if len(cnts1) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c1 = max(cnts1, key=cv2.contourArea)
        rect1 = cv2.minAreaRect(c1)
        ((x1, y1), radius1) = cv2.minEnclosingCircle(c1)
        M1 = cv2.moments(c1)
        center1 = (int(M1["m10"] / M1["m00"]), int(M1["m01"] / M1["m00"]))

        # only proceed if the radius meets a minimum size

            # draw the circle and centroid on the frame,
            # then update the list of tracked points
        box1 = cv2.boxPoints(rect1)
        box1 = np.int0(box1)
        f = True
        for i in range(4):
            for j in range(2):
                if abs(box1[i][j] - lastbox[i][j]) > 10:
                    f = False

                    break
        if f != f1:
            if not(f):
                score += 1
                print(score)
        f1 = f
        frame = cv2.drawContours(frame, [box1], -1, (0, 0, 255), 3)

    # update the points queue
    pts.appendleft(center)

    # loop over the set of tracked points
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)


    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
