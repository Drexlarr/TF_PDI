import cv2
import numpy as np
import copy
import sys


def nothing(x):
    pass


def loadImages(url):
    notes_img = []
    img = cv2.imread(url)
    # img = cv2.resize(img, (680, 480), interpolation=cv2.INTER_LANCZOS4)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Black notes 0 - 6
    notes_img.append(cv2.imread("./images/templates/b1.png", 0))
    notes_img.append(cv2.imread("./images/templates/b2.png", 0))
    notes_img.append(cv2.imread("./images/templates/b3.png", 0))
    notes_img.append(cv2.imread("./images/templates/b4.png", 0))
    notes_img.append(cv2.imread("./images/templates/b5.png", 0))
    notes_img.append(cv2.imread("./images/templates/b6.png", 0))
    notes_img.append(cv2.imread("./images/templates/bla.png", 0))

    # Corcheas 7 - 8
    notes_img.append(cv2.imread("./images/templates/cor.png", 0))
    notes_img.append(cv2.cvtColor(cv2.imread(
        "./images/templates/cor1.png"), cv2.COLOR_BGR2GRAY))

    # Fa 9
    notes_img.append(cv2.imread("./images/templates/fa.png", 0))

    # Redondas 10 - 11
    notes_img.append(cv2.imread("./images/templates/r1.png", 0))
    notes_img.append(cv2.imread("./images/templates/r2.png", 0))

    # Sol 12
    notes_img.append(cv2.imread("./images/templates/sol.png", 0))

    # White notes 13 - 15
    notes_img.append(cv2.imread("./images/templates/w1.png", 0))
    notes_img.append(cv2.imread("./images/templates/w2.png", 0))
    notes_img.append(cv2.imread("./images/templates/whi.png", 0))

    return img, img_gray, notes_img


def eraseX2(list_template):
    if len(list_template) == 0:
        return []
    delete = []
    for i in range(np.size(list_template, 0)):
        for n in range(i + 1, np.size(list_template, 0)):
            a = abs(list_template[i][0] - list_template[n][0])
            b = abs(list_template[i][1] - list_template[n][1])
            if (a < 3) and (b < 3):
                delete.append(n)
    delete = np.unique(delete)
    if np.size(delete):
        res = np.delete(list_template, delete, 0)
    else:
        res = np.array(list_template)
    return res


def rePaint(img, list_template, note, color):
    w, h = note.shape[::-1]
    for i in range(len(list_template)):
        x, y = list_template[i]
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 1)


def getLinesScore(img, list_keySol, list_template, keySol):
    w, h = keySol.shape[::-1]
    print(w, h)
    firstLine = [15, 17]
    secondLine = [firstLine[0] + 8, firstLine[1] + 8]
    thirdLine = [secondLine[0] + 8, secondLine[1] + 8]
    fourthLine = [thirdLine[0] + 8, thirdLine[1] + 8]
    fifthLine = [fourthLine[0] + 8, fourthLine[1] + 8]

    for i in range(len(list_template)):
        x, y = list_template[i]
        for j in range(len(list_keySol)):
            xsol, ysol = list_keySol[j]
            if x == 327 and y == 307:
                if y >= fifthLine[0] + ysol + 4 and y <= fifthLine[0] + ysol + 8:
                    print(fifthLine[0] + ysol)

            if y <= ysol + h:
                # FA
                if y >= fourthLine[0] + ysol + 1 and y <= fifthLine[0] + ysol - 4:
                    cv2.putText(img, 'Fa', (x, y-fourthLine[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (124, 124, 0), 1, cv2.LINE_AA)
                # Mi
                elif (y >= fourthLine[0] + ysol + 4 and y <= fifthLine[0] + ysol) or (y >= firstLine[0] + ysol + 1 and y <= secondLine[0] + ysol - 4):
                    cv2.putText(img, 'Mi', (x, y-fourthLine[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 124, 0), 1, cv2.LINE_AA)
                # Sol
                elif y >= thirdLine[0] + ysol + 4 and y <= fourthLine[0] + ysol:
                    cv2.putText(img, 'Sol', (x, y-fourthLine[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 124, 0), 1, cv2.LINE_AA)
                # La
                if y >= thirdLine[0] + ysol + 1 and y <= fourthLine[0] + ysol - 4:
                    cv2.putText(img, 'La', (x, y-fourthLine[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (124, 0, 0), 1, cv2.LINE_AA)
                # Si
                elif y >= secondLine[0] + ysol + 4 and y <= thirdLine[0] + ysol:
                    cv2.putText(img, 'Si', (x, y-fourthLine[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 255, 0), 1, cv2.LINE_AA)
                # Do
                elif (y >= secondLine[0] + ysol + 1 and y <= thirdLine[0] + ysol - 4) or (y >= fifthLine[0] + ysol + 4 and y <= fifthLine[0] + ysol + 8):
                    cv2.putText(img, 'Do', (x, y-fourthLine[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 0, 0), 1, cv2.LINE_AA)
                # Re
                elif (y >= firstLine[0] + ysol + 4 and y <= secondLine[0] + ysol) or (y >= fifthLine[0] + ysol + 1 and y <= h + ysol - 4):
                    cv2.putText(img, 'Re', (x, y-fourthLine[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 0, 255), 1, cv2.LINE_AA)


def getNotes(img, img_gray, note, color, list_save, thr=0.69):
    w, h = note.shape[::-1]
    result = cv2.matchTemplate(img_gray, note, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= thr)
    for point in zip(*loc[::-1]):
        # cv2.rectangle(img, point, (point[0] + w, point[1] + h), color, 1)
        list_save.append([point[0], point[1]])


def resizeFromKey(img, img_gray):
    proob_img = copy.deepcopy(img)
    proob_img_gray = copy.deepcopy(img_gray)
    scale_w = cv2.getTrackbarPos("scale_width", "Trackbars")/100
    scale_h = cv2.getTrackbarPos("scale_height", "Trackbars")/100
    thr = cv2.getTrackbarPos('threshold', 'Trackbars')/100
    width = int(proob_img.shape[1] * scale_w)
    height = int(proob_img.shape[0] * scale_h)
    dsize = (width, height)
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
    cv2.imshow('Corcheas', notes[12])

    list_blackNotes = []
    list_blackNotesScore = []
    list_whiteNotes = []
    list_whiteNotesScore = []
    list_corcheaNotes = []
    list_keySol = []

    i = 0
    while True:
        if not i:
            proob_img, proob_img_gray, thr = resizeFromKey(smImg, smImg_gray)
            for n in range(len(notes)):
                if n == 12:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (0, 255, 0), list_keySol, thr)
                elif n == 13 or n == 14:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (0, 0, 255), list_whiteNotes, 0.51)
                elif n == 15:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (0, 0, 255), list_whiteNotesScore, 0.51)
                elif n < 6:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 0, 0), list_blackNotes, 0.70)
                elif n == 6:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 0, 0), list_blackNotesScore, 0.70)

                elif n == 7 or n == 8:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 255, 0), list_corcheaNotes, 0.55)
            if len(list_blackNotes) != 0:
                final_keySol = eraseX2(list_keySol)
                final_blackNotes = eraseX2(list_blackNotes)
                rePaint(proob_img, final_blackNotes, notes[0], (255, 0, 0))
                rePaint(proob_img, final_keySol, notes[12], (0, 255, 0))
                getLinesScore(proob_img, final_keySol,
                              final_blackNotes, notes[12])
            cv2.imshow('Calc size', proob_img)

            i += 1
        elif cv2.waitKey(0) & 0xFF == ord('t'):
            list_blackNotes = []
            list_blackNotesScore = []
            list_whiteNotes = []
            list_whiteNotesScore = []
            list_corcheaNotes = []
            list_keySol = []
            final_keySol = []
            proob_img, proob_img_gray, thr = resizeFromKey(smImg, smImg_gray)
            getNotes(proob_img, proob_img_gray,
                     notes[12], (0, 255, 0), list_keySol, thr)
            final_keySol = eraseX2(list_keySol)
            if type(final_keySol) is not list:
                rePaint(proob_img, final_keySol, notes[12], (0, 255, 0))
            cv2.imshow('Calc size', proob_img)

        elif cv2.waitKey(0) & 0xFF == ord('r'):
            proob_img, proob_img_gray, thr = resizeFromKey(smImg, smImg_gray)

            list_blackNotes = []
            list_blackNotesScore = []
            list_whiteNotes = []
            list_whiteNotesScore = []
            list_corcheaNotes = []
            list_keySol = []

            for n in range(len(notes)):
                if n == 12:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (0, 255, 0), list_keySol, thr)
                elif n == 13 or n == 14:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (0, 0, 255), list_whiteNotes, 0.51)
                elif n == 15:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (0, 0, 255), list_whiteNotesScore, 0.51)
                elif n < 6:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 0, 0), list_blackNotes, 0.70)
                elif n == 6:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 0, 0), list_blackNotesScore, 0.70)

                elif n == 7 or n == 8:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 255, 0), list_corcheaNotes, 0.55)
            if len(list_blackNotes) != 0:
                final_keySol = eraseX2(list_keySol)
                final_blackNotes = eraseX2(list_blackNotes)
                rePaint(proob_img, final_blackNotes, notes[0], (255, 0, 0))
                rePaint(proob_img, final_keySol, notes[12], (0, 255, 0))
                getLinesScore(proob_img, final_keySol,
                              final_blackNotes, notes[12])
            cv2.imshow('Calc size', proob_img)

        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
