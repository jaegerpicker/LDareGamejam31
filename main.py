import pygame
import math, sys, random
from pygame.locals import *

class Player:
    x = 0
    y = 0
    img = pygame.image.load('Player.png')
    up = 0
    down = 0

class Shot:
    x = 0
    y = 0
    img = pygame.image.load('PhaserShot.png')
    up = 0
    down = 0

class Enemy:
    x = 0
    y = 0
    img = pygame.image.load('Monster.png')
    up = 0
    down = 0


PLAYER_SPEED = 10


def main():
    #import pdb; pdb.set_trace()
    clock = pygame.time.Clock()
    FRAMES_PER_SECOND = 30
    deltat = clock.tick(FRAMES_PER_SECOND)
    screen = pygame.display.set_mode((1024,768), DOUBLEBUF)
    pygame.display.flip()
    sprites = {}
    sprites['enemies'] = []
    sprites['shots'] = []
    sprites['players'] = []
    player = Player()
    player.x = 0
    player.y = 0
    player.img = pygame.image.load('Player.png')
    player.up = 0
    player.down = 0
    sprites['players'].append(player)
    for i in range(5):
        e = Enemy()
        e.x = random.randrange(0,700)
        e.y = random.randrange(0,700)
        e.img = pygame.image.load('Monster.png')
        e.up = 0
        e.down = 0
        sprites['enemies'].append(e)
        #screen.blit(enemies[i], (i * 10, i*10))
    #print len(sprites['enemies'])
    screen.blit(player.img, (0,0))
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
                shot = Shot()
                shot.x = sprites['players'][0].x
                shot.y = sprites['players'][0].y
                shot.up = 0
                shot.down = 0
                shot.img = pygame.image.load('PhaserShot.png')
                sprites['shots'].append(shot)
            if event.key == K_UP:
                sprites['players'][0].y -= PLAYER_SPEED
            if event.key == K_DOWN:
                sprites['players'][0].y += PLAYER_SPEED
            if event.key == K_RIGHT:
                sprites['players'][0].x += PLAYER_SPEED
            if event.key == K_LEFT:
                sprites['players'][0].x -= PLAYER_SPEED
        screen.fill((0,0,0))
        for key, value in sprites.iteritems():
            #print key
            for s in value:
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

                screen.blit(s.img, (s.x, s.y))
        i = i + 1
        pygame.display.flip()
        if i == 10:
            i = 0




if __name__ == "__main__":
    main()
