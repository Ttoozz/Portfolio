import math
from level import Level, elements
from os.path import split


import pygame
from pygame.fastevent import get_init


pygame.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

pygame.display.set_caption('YAA!')



class Player(pygame.sprite.Sprite):
    def __init__(self, level, timespeed):
        pygame.sprite.Sprite.__init__(self)
        self.collided_side = {"up":[False, -1], "down":[False, -1], "right":[False, -1], "left":[False, -1]}
        self.spritesheet = pygame.image.load('assets/satiro-Sheet v1.1.png').convert_alpha()
        self.pos = pygame.math.Vector2(0, 0)
        self.motion = pygame.math.Vector2(0, 0)
        #check the files then attribute these variable
        # save file -> then element
        self.element = elements['air']



        self.width, self.height = 50, 50
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.col_rect = pygame.Rect(self.pos[0]+10, self.pos[1]+2, self.width-10, self.height-4)
        self.img = self.get_image()
        self.mask = pygame.mask.Mask((self.rect.width, self.rect.height))#pygame.mask.from_surface(self.img)
        self.mask.fill()
        self.mask_img = pygame.mask.from_surface(self.img)
        self.mask_surf = self.mask.to_surface()
        self.Level = level
        self.timespeed = timespeed
        
        self.timers = {'on_ground':0, 'on_wall_right':0, 'on_wall_left':0, 'last_jump':0}

    def get_image(self):
        image = pygame.Surface((18, 19)).convert_alpha()
        image.blit(self.spritesheet, (0, 0), (5, 8, 18, 19))
        image = pygame.transform.scale(image, (self.width, self.height))
        image.set_colorkey((0, 0, 0))
        return image.convert_alpha()

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] and self.element.isLiquid:
            pass #self.motion.y -= self.element.acceleration
        elif keys[pygame.K_z]:
            pass #look down & attack down
        if keys[pygame.K_s] and self.element.isLiquid:
            pass #will be useful later on
        elif keys[pygame.K_z]:
            pass #look up & attack up
        if keys[pygame.K_q]:
            self.motion.x -= self.element.acceleration
        if keys[pygame.K_d]:
            self.motion.x += self.element.acceleration
        if keys[pygame.K_SPACE]:
            self.jump()

    def jump(self):
        if self.timers['on_ground'] >= pygame.time.get_ticks()-11-self.timespeed and self.timers['last_jump']+self.timespeed*5 <= pygame.time.get_ticks():
            self.motion.y -= 20
            self.timers['last_jump'] = pygame.time.get_ticks()

    def move(self):
        self.motion.x *= (1-self.element.friction)
        self.motion.y *= (1-self.element.friction)

        self.pos.x += self.motion.x
        self.pos.y += self.motion.y
        self.rect.x += self.motion.x
        self.rect.y += self.motion.y


    def raycast(self, origin, to_pos, step=2):

        dx = to_pos[0] - origin[0]
        dy = to_pos[1] - origin[1]
        distance = math.hypot(dx, dy)
        print(distance)


        if distance == 0:
            return "He is surely blocked lol"

        dx /= distance
        dy /= distance

        ix, iy = origin
        while not self.Level.get_mask().get_at((ix, iy)):
            ix, iy = ix + dx, iy + dy

        return (ix-dx, iy-dy)

    def collision(self):
        self.motion, self.rect, self.timers = self.Level.entity_collision(self.motion, self.rect, self.element,
                                                                          self.mask, self.timers)
    def update(self):
        self.input()
        self.collision()
        self.move()
        screen.blit(self.img, (self.rect.x, self.rect.y))
        #screen.blit(self.mask_surf, (self.rect.x, self.rect.y))






