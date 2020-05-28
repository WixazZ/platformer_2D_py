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
import sys

# Paramètres de la fenêtre
nombre_sprite_cote = 28
taille_sprite = 30
cote_fenetre = nombre_sprite_cote * taille_sprite

# Personnalisation de la fenêtre
titre_fenetre = "Platformer 2D"
image_icone = "images/dk_droite.png"

# Listes des images du jeu
image_accueil = "images/accueil.png"
image_fond = "background.jpg"
image_mur = "mur.png"
image_depart = "depart.png"
image_arrivee = "arrivee.png"
map1 = "first_map.txt"
perso_droite = "image\player_right.png"
perso_gauche = "image\player_left.png"
SCREEN_RECT = pygame.Rect((0, 0, cote_fenetre, cote_fenetre))
speed = 8
jump_speed = 40
perso_taille = taille_sprite * 2
gravite = 10


def exit():
    pygame.quit()
    sys.exit()


def main():
    pygame.init()
    pygame.display.set_caption(titre_fenetre)

    screen = pygame.display.set_mode(SCREEN_RECT.size)
    fond = pygame.image.load(image_fond).convert()

    carte = niveaux(map1)
    carte.lecture_map()
    carte.affichage(screen)

    player = Player(perso_droite, perso_gauche, carte)

    pygame.key.set_repeat(1, 20)
    fps = pygame.time.Clock()
    play = True

    while (play):

        fps.tick(30)
        player.move('gravite', carte)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.move('right', carte)
                    if event.key == pygame.K_SPACE:
                        player.move('jump', carte)

                elif event.key == pygame.K_LEFT:
                    player.move('left', carte)
                    if event.key == pygame.K_SPACE:
                        player.move('jump', carte)

                elif event.key == pygame.K_SPACE:
                    player.move('jump', carte)


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
        block = pygame.image.load(image_mur).convert()
        start = pygame.image.load(image_depart).convert()
        finish = pygame.image.load(image_arrivee).convert_alpha()
        num_j = 0
        for i in self.structure:
            num_i = 0
            for sprite in i:
                x = num_i * taille_sprite
                y = num_j * taille_sprite
                if sprite == 'B':
                    screen.blit(block, (x, y))
                elif sprite == 'S':
                    screen.blit(start, (x, y))
                elif sprite == 'F':
                    screen.blit(finish, (x, y))
                num_i = num_i + 1
            num_j = num_j + 1


class Player:
    def __init__(self, right, left, carte):
        self.right_direction = pygame.image.load(right)
        self.right_direction = pygame.transform.scale(self.right_direction, (perso_taille, perso_taille))
        self.left_direction = pygame.image.load(left)
        self.left_direction = pygame.transform.scale(self.left_direction, (perso_taille, perso_taille))
        self.default_direction = self.right_direction
        self.health = 3
        self.jump = False

        num_j = 0
        for i in carte.structure:
            num_i = 0
            for sprite in i:
                x = num_i * taille_sprite
                y = num_j * taille_sprite
                if sprite == 'S':
                    self.x = x
                    self.y = y
                num_i += 1
            num_j += 1

    def move(self, direction, carte):
        if direction == 'right':
            if self.collision(self.x + speed, self.y, carte):
                self.x += speed

            self.default_direction = self.right_direction

        elif direction == 'left':
            if self.collision(self.x - speed, self.y, carte):
                self.x -= speed

            self.default_direction = self.left_direction

        elif direction == 'gravite':
            if self.collision(self.x, self.y + 10, carte):
                self.y += gravite

        elif direction == 'jump':
            print("",self.jump)
            if not self.jump:
                self.jump = True
                self.jump_y = self.y
            else:
                if self.collision(self.x, self.y - jump_speed, carte):
                    self.y -= jump_speed

    def collision(self, x_perso, y_perso, carte):
        num_j = 0
        for i in carte.structure:
            num_i = 0
            for sprite in i:
                x = num_i * taille_sprite
                y = num_j * taille_sprite
                if sprite == 'B':
                    self.block_x = x
                    self.block_y = y
                    if (x_perso + perso_taille >= self.block_x) and (self.block_x + taille_sprite >= x_perso) and (
                            y_perso + perso_taille >= self.block_y) and (self.block_y + taille_sprite >= y_perso):
                        return False
                num_i += 1
            num_j += 1
        return True


if __name__ == '__main__':
    main()
