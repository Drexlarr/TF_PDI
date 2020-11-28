import cv2
import numpy as np


def nothing(x):
    pass


def initializeTrackbars(intialTracbarVals=0):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Threshold1", "Trackbars", 200, 255, nothing)
    cv2.createTrackbar("Threshold2", "Trackbars", 200, 255, nothing)


def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 5000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest, max_area


def reorder(myPoints):

    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    return myPointsNew


width = 1920
height = 1080

thres1 = 200.0
thres2 = 200
while True:
    # Segmentación
    image = cv2.imread("./resource/grupo1/5/20201115_143243.jpg")
    # Redimensionamos la imagen
    image = cv2.resize(image, (width, height),
                       interpolation=cv2.INTER_LANCZOS4)
    # Cambiamos a escala de grises
    imagegray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Aplicamos un filtro Gaussiano paar eliminar el ruido
    imagegaussian = cv2.GaussianBlur(imagegray, (5, 5), 1)
    # Obtenemos 2 threshold
    #thres = valTrackbars()
    # Aplicamos el filtro Canny para detectar los bordes
    imgThreshold = cv2.Canny(imagegaussian, thres1, thres2)
    #imgThreshold = cv2.Canny(imagegaussian, thres[0], thres[1])

    # Aplicaremos morofología matemática, primero dilatación y luego erosión
    kernel = np.ones((5, 5))

    dil = cv2.dilate(imgThreshold, kernel, iterations=2)
    imgThreshold = cv2.erode(dil, kernel, iterations=2)


# Descriptor de bordes Freeman
    imgContours = image.copy()
    imgBig = image.copy()
    contours, hier = cv2.findContours(
        imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)

# Hallar el mayor contorno
    biggest, max_area = biggestContour(contours)
    while(biggest.size == 0):
        thres1 -= 1
        if thres1 == 30:
            break

    print(biggest)
    if biggest.size != 0:
        biggest = reorder(biggest)
        print(biggest)
        cv2.drawContours(imgBig, biggest, -1, (0, 255, 0), 20)


# A partir de los puntos obtenidos, obtener la matriz de perspectiva para encontrar la imagen sin transformación
        pts1 = np.float32(biggest)
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored = cv2.warpPerspective(image, matrix, (width, height))

        imgWarpColored = imgWarpColored[20:imgWarpColored.shape[0] -
                                        20, 20:imgWarpColored.shape[1] - 20]
        imgWarpColored = cv2.resize(imgWarpColored, (width, height))

        imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
        imgWarpGray = cv2.GaussianBlur(imgWarpGray, (5, 5), 0)
        f1, f = cv2.threshold(imgWarpGray, 0, 255,
                              cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        break
cv2.imwrite("./titanic.jpg", f)

cv2.imshow("image2",  f)
cv2.waitKey(0)
cv2.destroyAllWindows()

