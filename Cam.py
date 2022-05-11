import pygame
import pygame.camera
from pygame.locals import *
import cv2

class Cam:

    left = 0
    top = 0
    width = 0
    heigh = 0

    def __init__(self, width, height):
        camera = cv2.VideoCapture(0)
        camera.set(3,640)
        camera.set(4,480)
        self.camera = camera
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


    def action(self, event):
        if event.type in (pygame.QUIT, pygame.KEYDOWN):           
                self.camera.release()


    def getSurfaceCam(self):
        # img = self.cam.get_image()
        retval,frame = self.camera.read()

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw the rectangle around each face

        for (x, y, w, h) in faces:
            self.left = x
            self.top = y
            self.width = w
            self.heigh = h

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame = pygame.surfarray.make_surface(frame)

        return frame, (0,0)




