import pygame
import math, sys, random
from pygame.locals import *

class BaseSprite(pygame.sprite.Sprite):
    up = 0
    down = 0
    def load_image(self, image_name):
        try:
            image = pygame.image.load(image_name)
        except pygame.error, message:
            print "Cannot load image: " + image_name
            raise SystemExit, message
        return image.convert_alpha()

    def draw(self):
        ''' Draw the sprite on the screen '''
        self.rect.left = self.x
        self.rect.top = self.y
        self.screen.blit(self.image, (self.rect.left, self.rect.top))

    def rectBox(self):
        self.rect = self.image.get_rect()
        self.image_w, self.image_h  = self.image.get_size()
        self.rect.move(self.x, self.y)
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

    def __init__(self, screen, x, y):
        self.screen  = screen
        self.x = x
        self.y = y
        self.rectBox()

class Player(BaseSprite):
    speed = 10

    def __init__(self, screen, x, y, image_name):
        self.image = self.load_image(image_name)
        super(self.__class__, self).__init__(screen, x, y)

class Shot(BaseSprite):
    speed = 25

    def __init__(self, screen, x, y, image_name):
        self.image = self.load_image(image_name)
        super(self.__class__, self).__init__(screen, x, y)

class Enemy(BaseSprite):
    speed = 5

    def __init__(self, screen, x, y, image_name):
        self.image = self.load_image(image_name)
        super(self.__class__, self).__init__(screen, x, y)


def game_over(screen, win):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 48)
    message = "GAME OVER"
    if win:
        message = "YOU WIN!"
    print message
    text1 = font.render(message, 1, (10, 10, 10))
    text1pos = text1.get_rect()
    text1pos.centerx = screen.get_rect().centerx
    text1pos.centery = screen.get_rect().centery
    screen.blit(text1, text1pos)
    font = pygame.font.Font(None, 36)
    text2 = font.render("Press Any Key to Continue", 1, (10, 10, 10))
    text2pos = text2.get_rect()
    text2pos.centerx = screen.get_rect().centerx
    text2pos.centery = screen.get_rect().centery + 50
    screen.blit(text2, text2pos)
    pygame.display.flip()


def main():
    #import pdb; pdb.set_trace()
    pygame.init()
    clock = pygame.time.Clock()
    FRAMES_PER_SECOND = 30
    deltat = clock.tick(FRAMES_PER_SECOND)
    screen = pygame.display.set_mode((1024,768), DOUBLEBUF)
    pygame.display.flip()
    sprites = {}
    sprites['enemies'] = []
    sprites['shots'] = []
    sprites['players'] = []
    player = Player(screen, 0, 0, 'Player.png')
    sprites['players'].append(player)
    for i in range(5):
        e = Enemy(screen, random.randrange(0,700), random.randrange(0,700), 'Monster.png')
        sprites['enemies'].append(e)
        #screen.blit(enemies[i], (i * 10, i*10))
    #print len(sprites['enemies'])
    pygame.display.flip()
    x = True
    i = 0
    while x:
        for event in pygame.event.get():
            if not hasattr(event, 'key'):
                continue
            if event.key == K_ESCAPE:
                sys.exit(0)
            if event.key == K_SPACE:
                shot = Shot(screen, sprites['players'][0].x + 50, sprites['players'][0].y + 25, 'PhaserShot.png')
                sprites['shots'].append(shot)
            if event.key == K_UP:
                sprites['players'][0].y -= sprites['players'][0].speed
            if event.key == K_DOWN:
                sprites['players'][0].y += sprites['players'][0].speed
            if event.key == K_RIGHT:
                sprites['players'][0].x += sprites['players'][0].speed
            if event.key == K_LEFT:
                sprites['players'][0].x -= sprites['players'][0].speed
        screen.fill((0,0,0))
        for key, value in sprites.iteritems():
            #print key
            j = 0
            for s in value:
                for ck, cv in sprites.iteritems():
                    for cs in cv:
                        if pygame.sprite.collide_rect(s, cs):
                            if s != cs:
                                del sprites[key][j]
                                if ck == 'players':
                                    game_over(screen, False)
                                    x = False
                                    break
                                if ck == 'enemies' and len(sprites[ck]) == 0:
                                    game_over(screen, True)
                                    x = True
                                    break
                if key != 'shots' and key != 'players':
                    if s.x > 700 or s.y > 700 or s.x < 0 or s.y < 0:
                        s.x = random.randrange(0,700)
                        s.y = random.randrange(0,700)
                    else:
                        s.x += i
                        s.y += i
                elif key == 'shots':
                    if s.x > 1024 or s.y > 768 or s.x < 0 or s.y < 0:
                        del sprites[key][0]
                    else:
                        s.x += 5
                j += 1
                s.draw()
        i = i + 1
        pygame.display.flip()
        if i == 10:
            i = 0
    pygame.event.wait()

if __name__ == "__main__":
    main()
