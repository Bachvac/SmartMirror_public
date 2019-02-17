from threading import Lock, Thread
import time
import threading

from imutils.video import VideoStream
from imutils import face_utils
import argparse #zbog parsiranja command line argumenata
import imutils
import time
import dlib
import cv2


from face_detection import FaceDetection

class Printer(Thread): #sluzi kao demo da vidimo sta se dogada u pozadini (s printanjem)
    #za dretve u ovom slucaju koristimo klase; napravimo klasu, njen konstruktor (koj nije obavezan)
    def __init__(self, value):
        Thread.__init__(self)
        self._value = value
        self.lock = Lock()

    def run(self):
        while True:
            with self.lock: #dvije stvari nemogu istovremeno vrtit taj blok koda
                print("PRINTER BLOCK")
                print("#" * 20)
                print("1) ", self._value)
                time.sleep(1)
                print("2) ", self._value)
                print("#" * 20)
            time.sleep(2)

    def face_update(self, has_face):
        with self.lock:
            self._value = has_face



def main(): #
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--shape-predictor", required=True, #ili p ili shape predictor se koriste u commandlineu, true jer je obavezno
        help="path to facial landmark predictor") #kad upisemo help u cl nam to ispise
    args = ap.parse_args()

    p = Printer(1)
    p.start()

    face = FaceDetection(args.shape_predictor, face_callbacks=[p.face_update])
    face.start()



    p.join() #mozda ne treba, ali bez ovoga glavna dretva zavrsi i umre, a ostale pokrenute (Printer i facedetection) nastave radit.
            #neke dretve (Daemon - pozadinski proces koj kad mu glavna dretva umre umre i on)
    face.join()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print("Me die now.")



