from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import pygame
from pygame.locals import *

pygame.font.init()
f = True
count = 0

# отрисовка поля
pygame.init()  # инициализация pygame
win = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
s1 = [win, (0, 255, 0), ((1920 - 720), (1080 - 270)), 180]
e1 = [win, (0, 255, 0), (300, 530, 320, 280)]
e2 = [win, (0, 255, 0), (1380, 530, 320, 240)]
e3 = [win, (255, 111, 0), (890, 780, 320, 240)]
t1 = [win, (0, 0, 0), [[0, 0], [321, 0], [0, 321]]]
t2 = [win, (0, 0, 0), [[19250, 0], [1920, 321], [1599, 0]]]
myfont = pygame.font.SysFont('Comic Sans MS', 100)
clock = pygame.time.Clock()
color = 0
x, y = 0, 0
a = 1
lastbox = [[], [], [], []]

# construct the argument parse and parse the arguments
# штука для запуска команд из консоли(не особо нужна)
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "yellow object"
# (or "ball") in the HSV color space, then initialize the
# list of tracked points
colorLower = (103, 120, 95)
colorUpper = (138, 255, 255)
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


# if we are viewing a video and we did not grab a frame,
# then we have reached the end of the video

# resize the frame, inverted ("vertical flip" w/ 180degrees),
# blur it, and convert it to the HSV color space


while True:
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                break
    # отрисовка поля
    win.fill((255, 255, 255))
    pygame.draw.ellipse(*e1)
    pygame.draw.ellipse(*e2)
    pygame.draw.ellipse(*e3)
    pygame.draw.polygon(*t1)
    pygame.draw.polygon(*t2)

    # корявая отрисовка шарика на поле
    if y <= 240:
        pygame.draw.circle(win, (0, 0, 0), (int(x) * 3, int(y * 4.3) - 300), 80)
    else:
        pygame.draw.circle(win, (0, 0, 0), (int(x) * 3, int(y * 4.3)), 80)
    # самая хреновая коллизия века
    if ((300 <= int(x * 3) <= 620) and (530 <= int(y * 4.3) <= 810)) or (
            (1380 <= int(x * 3) <= 1700) and (530 <= int(y * 4.3) <= 770)):
        count += 1
    elif (890 <= int(x * 3) <= 1210) and (780 <= int(y * 4.3) <= 1020):
        count -= 5
        # отрисовка очков(работает супер коряво)
    textsurface = myfont.render('Current count:' + str(int(count)), False, (255, 0, 0))
    textsurface = pygame.transform.rotate(textsurface, 180)
    win.blit(textsurface, (666, 555))
    pygame.display.flip()
    clock.tick(60)
    # grab the current frame(получение текущего кадра)
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # resize the frame, inverted ("vertical flip" w/ 180degrees),
    # blur it, and convert it to the HSV color space
    frame = imutils.resize(frame, width=640)
    # обрезка изображения по маске
    maskforframe = cv2.imread('mask1.png', 0)
    frame = cv2.bitwise_and(frame, frame, mask=maskforframe)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    # распознование цвета
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    mask1 = cv2.inRange(hsv, cL, cU)
    mask1 = cv2.erode(mask1, None, iterations=2)
    mask1 = cv2.dilate(mask1, None, iterations=2)
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    # поиск контуров после распознования цвета
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]

    cnts1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,
                             cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    # получение координат шарика и его радиуса
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
        # отрисовка рамки вокруг шарика
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        frame = cv2.drawContours(frame, [box], -1, (0, 255, 0), 3)
        # тоже самое для другого цвета(бесполезно)
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
        # frame = cv2.drawContours(frame, [box1], -1, (0, 0, 255), 3)

    # update the points queue
    # бесполезная штука, которая раньше рисовала траекторию
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

    # show the frame(кадр) to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    # if the 'q' key is pressed, stop the loop

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
pygame.quit()