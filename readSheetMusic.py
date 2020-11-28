import cv2
import numpy as np
import copy
import sys
import musicPlayer as mp


def nothing(x):
    pass


# Carga las imagenes
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
    notes_img.append(cv2.resize(cv2.imread(
        './images/templates/cor1.png', 0), (9, 21), interpolation=cv2.INTER_LANCZOS4))
    # notes_img.append(cv2.cvtColor(cv2.imread("./images/templates/cor1.png"), cv2.COLOR_BGR2GRAY))

    # Fa 9
    notes_img.append(cv2.imread("./images/templates/fa.png", 0))

    # Redondas 10 - 11

    notes_img.append(cv2.resize(cv2.imread(
        "./images/templates/r3.png", 0), (13, 9), interpolation=cv2.INTER_LANCZOS4))

    notes_img.append(cv2.resize(cv2.imread(
        "./images/templates/r4.png", 0), (13, 9), interpolation=cv2.INTER_LANCZOS4))

    # Sol 12
    notes_img.append(cv2.imread("./images/templates/sol.png", 0))

    # White notes 13 - 15
    notes_img.append(cv2.imread("./images/templates/w1.png", 0))
    notes_img.append(cv2.imread("./images/templates/w2.png", 0))
    notes_img.append(cv2.imread("./images/templates/whi.png", 0))

    # Compas 4/4
    # compas = [cv2.resize(cv2.imread('./images/templates/cuarto.png'),(13, 33), interpolation=cv2.INTER_LANCZOS4)]

    # Bemol = 16
    notes_img.append(cv2.resize(cv2.imread(
        './images/templates/be1.png', 0), (8, 11), interpolation=cv2.INTER_LANCZOS4))

    return img, img_gray, notes_img


# Elimina los match similares
def eraseX2(list_template, list_keySol, w_keySol, isKey=False):
    if len(list_template) == 0:
        return []
    if np.size(list_keySol, 0) > 1:
        xsol = list_keySol[1][0]
        xsol2 = list_keySol[0][0]
    else:
        xsol = list_keySol[0][0]
        xsol2 = list_keySol[0][0]
    delete = []
    for i in range(np.size(list_template, 0)):
        for n in range(i + 1, np.size(list_template, 0)):
            a = abs(list_template[i][0] - list_template[n][0])
            b = abs(list_template[i][1] - list_template[n][1])
            if (a < 3) and (b < 3) or (list_template[n][0] <= xsol + w_keySol and not isKey or list_template[n][0] <= (xsol2 - xsol) + (w_keySol*2) and not isKey) or (list_template[n][1] < list_keySol[0][1]):
                delete.append(n)
    delete = np.unique(delete)
    if np.size(delete):
        res = np.delete(list_template, delete, 0)
    else:
        res = np.array(list_template)
    return res


# Re pinta los match que quedaron del eraseX2
def rePaint(img, list_template, note, color):
    w, h = note.shape[::-1]
    for i in range(len(list_template)):
        x, y, z = list_template[i]
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 1)


# Obtiene el valor de la nota según la clave
def getLinesScore(img, list_keySol, list_template, keySol):
    w, h = keySol.shape[::-1]
    print(w, h)
    firstLine = [15, 17]
    secondLine = [firstLine[0] + 8, firstLine[1] + 8]
    thirdLine = [secondLine[0] + 8, secondLine[1] + 8]
    fourthLine = [thirdLine[0] + 8, thirdLine[1] + 8]
    fifthLine = [fourthLine[0] + 8, fourthLine[1] + 8]

    for i in range(len(list_template)):
        x, y, z = list_template[i]
        for j in range(len(list_keySol)):
            xsol, ysol, zsol = list_keySol[j]

            if y <= ysol + h and y >= ysol:
                # Re: 2-3
                if (y >= firstLine[0] + ysol + 4 and y <= secondLine[0] + ysol) or (y >= fifthLine[0] + ysol + 1 and y <= h + ysol - 12):
                    cv2.putText(img, 'Re', (x, y-fourthLine[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 0, 255), 1, cv2.LINE_AA)
                    if y <= secondLine[0] + ysol:
                        list_template[i][2] = 3
                    else:
                        list_template[i] = 2
                # Do: 0-1
                elif (y >= secondLine[0] + ysol and y <= thirdLine[0] + ysol - 4) or (y >= fifthLine[0] + ysol + 4 and y <= fifthLine[0] + ysol + 8):
                    cv2.putText(img, 'Do', (x, y-fourthLine[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 0, 0), 1, cv2.LINE_AA)
                    if y <= thirdLine[1] + ysol - 4:
                        list_template[i][2] = 1
                    else:
                        list_template[i][2] = 0
                # Si 12
                elif y >= secondLine[0] + ysol + 4 and y <= thirdLine[0] + ysol - 2:
                    cv2.putText(img, 'Si', (x, y-fourthLine[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 255, 0), 1, cv2.LINE_AA)
                    list_template[i][2] = 12
                # La 10-11
                if (y >= thirdLine[0] + ysol and y <= fourthLine[0] + ysol - 4) or (y >= firstLine[0] + ysol - 11 and y <= firstLine[0] + ysol - 8):
                    cv2.putText(img, 'La', (x, y-fourthLine[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (124, 0, 0), 1, cv2.LINE_AA)
                    if y <= firstLine[0] + ysol - 8:
                        list_template[i][2] = 11
                    else:
                        list_template[i][2] = 10
                # Sol 8-9
                elif (y >= thirdLine[0] + ysol + 4 and y <= fourthLine[0] + ysol) or (y >= firstLine[0] + ysol - 8 and y <= firstLine[0] + ysol - 5):
                    cv2.putText(img, 'Sol', (x, y-fourthLine[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 124, 0), 1, cv2.LINE_AA)
                    if y <= firstLine[0] + ysol - 5:
                        list_template[i][2] = 9
                    else:
                        list_template[i][2] = 8
                # Fa 6-7
                elif (y >= fourthLine[0] + ysol + 1 and y <= fifthLine[0] + ysol - 4) or (y >= firstLine[0] + ysol - 4 and y <= firstLine[0] + ysol - 2):
                    cv2.putText(img, 'Fa', (x, y-fourthLine[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (124, 124, 0), 1, cv2.LINE_AA)
                    if y <= firstLine[0] + ysol - 2:
                        list_template[i][2] = 7
                    else:
                        list_template[i][2] = 6
                # Mi: 4-5
                elif (y >= fourthLine[0] + ysol + 5 and y <= fifthLine[0] + ysol - 1) or (y >= firstLine[0] + ysol and y <= secondLine[0] + ysol - 5):
                    cv2.putText(img, 'Mi', (x, y-fourthLine[1]), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 124, 0), 1, cv2.LINE_AA)
                    if y <= secondLine[0] + ysol - 5:
                        list_template[i][2] = 5
                    else:
                        list_template[i][2] = 4


def sortNotes(list_keySol, list_template, keySol):
    w, h = keySol.shape[::-1]
    sort_notes = []
    for i in range(len(list_keySol)):
        xsol, ysol, zsol = list_keySol[i]
        aux = []
        for j in range(len(list_template)):
            x, y, z = list_template[j]
            if y <= h + ysol and y >= ysol:
                aux.append([x, y, z, 1])
        aux.sort(key=lambda x: x[0])
        if len(aux) != 0:
            sort_notes += aux
    return sort_notes


def group(blacks, whites, breves, list_keySol, keySol, list_cn, notes):
    w_bnote, h_bnote = notes[0].shape[::-1]
    w_wnote, h_wnote = notes[14].shape[::-1]
    w_cn, h_cn = notes[8].shape[::-1]
    w, h = keySol.shape[::-1]
    sort_notes = []
    aux_x = aux_y = 0
    for i in range(len(list_keySol)):
        xsol, ysol, zsol = list_keySol[i]
        if abs(xsol - aux_x) < 3 and abs(ysol - aux_y) < 3:
            continue
        aux_x = xsol
        aux_y = ysol
        aux = []
        for j in range(len(blacks)):
            x, y, z = blacks[j]
            if y <= h + ysol and y >= ysol:
                if z != -1:
                    aux.append([x, y, z, 1])
                    for q in range(len(list_cn)):
                        if (x + w_bnote > list_cn[q][0] and x < list_cn[q][0]) and y - 5 < list_cn[q][1] + h_cn:
                            aux[len(aux)-1][3] = 0.5

        for k in range(len(whites)):
            x, y, z = whites[k]
            if y <= h + ysol and y >= ysol:
                if z != -1:
                    aux.append([x, y, z, 2])
                    for q in range(len(list_cn)):
                        if (x + w_wnote > list_cn[q][0] and x < list_cn[q][0]) and y - 5 < list_cn[q][1] + h_cn:
                            aux[len(aux)-1][3] = 0.5
        for l in range(len(breves)):
            x, y, z = breves[l]
            if y <= h + ysol and y >= ysol:
                if z != -1:
                    aux.append([x, y, z, 4])

        aux.sort(key=lambda x: x[0])
        if len(aux) != 0:
            sort_notes += aux
    print(sort_notes)
    return sort_notes


# Encuentra todos los match
def getNotes(img, img_gray, note, color, list_save, thr=0.69):
    w, h = note.shape[::-1]
    result = cv2.matchTemplate(img_gray, note, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= thr)
    for point in zip(*loc[::-1]):
        # cv2.rectangle(img, point, (point[0] + w, point[1] + h), color, 1)
        list_save.append([point[0], point[1], -1])


# Redefine el tamaño de la imagen
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
    # sheet_name = sys.argv[1]
    smImg, smImg_gray, notes = loadImages(sheet_name)
    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("scale_width", "Trackbars", 38, 225, nothing)
    cv2.createTrackbar("scale_height", "Trackbars", 40, 225, nothing)
    cv2.createTrackbar("threshold", "Trackbars", 43, 100, nothing)
    cv2.imshow('Corcheas', notes[12])

    array_notas = []

    list_blackNotes = []
    list_blackNotesScore = []
    list_whiteNotes = []
    list_whiteNotesScore = []
    list_corcheaNotes = []
    list_semibreve = []
    list_keySol = []
    list_bemolNotes = []

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
                             notes[n], (0, 0, 255), list_whiteNotes, 0.55)
                elif n == 15:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (0, 0, 255), list_whiteNotesScore, 0.51)
                elif n < 6:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 0, 0), list_blackNotes, 0.70)
                elif n == 6:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 0, 0), list_blackNotesScore, 0.70)
                elif n == 8:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 255, 0), list_corcheaNotes, 0.65)
                elif n == 10 or n == 11:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 124, 255), list_semibreve, 0.70)
                elif n == 16:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (0, 124, 255), list_bemolNotes, 0.60)

            if len(list_blackNotes) != 0:
                # Limpieza
                final_keySol = eraseX2(
                    list_keySol, list_keySol, notes[12].shape[1], True)
                final_blackNotes = eraseX2(
                    list_blackNotes, final_keySol, notes[12].shape[1])
                final_whiteNotes = eraseX2(
                    list_whiteNotes, final_keySol, notes[12].shape[1])
                final_semibreves = eraseX2(
                    list_semibreve, final_keySol, notes[12].shape[1])
                final_corcheaNotes = eraseX2(
                    list_corcheaNotes, list_keySol, notes[12].shape[1])
                final_bemolNotes = eraseX2(
                    list_bemolNotes, list_keySol, notes[12].shape[1])

                # Repintamos el resultado
                rePaint(proob_img, final_whiteNotes, notes[13], (0, 0, 255))
                rePaint(proob_img, final_blackNotes, notes[0], (255, 0, 0))
                rePaint(proob_img, final_keySol, notes[12], (0, 255, 0))
                rePaint(proob_img, final_semibreves, notes[11], (0, 255, 124))
                rePaint(proob_img, final_corcheaNotes, notes[8], (0, 255, 255))
                rePaint(proob_img, final_bemolNotes,
                        notes[16], (124, 255, 255))

                getLinesScore(proob_img, final_keySol,
                              final_blackNotes, notes[12])
                getLinesScore(proob_img, final_keySol,
                              final_whiteNotes, notes[12])
                getLinesScore(proob_img, final_keySol,
                              final_semibreves, notes[12])

            cv2.imshow('Calc size', proob_img)

            i += 1
        elif cv2.waitKey(0) & 0xFF == ord('p'):
            final_notes = group(final_blackNotes, final_whiteNotes, final_semibreves,
                                list_keySol, notes[12], final_corcheaNotes, notes)
            mp.readNotes(final_notes)

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
            final_keySol = eraseX2(
                list_keySol, list_keySol, notes[12].shape[1], True)
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
                             notes[n], (0, 0, 255), list_whiteNotes, 0.55)
                elif n == 15:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (0, 0, 255), list_whiteNotesScore, 0.51)
                elif n < 6:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 0, 0), list_blackNotes, 0.70)
                elif n == 6:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 0, 0), list_blackNotesScore, 0.70)
                elif n == 8:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 255, 0), list_corcheaNotes, 0.65)
                elif n == 10 or n == 11:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (255, 124, 255), list_semibreve, 0.70)
                elif n == 16:
                    getNotes(proob_img, proob_img_gray,
                             notes[n], (0, 124, 255), list_bemolNotes, 0.60)

            if len(list_blackNotes) != 0:
                # Limpieza
                final_keySol = eraseX2(
                    list_keySol, list_keySol, notes[12].shape[1], True)
                final_blackNotes = eraseX2(
                    list_blackNotes, final_keySol, notes[12].shape[1])
                final_whiteNotes = eraseX2(
                    list_whiteNotes, final_keySol, notes[12].shape[1])
                final_semibreves = eraseX2(
                    list_semibreve, final_keySol, notes[12].shape[1])
                final_corcheaNotes = eraseX2(
                    list_corcheaNotes, list_keySol, notes[12].shape[1])
                final_bemolNotes = eraseX2(
                    list_bemolNotes, list_keySol, notes[12].shape[1])

                # Repintamos el resultado
                rePaint(proob_img, final_whiteNotes, notes[13], (0, 0, 255))
                rePaint(proob_img, final_blackNotes, notes[0], (255, 0, 0))
                rePaint(proob_img, final_keySol, notes[12], (0, 255, 0))
                rePaint(proob_img, final_semibreves, notes[11], (0, 255, 124))
                rePaint(proob_img, final_corcheaNotes, notes[8], (0, 255, 255))
                rePaint(proob_img, final_bemolNotes,
                        notes[16], (124, 255, 255))

                getLinesScore(proob_img, final_keySol,
                              final_blackNotes, notes[12])
                getLinesScore(proob_img, final_keySol,
                              final_whiteNotes, notes[12])
                getLinesScore(proob_img, final_keySol,
                              final_semibreves, notes[12])

                sortNotes(final_keySol, final_blackNotes, notes[12])
                sortNotes(final_keySol, final_whiteNotes, notes[12])
                sortNotes(final_keySol, final_semibreves, notes[12])
            cv2.imshow('Calc size', proob_img)

        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
