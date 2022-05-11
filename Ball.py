import pygame
import random

class Ball:
    inhibate = 0
    points = 0
    run = True
    loose = False

    def __init__(self, width, height):
        self.speed = [5, 5]
        self.width = width
        self.height = height
        self.ballInit = pygame.image.load("intro_ball.gif")
        self.ball = pygame.image.load("intro_ball.gif")
        self.ballrect = self.ball.get_rect()
        self.angle = 0 

    def reload(self):
        """reload the game"""
        self.run = True
        self.loose = False
        self.points = 0
        self.ballrect.left = 0
        self.ballrect.top = 0
        self.angle = 0 
        self.speed = [5, 5]

    def accelerateX(self):
        self.speed = [self.speed[0] + 5, self.speed[1] + random.randrange(0,3)]

    def accelerateY(self):
        self.speed = [self.speed[0] + random.randrange(0,3), self.speed[1] + 5]

    def decelerate(self):
        if(self.speed[0] > 5):
            self.speed[0] = self.speed[0] - 1
        if(self.speed[1] > 5):
            self.speed[1] = self.speed[1] - 1

    def rotate(self):
        ballRotated = pygame.transform.rotate(self.ballInit, self.angle)
        self.ballrect = ballRotated.get_rect(center = self.ballInit.get_rect(center = self.ballrect.center).center)
        
        self.angle += 1
        self.ball = ballRotated

    def animate(self, faceRect):

        self.rotate()

        if(not self.run):
            return self.ball, self.ballrect, self.points, self.loose
        
        
        (l,t,w,h) = faceRect

        horTopLine = ((l,t), (l+h,t))
        verLeftLine = ((l,t), (l,t+w))
        verRightLine = ((l+h,t), (l+h,t+h))

        self.decelerate()
        if(self.inhibate >0):
            self.inhibate = self.inhibate-1
        self.ballrect = self.ballrect.move(self.speed)


        # Ball is not allowed to leave screen
        if self.ballrect.left < 0 : self.ballrect.left = -1
        if self.ballrect.right > self.width : self.ballrect.right = self.width + 1
        if self.ballrect.top < 0 : self.ballrect.top = -1
        if self.ballrect.bottom > self.height : self.ballrect.bottom = self.height + 1


        topCol = self.ballrect.clipline(horTopLine)
        leftCol = self.ballrect.clipline(verLeftLine)
        rightCol = self.ballrect.clipline(verRightLine)

        if topCol:
            self.accelerateY()

        if leftCol:
            self.accelerateX()

        if rightCol:
            self.accelerateX()

        if ((topCol or rightCol or leftCol)) and (self.inhibate == 0):
            self.points = self.points + 1

        
        if self.ballrect.bottom > self.height:
            self.loose = True

        # Change direction if touch screen sides or face
        if(self.inhibate == 0):
            if self.ballrect.left < 0 or self.ballrect.right > self.width or rightCol or leftCol:
                self.inhibate = 10
                self.speed[0] = -self.speed[0]
            if self.ballrect.top < 0 or self.ballrect.bottom > self.height or topCol:
                self.inhibate = 10
                self.speed[1] = -self.speed[1]

        return self.ball, self.ballrect, self.points, self.loose