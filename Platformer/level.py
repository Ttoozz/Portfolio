import pygame, json, math



class Element:
    def __init__(self, gravity, friction, acceleration, liquid):
        self.gravity = gravity
        self.friction = friction
        self.acceleration = acceleration
        self.isLiquid = liquid

class Level:
    def __init__(self, path):
        self.img = pygame.image.load(path).convert_alpha()
        self.col_mask = pygame.mask.from_surface(self.img)
        self.mask_img = self.col_mask.to_surface()
        self.offset = [0., 0.]

    def entity_collision(self, motion, rect, element, mask:pygame.Mask, timers=False, offset=(0,0)):

        """
        angle = math.atan2(self.motion.y, self.motion.x)
        angle = math.degrees(angle)
        print(angle)
        dist = round(math.sqrt(self.motion.x**2 + self.motion.y**2), 2)

        #self.raycast(angle, dist, (self.rect.left, self.rect.bottom))
        """
        motion.y += element.gravity
        friction = element.friction



        if offset != (0, 0) and mask != 0:
            overlap = self.col_mask.overlap(mask, offset)
        else:
            overlap = self.get_mask().overlap_mask(mask, (round(rect.x + (motion.x * (1 - friction))), round(rect.y + (motion.y * (1 - friction)))))

        collided_side = {"up": [False, -1], "down": [False, -1], "right": [False, -1], "left": [False, -1]}

        if overlap.count():
            collided_rects = overlap.get_bounding_rects()

            for col_rect in collided_rects:
                if col_rect.x == (rect.x + round(motion.x * (1 - friction))):
                    collided_side["left"] = [True, collided_rects.index(col_rect)]
                if col_rect.right == (rect.right + round(motion.x * (1 - friction))):
                    collided_side["right"] = [True, collided_rects.index(col_rect)]
                if col_rect.bottom == (rect.bottom + round(motion.y * (1 - friction))):
                    collided_side["down"] = [True, collided_rects.index(col_rect)]
                if col_rect.top == (rect.top + round(motion.y * (1 - friction))):
                    collided_side["up"] = [True, collided_rects.index(col_rect)]
                print(collided_side)
                print(rect.bottom, motion)
                print((rect.bottom + round(motion.y * (1 - friction))))
            old_motion_x = motion.x

            if collided_side["left"][0] and collided_side["right"][0] and collided_side["down"][0] and \
                    collided_side["up"][0]:
                # will need to do ray cast for these 2numbers
                motion.x = 0
                motion.y = 0
                timers['on_ground'] = pygame.time.get_ticks()

            else:
                if collided_side["up"][0]:
                    if collided_side['left'][0] and collided_side['right'][0]:
                        if collided_rects[collided_side["left"][1]].width < collided_rects[
                            collided_side["left"][1]].height:
                            rect.x = collided_rects[collided_side["left"][1]].right
                            motion.x = 0
                            collided_side["up"][0] = False

                        elif motion.y < 0:

                            rect.y = collided_rects[collided_side["up"][1]].bottom
                            motion.y = 0

                        else:
                            motion.y = 0

                    elif collided_side["left"][0]:
                        if collided_rects[collided_side["left"][1]].width < 10:
                            rect.x = collided_rects[collided_side["left"][1]].right
                            motion.x = 0
                            collided_side["up"][0] = False
                        else:
                            rect.y = collided_rects[collided_side["up"][1]].bottom
                            motion.y = 0
                            collided_side["up"][0] = False

                    elif collided_side["right"][0]:
                        if collided_rects[collided_side["left"][1]].width < 10:
                            rect.right = collided_rects[collided_side["right"][1]].left
                            motion.x = 0
                            collided_side["up"][0] = False
                        else:
                            rect.y = collided_rects[collided_side["up"][1]].bottom
                            motion.y = 0
                            collided_side["up"][0] = False

                elif collided_side["down"][0]:
                    if collided_side["right"][0] or collided_side["left"][0]:

                        if collided_rects[collided_side["down"][1]].width + 10 > collided_rects[
                            collided_side["down"][1]].height:

                            rect.bottom = collided_rects[collided_side["down"][1]].top
                            motion.y = 0
                            collided_side["down"][0] = False
                            if timers:
                                timers['on_ground'] = pygame.time.get_ticks()

                        elif collided_side["right"][0]:
                            rect.right = collided_rects[collided_side["right"][1]].left
                            motion.x = 0
                            collided_side["down"][0] = False

                        elif collided_side["left"][0]:
                            rect.left = collided_rects[collided_side["left"][1]].right
                            motion.x = 0
                            collided_side["down"][0] = False

                elif collided_side["left"][0]:
                    rect.x = collided_rects[collided_side["left"][1]].right
                    motion.x = 0
                elif collided_side["right"][0]:
                    rect.right = collided_rects[collided_side["right"][1]].left
                    motion.x = 0


                elif collided_side["left"][0] and collided_side["right"][0] and collided_side["down"][0]:
                    motion.y = 0
                    motion.x = old_motion_x
                    rect.bottom = collided_rects[collided_side["down"][1]].top
                    if timers:
                        timers['on_ground'] = pygame.time.get_ticks()


        return motion, rect, timers



    def draw_mask(self, screen):
        screen.blit(self.mask_img, (0,0))

    def get_mask(self):
        return self.col_mask

    def draw(self, screen):
        screen.blit(self.img, (0,0))

    def update(self, screen):
        self.draw(screen)

elements = {}
data = json.load(open("Element/elements.json"))
for i in data:
    elements[i] = Element(data[i]['gravity'], data[i]['friction'], data[i]['acceleration'], data[i]['liquid'])


