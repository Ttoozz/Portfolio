import random
from tkiteasy import *
from PIL import Image, ImageTk



#normally we will resize everything there and set the TILE_SIZE but nah no time
Image.open('heart.png').resize((30, 30)).save('heart_ig.png')




W, H = 1050, 1050
WIN = ouvrirFenetre(W, H)
TILE_SIZE = 40

blocking_tiles = ['M', 'C', 'E', 'F', 'P']
indestructible = ['C']
destructible = ['M']
hit_tiles = ['F', 'P']
enemies = []
spawners = []

HP = 3
levels = {1:True, 2:False, 3:False}

class Player():
    def __init__(self, x, y, hp, img='char.png'):
        self.x = x
        self.y = y
        self.img_file = img
        self.hp = hp
        self.image = WIN.afficherImage(x, y, img)
        self.bombs = []
        self.level = 0
        self.range = 1

    def commande(self):
        touche = WIN.recupererTouche()
        if touche:
            touche = touche.upper()
            if touche == 'Z':
                self.touche_Z()
            elif touche == 'Q':
                self.touche_Q()
            elif touche == 'S':
                self.touche_S()
            elif touche == 'D':
                self.touche_D()
            elif touche == 'SPACE':
                self.touche_Espace()
            elif touche == 'X':
                self.touche_X()
            return True

    def touche_Z(self):
        if map[self.y//TILE_SIZE-1][self.x//TILE_SIZE] not in blocking_tiles:
            if map[self.y//TILE_SIZE-1][self.x//TILE_SIZE] == 'U':
                self.levelup()
                WIN.supprimer(map_graphique[self.y // TILE_SIZE-1][self.x // TILE_SIZE])
                map_graphique[self.y // TILE_SIZE+1][self.x // TILE_SIZE] = WIN.dessinerRectangle(self.x,self.y-TILE_SIZE,TILE_SIZE,TILE_SIZE, 'green')
            map[self.y//TILE_SIZE][self.x//TILE_SIZE] = ' '
            map[self.y // TILE_SIZE-1][(self.x // TILE_SIZE)] = 'P'
            WIN.supprimer(self.image)
            self.y -= TILE_SIZE
            self.image = WIN.afficherImage(self.x ,self.y, self.img_file)

    def touche_Q(self):
        if map[self.y//TILE_SIZE][self.x//TILE_SIZE-1] not in blocking_tiles:
            if map[self.y//TILE_SIZE][self.x//TILE_SIZE-1] == 'U':
                self.levelup()
                WIN.supprimer(map_graphique[self.y//TILE_SIZE][self.x//TILE_SIZE-1])
                map_graphique[self.y//TILE_SIZE][self.x//TILE_SIZE-1] = WIN.dessinerRectangle(self.x- TILE_SIZE, self.y, TILE_SIZE, TILE_SIZE, 'green')
            map[self.y//TILE_SIZE][self.x//TILE_SIZE] = ' '
            map[self.y // TILE_SIZE][(self.x // TILE_SIZE)-1] = 'P'
            WIN.supprimer(self.image)
            self.x -= TILE_SIZE
            self.image = WIN.afficherImage(self.x ,self.y, self.img_file)

    def touche_S(self):
        if map[self.y//TILE_SIZE+1][self.x//TILE_SIZE] not in blocking_tiles:
            if map[self.y//TILE_SIZE+1][self.x//TILE_SIZE] == 'U':
                self.levelup()
                WIN.supprimer(map_graphique[self.y // TILE_SIZE+1][self.x // TILE_SIZE])
                map_graphique[self.y // TILE_SIZE+1][self.x // TILE_SIZE] = WIN.dessinerRectangle(self.x,self.y+ TILE_SIZE,TILE_SIZE,TILE_SIZE, 'green')
            map[self.y//TILE_SIZE][self.x//TILE_SIZE] = ' '
            map[self.y // TILE_SIZE+1][(self.x // TILE_SIZE)] = 'P'
            WIN.supprimer(self.image)
            self.y += TILE_SIZE
            self.image = WIN.afficherImage(self.x ,self.y, self.img_file)

    def touche_D(self):
        if map[self.y//TILE_SIZE][self.x//TILE_SIZE+1] not in blocking_tiles:
            if map[self.y//TILE_SIZE][self.x//TILE_SIZE+1] == 'U':
                self.levelup()
                WIN.supprimer(map_graphique[self.y//TILE_SIZE][self.x//TILE_SIZE+1])
                map_graphique[self.y//TILE_SIZE][self.x//TILE_SIZE-1] = WIN.dessinerRectangle(self.x+ TILE_SIZE, self.y , TILE_SIZE, TILE_SIZE, 'green')
            map[self.y//TILE_SIZE][self.x//TILE_SIZE] = ' '
            map[self.y // TILE_SIZE][(self.x // TILE_SIZE)+1] = 'P'
            WIN.supprimer(self.image)
            self.x += TILE_SIZE
            self.image = WIN.afficherImage(self.x ,self.y, self.img_file)

    def touche_Espace(self):
        self.bombs.append(Bomb(self.x, self.y, self, range=self.range))

    def touche_X(self):
        pass

    def levelup(self):
        self.level += 1
        if self.level%2 == 1:
            self.hp += 1
        elif self.level%2 == 0:
            self.range += 1



    def on_top(self):
        WIN.supprimer(self.image)
        self.image = WIN.afficherImage(self.x ,self.y, self.img_file)
    def delete(self):
        WIN.supprimer(self.image)
        for i in self.bombs:
            i.explode()
            i.delete()

    def hitted(self, dmg=1):
        self.hp -= dmg
        if self.hp <= 0:
            menus['in_game'] = False
            menus['end_screen'] = True

    def update(self):
        if self.commande():
            for i in self.bombs:
                i.tick()
            return True

class Bomb():
    def __init__(self, x, y, owner, img='bomb.png', Ntimer=4, range=2):
        self.x = x
        self.y = y
        self.timer = Ntimer
        self.range = range
        self.img_file = img
        self.owner = owner
        self.img =  WIN.afficherImage(self.x, self.y, img)

    def tick(self):
        if self.timer == -1:
            self.delete()
        elif self.timer == 0:
            self.explode()
        else:
            if self.owner.x == self.x and self.owner.y == self.y:
                self.owner.on_top()
            self.timer -= 1


    def explode(self):
        self.timer -= 1

        self.hitted_tiles = [(self.x, self.y)]

        self.hitted_tiles += self.explosion_rec(self.range, (1,0), (self.x, self.y))
        self.hitted_tiles += self.explosion_rec(self.range, (-1, 0), (self.x, self.y))
        self.hitted_tiles += self.explosion_rec(self.range, (0, 1), (self.x, self.y))
        self.hitted_tiles += self.explosion_rec(self.range, (0, -1), (self.x, self.y))
        WIN.supprimer(self.img)

        for i in range(len(self.hitted_tiles)):
            for j in enemies + [self.owner]:
                if j.x == self.hitted_tiles[i][0] and j.y == self.hitted_tiles[i][1]:
                    j.hitted()
            if map[self.hitted_tiles[i][1]//TILE_SIZE][self.hitted_tiles[i][0]//TILE_SIZE] in destructible:
                map[self.hitted_tiles[i][1] // TILE_SIZE][self.hitted_tiles[i][0] // TILE_SIZE] = ' '
                WIN.supprimer(map_graphique[self.hitted_tiles[i][1] // TILE_SIZE][self.hitted_tiles[i][0] // TILE_SIZE])
                map_graphique[self.hitted_tiles[i][1] // TILE_SIZE][
                    self.hitted_tiles[i][0] // TILE_SIZE] = WIN.dessinerRectangle(self.hitted_tiles[i][0],
                                                                                  self.hitted_tiles[i][1], TILE_SIZE,
                                                                                  TILE_SIZE, 'green')
                game_options['score'] += 20
            self.hitted_tiles[i] = WIN.afficherImage(self.hitted_tiles[i][0], self.hitted_tiles[i][1], 'explosion.png')

    def explosion_rec(self, radius, direction, pos):
        if map[pos[1]//40+direction[1]][pos[0]//40+direction[0]] not in indestructible and radius > 0:
            return [(pos[0]+40*direction[0], pos[1]+40*direction[1])] + self.explosion_rec(radius-1, direction, (pos[0] + TILE_SIZE*direction[0], pos[1] + TILE_SIZE*direction[1]))
        return []

    def delete(self):
        for i in self.hitted_tiles:
            WIN.supprimer(i)
        self.owner.bombs.pop(self.owner.bombs.index(self))
        del self.hitted_tiles



class Enemy:
    def __init__(self, x, y, hp=1, img='Enemy1.png'):
        self.x = x
        self.y = y
        self.hp = hp
        self.img = img
        self.old_pos = []
        self.image = WIN.afficherImage(self.x, self.y, img)
        self.dont_move = 0
    def move(self):
        if self.hp <= 0:
            WIN.supprimer(self.image)
        if self.dont_move == 0:
            pos_movable = []
            if map[int(self.y//TILE_SIZE)-1][int(self.x//TILE_SIZE)] not in blocking_tiles:
                pos_movable.append((self.y//TILE_SIZE-1, self.x//TILE_SIZE))
            if map[int(self.y // TILE_SIZE) + 1][int(self.x // TILE_SIZE)] not in blocking_tiles:
                pos_movable.append((self.y // TILE_SIZE+1, self.x // TILE_SIZE))
            if map[int(self.y // TILE_SIZE)][int(self.x // TILE_SIZE) -1] not in blocking_tiles:
                pos_movable.append((self.y // TILE_SIZE, self.x // TILE_SIZE -1 ))
            if map[int(self.y // TILE_SIZE)][int(self.x // TILE_SIZE) + 1] not in blocking_tiles:
                pos_movable.append((self.y // TILE_SIZE, self.x // TILE_SIZE + 1))

            if pos_movable == [self.old_pos]:
                pass
            elif self.old_pos in pos_movable:
                pos_movable.remove(self.old_pos)
            if len(pos_movable) == 0:
                return

            new_pos = random.choice(pos_movable)

            WIN.supprimer(self.image)
            self.old_pos = (self.y//TILE_SIZE, self.x//TILE_SIZE)
            map[self.old_pos[0]][self.old_pos[1]] = ' '
            map[new_pos[0]][new_pos[1]] = 'F'

            self.x = new_pos[1]*TILE_SIZE
            self.y = new_pos[0]*TILE_SIZE
            self.image = WIN.afficherImage(self.x, self.y, self.img)
        else:
            self.dont_move -= 1

    def hit(self):
        if map[int(self.y//TILE_SIZE)-1][int(self.x//TILE_SIZE)] == 'P':
            P.hitted()
            self.dont_move += 1
        if map[int(self.y // TILE_SIZE)+1][int(self.x // TILE_SIZE)] == 'P':
            P.hitted()
            self.dont_move += 1
        if map[int(self.y // TILE_SIZE)][int(self.x // TILE_SIZE) -1] == 'P':
            P.hitted()
            self.dont_move += 1
        if map[int(self.y // TILE_SIZE)][int(self.x // TILE_SIZE) + 1] == 'P':
            P.hitted()
            self.dont_move += 1

    def hitted(self):
        self.hp -= 1
        game_options['score'] += 20
        if self.hp <= 0:
            WIN.supprimer(self.image)
            enemies.pop(enemies.index(self))
            game_options['score'] += 50
            map[self.y//TILE_SIZE][self.x//TILE_SIZE] = 'U'
            map_graphique[self.y//TILE_SIZE][self.x//TILE_SIZE] = WIN.afficherImage(self.x, self.y, 'upgrade.png')

    def kill(self):
        WIN.supprimer(self.image)
        enemies.pop(enemies.index(self))
        game_options['score'] += 50
        map[self.y // TILE_SIZE][self.x // TILE_SIZE] = 'U'
        map_graphique[self.y // TILE_SIZE][self.x // TILE_SIZE] = WIN.afficherImage(self.x, self.y, 'upgrade.png')

    def update(self):
        self.move()
        self.hit()




def init_map(file):
    texte = open(file, 'r')
    brouillon = texte.readlines()
    map  = []
    for ligne in brouillon:
        map.append(list(ligne))
    map = map[3:]
    return map


def setup_game(file='map0.txt'):
    f = open(file, 'r').readlines()
    map = f[3:]
    timer = int(f[0].split()[1])
    global TIMER_ENEMY
    TIMER_ENEMY = int(f[1].split()[1])
    global enemies
    enemies = []
    global game_options
    game_options = {'hp': HP, 'score': 0, 'enemy_hp': 1, 'timer': timer, 'timer_enemy': TIMER_ENEMY}


    map = init_map(file)
    map_graphique = []
    for i in range(len(map)):
        map_graphique.append([])

    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 'M':
                map_graphique[i].append(WIN.afficherImage(j*TILE_SIZE, i*TILE_SIZE, 'wall.png'))
            elif map[i][j] == 'C':
                map_graphique[i].append(WIN.afficherImage(j * TILE_SIZE, i * TILE_SIZE, 'colon.png'))
            elif map[i][j] == 'E':
                map_graphique[i].append(WIN.afficherImage(j * TILE_SIZE, i * TILE_SIZE, 'ethernet.png'))
                spawners.append([i,j])
            elif map[i][j] == 'F':
                F = Enemy(j*TILE_SIZE, i*TILE_SIZE)
                map_graphique[i].append(WIN.afficherImage(j * TILE_SIZE, i * TILE_SIZE, 'fantome.png'))
            elif map[i][j] == 'U':
                map_graphique[i].append(WIN.afficherImage(j * TILE_SIZE, i * TILE_SIZE, 'upgrade.png'))
            elif map[i][j] == 'P':
                map_graphique[i].append(WIN.dessinerRectangle(j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE, 'green'))
                global P
                P = Player(j*TILE_SIZE, i*TILE_SIZE, game_options['hp'])
            else:
                map_graphique[i].append(WIN.dessinerRectangle(j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE, 'green'))
    return map, map_graphique


def wipe_out():
    for i in elt_on_screen:
        WIN.supprimer(i)


def spawn_fantome():
    try :
        spawn = random.choice(spawners)
        spawn[0], spawn[1]
        possible_spawn = []
        if map[spawn[0]-1][spawn[1]] not in blocking_tiles: possible_spawn.append([spawn[0]-1, spawn[1]])
        if map[spawn[0]+1][spawn[1]] not in blocking_tiles: possible_spawn.append([spawn[0]+1, spawn[1]])
        if map[spawn[0]][spawn[1]-1] not in blocking_tiles: possible_spawn.append([spawn[0], spawn[1]-1])
        if map[spawn[0]][spawn[1]+1] not in blocking_tiles: possible_spawn.append([spawn[0], spawn[1]+1])
        fantome_pos = random.choice(possible_spawn)
        map[fantome_pos[0]][fantome_pos[1]] = 'F'
        enemies.append(Enemy(fantome_pos[1]*TILE_SIZE, fantome_pos[0]*TILE_SIZE))
    except IndexError:
        print("How lucky! No Enemy spawn!")





print('Commande ? \n Z = Haut \n Q = Gauche \n S = Bas \n D = Droite \n Espace = Poser Bombe \n X = Ne Rien Faire')

menus = {
    'running':True,
    'in_game':False,
    'menu':True,
    'levels':False,
    'end_screen':False
}
win = False
elt_on_screen = []

while menus['running']:
    while menus['in_game']:

        # ACTION APRES LE TOUR DU JOUEUR
        if P.update():
            print(map)
            game_options['timer'] -= 1
            game_options['timer_enemy'] -= 1
            for i in enemies:
                i.update()
            if game_options['timer'] == 0:
                menus['in_game'] = False
                menus['end_screen'] = True
                win = True


                if current_level < 4:
                    levels[current_level+1] = True
            if game_options['timer_enemy'] == 0:
                spawn_fantome()
                game_options['timer_enemy'] = TIMER_ENEMY


    if menus['end_screen']:
        elt_on_screen.append(WIN.afficherTexte(f'Score:{game_options['score']}', W/2-50, H/7, 'black', 75))
        if current_level < 3 and win:
            elt_on_screen.append(WIN.dessinerRectangle(W/4-110,H-355,220, 110,'red'))
            elt_on_screen.append(WIN.afficherTexte('Next', W/4, H-300, 'white', 55))
            elt_on_screen.append(WIN.dessinerRectangle(W-330, H - 355, 220, 110, 'blue'))
            elt_on_screen.append(WIN.afficherTexte('Menu', W-220, H - 300, 'white', 55))
        else:
            elt_on_screen.append(WIN.dessinerRectangle(W / 4 - 110, H - 355, 220, 110, 'blue'))
            elt_on_screen.append(WIN.afficherTexte('Menu', W / 4, H - 300, 'white', 55))
        while menus['end_screen']:
            c = WIN.attendreClic()
            if current_level < 3 and W-330 < c.x < W-110 and H-335 < c.y < H-225:
                menus['end_screen'] = False
                menus['menu'] = True
                P.delete()
                for i in map_graphique:
                    for j in i:
                        WIN.supprimer(j)
                WIN.delete('all')
                print(map_graphique)
                wipe_out()
            if W/4-110 < c.x < W/4 + 110 and H-355 < c.y < H-245:
                if current_level < 3 and win:
                    menus['end_screen'] = False
                    menus['in_game'] = True
                    P.delete()
                    for i in map_graphique:
                        for j in i:
                            WIN.supprimer(j)
                    WIN.delete('all')
                    print(map_graphique)
                    wipe_out()
                    sleep(1)
                    del(P, map, map_graphique)
                    map, map_graphique = setup_game(f'map{current_level}.txt')
                    current_level += 1
                else:
                    menus['end_screen'] = False
                    menus['menu'] = True
                    P.delete()
                    for i in enemies:
                        i.kill()
                    WIN.delete('all')
                    print(len(enemies))
                    for i in map_graphique:
                        for j in i:
                            WIN.supprimer(j)
                    wipe_out()


    if menus['menu']:
        elt_on_screen.append(WIN.dessinerRectangle(W / 2 - 100, H / 2 - 50, 200, 100, 'white'))
        elt_on_screen.append(WIN.afficherTexte('Jouez', W/2, H/2, 'red', 50))

        while True:
            c = WIN.attendreClic()
            if W/2-100 < c.x < W/2+100 and H/2-50 < c.y < H/2+50:
                menus['menu'] = False
                wipe_out()
                menus['levels'] = True
                break
    if menus['levels']:
        elt_on_screen.append(WIN.dessinerRectangle(W/2-200, H/7-75, 400, 150, 'white'))
        if levels[1]: elt_on_screen.append(WIN.afficherTexte('Niveau 1', W/2, H/7, 'red', 55))
        else: elt_on_screen.append(WIN.afficherTexte('Niveau 1', W/2, H / 7, 'grey', 55))

        elt_on_screen.append(WIN.dessinerRectangle(W/2-200, H/2-150, 400, 150, 'white'))
        if levels[2]: elt_on_screen.append(WIN.afficherTexte('Niveau 2', W/ 2, H/2-75, 'red', 55))
        else: elt_on_screen.append(WIN.afficherTexte('Niveau 2', W / 2, H/2-75, 'grey', 55))

        elt_on_screen.append(WIN.dessinerRectangle(W/2-200, H-400, 400, 150, 'white'))
        if levels[3]: elt_on_screen.append(WIN.afficherTexte('Niveau 3', W / 2, H-325, 'red', 55))
        else: elt_on_screen.append(WIN.afficherTexte('Niveau 3', W / 2, H-325, 'grey', 55))

        while menus['levels']:
            c = WIN.attendreClic()
            if W/2-200 < c.x < W/2+200 and H/7-75 < c.y < H/7+75 and levels[1]:
                menus['levels'] = False
                wipe_out()
                map, map_graphique = setup_game()
                menus['in_game'] = True
                current_level = 1


            elif W / 2 - 200 < c.x < W / 2 + 200 and H / 2 - 150 < c.y < H / 2 and levels[2]:
                menus['levels'] = False
                wipe_out()
                map, map_graphique = setup_game('map1.txt')
                menus['in_game'] = True
                current_level = 2
                break

            elif W / 2 - 200 < c.x < W / 2 + 200 and H - 400 < c.y < H - 250 and levels[3]:
                menus['levels'] = False
                wipe_out()
                map, map_graphique = setup_game('map2.txt')
                menus['in_game'] = True
                current_level = 3
                break



WIN.fermerFenetre()









