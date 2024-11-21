#Create your own shooter

from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


font.init()
font2 = font.SysFont('Arial',36)
win = font2.render('YOU WIN!',True,(255,255,255))
lose = font2.render('YOU LOSE!',True,(180,0,0))

back = 'galaxy.jpg'
rocket = 'rocket.png'
ufo = 'ufo.png'
bullet_png = 'bullet.png'
asteroid = 'asteroid.png'

skor = 0
lost = 0
goal = 20
max_lost = 10
life = 3


class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
 
        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        #every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet(bullet_png,self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height :
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(back), (win_width, win_height))

player = Player(rocket, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(ufo, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    ast = Enemy(asteroid, randint(30, win_width - 30), -40, 80, 50, randint(1, 3))
    asteroids.add(ast)

bullets = sprite.Group()

game = True
finish = False
real_time = False
num_fire = 0

while game :
    for e in event.get():
        if e.type == QUIT:
            game = False
        
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and real_time == False :
                    num_fire += 1
                    fire_sound.play()
                    player.fire()
                if num_fire >= 5 and real_time == False :
                    rec = timer()
                    real_time = True
                # game = True

    if finish != True:
        window.blit(background,(0,0))

        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        collides = sprite.groupcollide(monsters,bullets,True,True)
        for i in collides:
            skor += 1
            monster = Enemy(ufo, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            
        if sprite.spritecollide(player,monsters,False) or sprite.spritecollide(player,asteroids,False):
            sprite.spritecollide(player,monsters,True)
            sprite.spritecollide(player,asteroids,True)
            life -= 1
        if lost >= max_lost or life == 0 :
            finish = True
            window.blit(lose,(200,200))

        if skor >= goal:
            finish = True
            window.blit(win,(200,200))

        skor1 = font2.render('Skor:' + str(skor), 1, (255,255,255))
        window.blit(skor1,(10, 20))
        lost1 = font2.render('Lost:' + str(lost), 1, (255,255,255))
        window.blit(lost1,(10, 50))
            
        if life == 3:
            life_color = (0,255,0)
        if life == 2:
            life_color = (255,255,0)
        if life == 1:
            life_color = (255,0,0)

        life_text = font2.render(str(life), 1, life_color)
        window.blit(life_text,(650,10))

        display.update()
time.delay(50)
