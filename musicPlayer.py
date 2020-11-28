import musicalbeeps

tempo = 100
player = musicalbeeps.Player(volume=0.4,
                             mute_output=False)

array_keySol_notes = ['C4', 'C5', 'D4', 'D5', 'E4',
                      'E5', 'F4', 'F5', 'G4', 'G5', 'A4', 'A5', 'B4']


def readNotes(array):
    for i in range(len(array)):
        note = array_keySol_notes[array[i][2]]
        tp_note = array[i][3]
        player.play_note(note, 60/tempo*tp_note)
