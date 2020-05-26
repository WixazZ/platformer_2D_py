'''''

pg.init()

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.gravity = 1
        self.velocity = 3
        self.life = 3
        self.all_project = pg.sprite.Group()
        self.image = pg.image.load('player.png')
        self.rect = self.image.get_rect()
        self.rect_x = 100
        self.rect_y = 50
        self.jump_height = 100

    def deplacement(self):
        if game.pressed.get(pg.K_a) :
            self.rect.x -= self.velocity

class Game:
    def __init__(self):
        self.player = Player()
        self.pressed = {}


fenetre_x = 900
fenetre_y = 900
pos_player_x = 500
pos_player_y = 500

fenetre = pg.display.set_mode((fenetre_x, fenetre_y))

background = [200, 100, 100]
#background = pg.image.load()


player = Player()
game =Game()
fenetre.fill(background)
#perso = pg.draw.rect(fenetre, green, (50, 50, 50, 50))
pg.display.flip()

valide = True
while valide:
    #fenetre.blit(background, (0, 0))
    fenetre.blit(game.player.image, player.rect)
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            valide = False
        game.player.deplacement()


pg.quit()
'''

'''''
pygame.init()

pygame.display.set_caption('Comet Fall Game')

taille_x = 1064
taille_y = 710

screen = pygame.display.set_mode((taille_x, taille_y))

game = Game()

player = Player()

background = pygame.image.load('background.jpg')


run = True


while run:


    screen.blit(background, (0, 0))
    screen.blit(game.player.image, game.player.rect)

    for projectile in game.player.all_projectiles:
        projectile.move()

    game.player.all_projectiles.draw(screen)

    if (taille_x-320 >= game.player.rect.x >= 0):
        if game.pressed.get(pygame.K_d):
            if game.pressed.get(pygame.K_SPACE) :
                if game.player.one_jump == True:
                    game.player.jump()
            game.player.move_right()

        elif game.pressed.get(pygame.K_a):
            if game.pressed.get(pygame.K_SPACE):
                if game.player.one_jump == True:
                    game.player.jump()
            game.player.move_left()

        elif game.pressed.get(pygame.K_SPACE):
            if game.player.one_jump == True:
                game.player.jump()

    elif(game.player.rect.x < 0):
        game.player.rect.x = 0

    elif(game.player.rect.x > taille_x-320):
        game.player.rect.x = taille_x - 320

    if game.player.rect.y >= 500:
        game.player.one_jump = True

    if game.player.rect.y < 500:
        game.player.gravityy()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
            quit()

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            if event.key == pygame.K_f:
                game.player.launch_projectile()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

    pygame.display.update()
'''
import pygame
HORIZONTAL_PLAT = 1000
VERTICAL_PLAT = 30*28
import sys
SCREEN_RECT = pygame.Rect((0, 0, 1000, 30*28))


def exit():
    pygame.quit()
    sys.exit()

def main():

    pygame.init()
    pygame.display.set_caption('Platformer 2D')

    screen = pygame.display.set_mode(SCREEN_RECT.size)
    fond = pygame.image.load("background.jpg").convert()


    carte = niveaux('first_map.txt')
    carte.lecture_map()
    carte.affichage(screen)

    player = Player('image\player_right.png', 'image\player_left.png', carte)

    pygame.key.set_repeat(1, 20)
    fps = pygame.time.Clock()
    play = True

    while(play):


        fps.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.move('right')
                elif event.key == pygame.K_LEFT:
                    player.move('left')
        pygame.display.update()
        pygame.display.flip()
        screen.blit(fond, (0, 0))
        carte.affichage(screen)

        screen.blit(player.default_direction, (player.x, player.y))


class niveaux:
    def __init__(self, maprecup):
        self.map = maprecup
        self.structure = None

    def lecture_map(self):
        with open(self.map, 'r') as map:
            struct_niveau = []
            for i in map:
                struct_niveau.append(str(i) + "\n")
            self.structure = struct_niveau


    def affichage(self, screen):
        block = pygame.image.load('mur.png').convert()
        start = pygame.image.load('depart.png').convert()
        finish = pygame.image.load('arrivee.png').convert_alpha()
        num_j = 0
        for i in self.structure:
            num_i = 0
            for sprite in i:
                x = num_i * 30
                y = num_j * 30
                if sprite == 'B':
                    screen.blit(block, (x, y))
                elif sprite == 'S':
                    screen.blit(start, (x, y))
                elif sprite == 'F':
                    screen.blit(finish, (x, y))
                num_i = num_i + 1
            num_j = num_j + 1


class Player:
    def __init__(self, right, left, map):
        self.right_direction = pygame.image.load(right)
        self.right_direction = pygame.transform.scale(self.right_direction, (30*2, 30*2))
        self.left_direction = pygame.image.load(left)
        self.left_direction = pygame.transform.scale(self.left_direction, (30*2, 30*2))

        self.default_direction = self.right_direction
        self.health = 3
        num_j = 0
        for i in map.structure:
            num_i = 0
            for sprite in i:
                x = num_i * 30
                y = num_j * 30
                if sprite == 'S':
                    self.x = x
                    self.y = y
                num_i += 1
            num_j += 1

    def move(self, direction):
        if direction == 'right':
            if self.x+8 < (1000-60):
                self.x += 8
            else:
                self.x =1000-60
            self.default_direction = self.right_direction

        elif direction == 'left':
            if self.x-8 > (30):
                self.x -= 8
            else:
                self.x = 30
            self.default_direction = self.left_direction


    #def collision(self, direction):
        #if(self.x + 30*2):


if __name__ == '__main__':
    main()
