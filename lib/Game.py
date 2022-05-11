import sys, pygame
from lib.Ball import Ball
from lib.Cam import Cam

class Game:
    loose = False

    def __init__(self,width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.cam = Cam(width, height)
        self.ball = Ball(width, height)


    def actionsHandeler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:           
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.ball.reload()

    def getFaceRectFromCam(self):
        l = self.width-self.cam.width-self.cam.left
        t = self.cam.top
        w = self.cam.heigh
        h = self.cam.width

        return (l,t,w,h)

    def writeText(self,text):
        font = pygame.font.SysFont(None, 50)
        img = font.render(text, True, (255,0,0))
        return img


    def run(self):
        
        while 1:
            self.screen.fill((0,0,0))

            faceRect = (l,t,w,h) = self.getFaceRectFromCam()

                
            ball, ballRect, self.points, self.loose =  self.ball.animate(faceRect)

            camPic, pos = self.cam.getSurfaceCam()

            self.actionsHandeler()

            self.screen.blit(camPic, pos)

            # Handle failure
            if(self.loose):
                self.screen.blit(self.writeText('!!! Looser !!!'), (200,150))
                self.ball.run = False

            # display ball
            self.screen.blit(ball, ballRect)
                
            # display score
            self.screen.blit(self.writeText(str(self.points)), (25,25))


            # display face rectangle for debuging
            pygame.draw.rect(self.screen, (255,0,0), faceRect, 1)
            pygame.draw.rect(self.screen, (255,255,0), ballRect, 1)


            pygame.display.flip()



