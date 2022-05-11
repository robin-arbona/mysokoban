import pygame
import random

class Ball:
    inhibate = 0
    points = 0
    run = True
    loose = False

    def __init__(self, width, height):
        self.speed = [ random.randrange(-5,5) , random.randrange(-5,5) ]
        self.width = width
        self.height = height
        self.ballInit = pygame.image.load("lib/intro_ball.gif")
        self.ball = pygame.image.load("lib/intro_ball.gif")
        self.ballrect = self.ball.get_rect()
        self.ballrect.left = random.randrange(0,self.width - 50)
        self.angle = 0 
        self.acc = 10

    def reload(self):
        """reload the game"""
        self.run = True
        self.loose = False
        self.points = 0
        self.ballrect.left = random.randrange(0,self.width - 50)
        self.ballrect.top = 0
        self.angle = 0 
        self.speed = [ random.randrange(-5,5) , random.randrange(-5,5) ]

    def accelerateX(self):
        if(self.speed[0] > 0):
            self.speed = [self.speed[0] + self.acc, self.speed[1] + random.randrange(-3,3)]
        else:
            self.speed = [self.speed[0] - self.acc, self.speed[1] + random.randrange(-3,3)]

    def accelerateY(self):
        if(self.speed[1] > 0):
            self.speed = [self.speed[0] + random.randrange(-3,3), self.speed[1] + self.acc]
        else:
            self.speed = [self.speed[0] + random.randrange(-3,3), self.speed[1] - self.acc]


    def decelerate(self):
        if(self.speed[0] > self.acc):
            self.speed[0] = self.speed[0] - 1
        if(self.speed[1] > self.acc):
            self.speed[1] = self.speed[1] - 1
        if(self.speed[1] < self.acc):
            self.speed[1] = self.speed[1] + 1

    def rotate(self):
        ballRotated = pygame.transform.rotate(self.ballInit, self.angle)
        self.ballrect = ballRotated.get_rect(center = self.ballInit.get_rect(center = self.ballrect.center).center)
        
        self.angle += 5
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


        # Collision whith faces sides defintion
        topCol = self.ballrect.clipline(horTopLine)
        leftCol = self.ballrect.clipline(verLeftLine)
        rightCol = self.ballrect.clipline(verRightLine)

        # Accelare move when touch top or left / right faces rectangle sides
        if topCol:
            self.accelerateY()

        if leftCol:
            self.accelerateX()

        if rightCol:
            self.accelerateX()

        if ((topCol or rightCol or leftCol)) and (self.inhibate == 0):
            self.points = self.points + 1

        # Loose if touch screen bottom        
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