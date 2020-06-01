import pygame
import sys
import math

vec = pygame.math.Vector2
pygame.init()

# Paramètres de la fenêtre
nombre_sprite_cote_height = 22
nombre_sprite_cote_width = 34
taille_sprite = 30
cote_fenetre_height = nombre_sprite_cote_height * taille_sprite
cote_fenetre_width = nombre_sprite_cote_width * taille_sprite

# Personnalisation de la fenêtre
titre_fenetre = "Platformer 2D"
image_icone = "images/dk_droite.png"

# Listes des images du jeu
image_accueil = "images/accueil.png"
image_fond = "background.jpg"
image_mur = "mur.png"
image_depart = "depart.png"
image_arrivee = "arrivee.png"
image_nuage = "image/nuage.png"
image_carapace = "image/carapace.png"
map1 = "first_map.txt"
perso_droite = "image/player_right.png"
perso_gauche = "image/player_left.png"
SCREEN_RECT = pygame.Rect((0, 0, cote_fenetre_width, cote_fenetre_height))
speed = 8
jump_speed = 30
perso_taille = taille_sprite * 2
gravite = 10
player_largeur = 60
player_longueur = 60
screen = pygame.display.set_mode(SCREEN_RECT.size)

def exit():
    pygame.quit()
    sys.exit()


def main():
    global player_x, player_y


    fond = pygame.image.load(image_fond).convert()

    pygame.display.set_caption(titre_fenetre)

    menu()
    carte = niveaux(map1)
    carte.lecture_map()
    carte.affichage(screen)

    All_Block = pygame.sprite.Group()
    All_enemies = pygame.sprite.Group()

    num_j = 0
    for i in carte.structure:
        num_i = 0
        for sprite in i:
            x = num_i * taille_sprite
            y = num_j * taille_sprite
            if sprite == 'S':
                player_x = x
                player_y = y
            if sprite == 'B':
                bloc = Block(x, y, taille_sprite, taille_sprite)
                All_Block.add(bloc)
            if sprite == 'E':
                enemies = Block(x, y, taille_sprite, taille_sprite)
                All_enemies.add(enemies)
            if sprite == 'V':
                enemies = Block(x, y, taille_sprite, taille_sprite)
                All_enemies.add(enemies)
            num_i += 1
        num_j += 1

    player = Player(player_x, player_y, perso_droite, perso_gauche)

    fps = pygame.time.Clock()
    play = True

    while (play):

        fps.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        collision = pygame.sprite.spritecollide(player, All_Block, False)
        if collision:
            pressed = pygame.key.get_pressed()

            if player.pos.x + perso_taille - 5 <= collision[0].rect.left:
                player.key_right = False

            #if player.pos.x + 5 >= collision[0].rect.x + taille_sprite:
                #player.key_left = False

            if player.pos.y + player_longueur + 8 >= collision[0].rect.top and player.key_right != False and player.key_left != False:
                player.pos.y = collision[0].rect.top - perso_taille

        enemies_collision = pygame.sprite.spritecollide(player, All_enemies, False)
        if enemies_collision:
            player.health -= 1
            player.pos.x = player_x
            player.pos.y = player_y

        if player.pos.y > cote_fenetre_height:
            player.health -= 1
            player.pos.x = player_x
            player.pos.y = player_y

        if player.health <= 0:
            player.health = player.healthMax
            game_over()

        player.update()
        pygame.display.update()
        pygame.display.flip()
        screen.blit(fond, (0, 0))
        carte.affichage(screen)

        screen.blit(player.right_direction, (player.pos.x, player.pos.y))


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
        nuage = pygame.image.load(image_nuage)
        nuage = pygame.transform.scale(nuage, (taille_sprite, taille_sprite))
        carapace = pygame.image.load(image_carapace)
        carapace = pygame.transform.scale(carapace, (taille_sprite, taille_sprite))
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
                elif sprite == 'V':
                    screen.blit(nuage, (x, y))
                elif sprite == 'E':
                    screen.blit(carapace, (x, y))

                num_i = num_i + 1
            num_j = num_j + 1


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, right, left):
        pygame.sprite.Sprite.__init__(self)
        self.right_direction = pygame.Surface((perso_taille, perso_taille))
        self.right_direction = pygame.image.load(right).convert_alpha()
        self.right_direction = pygame.transform.scale(self.right_direction, (perso_taille, perso_taille))

        self.left_direction = pygame.image.load(left).convert_alpha()
        self.left_direction = pygame.transform.scale(self.left_direction, (perso_taille, perso_taille))

        self.rect = self.right_direction.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.Surface((player_longueur, player_largeur))

        self.health = 3
        self.healthMax = 3
        self.vitesse = vec(0, 0)
        self.pos = vec(x, y)
        self.key_right = True
        self.key_left = True

    def update(self):
        self.vitesse = vec(0, 8)
        pressed = pygame.key.get_pressed()

        if self.key_right:
            if pressed[pygame.K_RIGHT]:
                self.vitesse.x = 5

        if self.key_left:
            if pressed[pygame.K_LEFT]:
                self.vitesse.x = -5

        self.key_left = True
        self.key_right = True
        self.pos += self.vitesse
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.image.load(perso_droite)


def menu():
    fond = pygame.image.load("image/fond.jpg").convert()
    fond = pygame.transform.scale(fond, (cote_fenetre_width, cote_fenetre_height))
    play_button = pygame.image.load("image/button.png")
    play_button = pygame.transform.scale(play_button, (400, 150))
    play_button_rect = play_button.get_rect()
    play_button_rect.x = math.ceil(screen.get_width() / 3.2)
    play_button_rect.y = math.ceil(screen.get_height() / 1.4)


    continuer = True

    while continuer:
        screen.blit(fond, (0, 0))
        screen.blit(play_button, (play_button_rect.x, play_button_rect.y))
        for event in pygame.event.get():  # Attente des événements
            if event.type == pygame.QUIT:
                continuer = 0
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    continuer = False
        pygame.display.flip()

def game_over():
    fond_over = pygame.image.load("image/game_over/Game over.png").convert()
    play_button = pygame.image.load("image/game_over/Try again.png")
    play_button = pygame.transform.scale(play_button, (183, 54))
    play_button_rect = play_button.get_rect()
    play_button_rect.x = math.ceil(screen.get_width() / 2)
    play_button_rect.y = math.ceil(screen.get_height() / 1.2)

    screen.blit(fond_over, (0, 0))
    screen.blit(play_button, play_button_rect)
    continuer = True
    while continuer:

        for event in pygame.event.get():  # Attente des événements
            if event.type == pygame.QUIT:
                continuer = 0
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    continuer = False
        pygame.display.flip()

if __name__ == '__main__':
    main()
