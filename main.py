import cv2 as cv
import numpy as np
import isSet
from Card import Card
import pyzbar.pyzbar as pyzbar
import threading


def tts_set():
    # Does TTS
    pass


cam = cv.VideoCapture(0)
qrCodeDetector = cv.QRCodeDetector()

font = cv.FONT_HERSHEY_SIMPLEX

decodedCards = []

while True:
    ret, frame = cam.read()

    objs = pyzbar.decode(frame)

    for o in objs:
        print(o)

    decodedObjects = pyzbar.decode(frame)

    for decodedObject in decodedObjects:
        points = decodedObject.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4:
            hull = cv.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        # Number of points in the convex hull
        n = len(hull)
        # Draw the convext hull
        for j in range(0, n):
            cv.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

        x = decodedObject.rect.left
        y = decodedObject.rect.top

        print(x, y)

        print('Type : ', decodedObject.type)
        print('Data : ', decodedObject.data, '\n')
        if str(decodedObject.data.decode('utf-8')) not in decodedCards:
            decodedCards.append(str(decodedObject.data.decode('utf-8')))

        barCode = str(decodedObject.data)

        cv.putText(frame, barCode, (x, y), font, 1, (0, 255, 255), 2, cv.LINE_AA)

    cv.imshow("Preview", frame)

    if len(decodedCards) == 12:
        cards = []
        for i in decodedCards:
            attrs = i.split()
            card = Card(attrs[0], attrs[1], attrs[2], attrs[3])
            cards.append(card)

        print("Card objects:\n", cards)

        useSet = isSet.find_first_set(cards)
        if useSet:
            print("SET found:", useSet, "\n")
        else:
            print("No sets found with these cards")

        decodedCards = []

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv.destroyAllWindows()



