import cv2
import numpy as np
import copy
import sys


def nothing(x):
    pass


def loadImages(url):
    notes_img = []
    img = cv2.imread(url)
    #img = cv2.resize(img, (680, 480), interpolation=cv2.INTER_LANCZOS4)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    notes_img.append(cv2.imread("./images/templates/b1.png", 0))
    notes_img.append(cv2.imread("./images/templates/b2.png", 0))
    notes_img.append(cv2.imread("./images/templates/b3.png", 0))
    notes_img.append(cv2.imread("./images/templates/b4.png", 0))
    notes_img.append(cv2.imread("./images/templates/b5.png", 0))
    notes_img.append(cv2.imread("./images/templates/b6.png", 0))
    notes_img.append(cv2.imread("./images/templates/bla.png", 0))
    notes_img.append(cv2.imread("./images/templates/cor.png", 0))
    notes_img.append(cv2.cvtColor(cv2.imread(
        "./images/templates/cor1.png"), cv2.COLOR_BGR2GRAY))
    notes_img.append(cv2.imread("./images/templates/fa.png", 0))
    notes_img.append(cv2.imread("./images/templates/r1.png", 0))
    notes_img.append(cv2.imread("./images/templates/r2.png", 0))
    notes_img.append(cv2.imread("./images/templates/sol.png", 0))
    notes_img.append(cv2.imread("./images/templates/w1.png", 0))
    notes_img.append(cv2.imread("./images/templates/w2.png", 0))
    notes_img.append(cv2.imread("./images/templates/whi.png", 0))

    return img, img_gray, notes_img


def getNotes(img, img_gray, note, color, thr=0.69):
    w, h = note.shape[::-1]
    result = cv2.matchTemplate(img_gray, note, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= thr)
    for point in zip(*loc[::-1]):
        cv2.rectangle(img, point, (point[0] + w, point[1] + h), color, 1)


def resizeFromKey(img, img_gray):
    proob_img = copy.deepcopy(img)
    proob_img_gray = copy.deepcopy(img_gray)
    scale_w = cv2.getTrackbarPos("scale_width", "Trackbars")/100
    scale_h = cv2.getTrackbarPos("scale_height", "Trackbars")/100
    thr = cv2.getTrackbarPos('threshold', 'Trackbars')/100
    width = int(proob_img.shape[1] * scale_w)
    height = int(proob_img.shape[0] * scale_h)
    dsize = (width, height)
    print(thr)
    proob_img = cv2.resize(proob_img, dsize)
    proob_img_gray = cv2.resize(proob_img_gray, dsize)
    return proob_img, proob_img_gray, thr


if __name__ == "__main__":
    sheet_name = './resource/grupo4/Escaneado/' + sys.argv[1]
    smImg, smImg_gray, notes = loadImages(sheet_name)

    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("scale_width", "Trackbars", 38, 100, nothing)
    cv2.createTrackbar("scale_height", "Trackbars", 40, 100, nothing)
    cv2.createTrackbar("threshold", "Trackbars", 43, 100, nothing)
    cv2.imshow('Corcheas', notes[8])

    i = 0
    while True:
        if not i:
            proob_img, proob_img_gray, thr = resizeFromKey(smImg, smImg_gray)
            for n in range(len(notes)):
                if n == 12:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (0, 255, 0), thr)
                elif n >= 13:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (0, 0, 255), 0.51)
                elif n <= 6:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 0, 0), 0.70)
                elif n == 7 and n == 8:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 255, 0), 0.55)
            cv2.imshow('Calc size', proob_img)

            i += 1
        elif cv2.waitKey(0) & 0xFF == ord('r'):
            proob_img, proob_img_gray, thr = resizeFromKey(smImg, smImg_gray)
            for n in range(len(notes)):
                if n == 12:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (0, 255, 0), thr)
                elif n >= 13:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (0, 0, 255), 0.54)
                elif n <= 6:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 0, 0), 0.70)
                elif n == 7 and n == 8:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 255, 0), 0.55)
            cv2.imshow('Calc size', proob_img)

        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
