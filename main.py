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
titre_fenetre = "Random survival"

# Listes des images du jeu
image_accueil = "images/accueil.png"
image_fond = "background.jpg"
image_mur = "mur.png"
image_arrivee = "arrivee.png"
image_nuage = "image/nuage.png"
image_carapace = "image/carapace.png"
map1 = "first_map.txt"
perso_droite = "image/player_right.png"
perso_gauche = "image/player_left.png"
SCREEN_RECT = pygame.Rect((0, 0, cote_fenetre_width, cote_fenetre_height))
screen = pygame.display.set_mode(SCREEN_RECT.size)

#variable global
speed = 8
jump_speed = 30
perso_taille = taille_sprite * 2
gravite = 10
player_largeur = 60
player_longueur = 60


#sort du jeu
def exit():
    pygame.quit()
    sys.exit()

#fonction principale
def main():
    global player_x, player_y #deux valeurs d'apparition


    fond = pygame.image.load(image_fond).convert()  #met le background

    pygame.display.set_caption(titre_fenetre)   #nom du jeu

    menu()

    #va chercher la map en texte
    carte = niveaux(map1)
    carte.lecture_map()
    carte.affichage(screen)

    #créer les groups pour les collisions
    All_Block = pygame.sprite.Group()
    All_enemies = pygame.sprite.Group()
    victoire_groups = pygame.sprite.Group()

    #va chercher chaque caractere du .txt pour les ajouter au groupe
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
            if sprite == 'F':
                victoire_block = Block(x, y, taille_sprite, taille_sprite)
                victoire_groups.add(victoire_block)
            num_i += 1
        num_j += 1

    #défini a player la class Player
    player = Player(player_x, player_y, perso_droite, perso_gauche)

    #mets une limite a nombre de tours pas seconde du  programe
    fps = pygame.time.Clock()

    #tant que play = true la boucle continue
    play = True

    #boucle de jeu principal1
    while (play):

        #application du nombre de frame par seconde a 30
        fps.tick(30)

        # on appui sur la croix pour quitter le jeu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        #collision avec les block

        collision = pygame.sprite.spritecollide(player, All_Block, False)
        if collision:
            pressed = pygame.key.get_pressed()

            #vérifie la collision a gauche
            if player.pos.x + perso_taille - 5 <= collision[0].rect.left:
                player.key_right = False

            # vérifie la collision a droite mais créer un bug quand il y a un déplacement sur la gauche

            #if player.pos.x + 5 >= collision[0].rect.x + taille_sprite:
                #player.key_left = False

            # vérifie la collision vers le haut mais ne fonctionne pas

            #if player.pos.y + perso_taille > collision[0].rect.top + taille_sprite:
                #print("test")
                #player.pos.y = player.pos.y+20
                #player.hauter_max_atteint = True

            #vérifie la collision avec une platforme du dessous et block la gracvité
            if player.pos.y + player_longueur >= collision[0].rect.top and player.key_right != False and player.key_left != False:
                player.pos.y = collision[0].rect.top - perso_taille-5
                if pressed[pygame.K_SPACE]:
                    #met tout les condition de saut en initial
                    player.key_jump = True
                    player.en_saut = True
                    player.hauter_max_atteint = False
                    player.jumpMAX = player.pos.y - 5*30



        #collision contre un enemie
        enemies_collision = pygame.sprite.spritecollide(player, All_enemies, False)
        if enemies_collision:
            player.health -= 1
            player.pos.x = player_x
            player.pos.y = player_y

        #collision avec le block de la victoire
        victory_collision = pygame.sprite.spritecollide(player, victoire_groups, False)
        if victory_collision:
            #remet tout a l'initial si tenté une nouvelle partie
            player.health = player.healthMax
            player.pos.x = player_x
            player.pos.y = player_y
            player.key_jump = False
            player.en_saut = False
            victory()

        #si sort de l'écran perd une vie
        if player.pos.y > cote_fenetre_height:
            player.health -= 1
            player.pos.x = player_x
            player.pos.y = player_y

        #si plus de vie écran de fin
        if player.health <= 0:
            # remet tout a l'initial si tenté une nouvelle partie
            player.health = player.healthMax
            player.pos.x = player_x
            player.pos.y = player_y
            player.key_jump = False
            player.en_saut = False
            game_over()

        player.update()
        pygame.display.update()
        pygame.display.flip()
        screen.blit(fond, (0, 0))
        carte.affichage(screen)

        screen.blit(player.direction, (player.pos.x, player.pos.y))


#classe niveau pour initialisé la map
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

    #affichage de tout les joueurs
    def affichage(self, screen):
        block = pygame.image.load(image_mur).convert()
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
                elif sprite == 'F':
                    screen.blit(finish, (x, y))
                elif sprite == 'V':
                    screen.blit(nuage, (x, y))
                elif sprite == 'E':
                    screen.blit(carapace, (x, y))

                num_i = num_i + 1
            num_j = num_j + 1


#classe joueur sprite pour les collisions
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, right, left):
        pygame.sprite.Sprite.__init__(self)
        self.right_direction = pygame.Surface((perso_taille, perso_taille))
        self.right_direction = pygame.image.load(right).convert_alpha()
        self.right_direction = pygame.transform.scale(self.right_direction, (perso_taille, perso_taille))

        self.left_direction = pygame.image.load(left).convert_alpha()
        self.left_direction = pygame.transform.scale(self.left_direction, (perso_taille, perso_taille))
        self.direction = self.right_direction
        self.rect = self.direction.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.Surface((player_longueur, player_largeur))

        self.health = 3
        self.healthMax = 3

        self.vitesse = vec(0, 0)
        self.pos = vec(x, y)
        self.jumpMAX = self.pos.y - 5 * 30
        self.hauter_max_atteint = False
        self.en_saut = False
        self.key_jump = False
        self.key_right = True
        self.key_left = True

    #fonction pour gérer tout les mouvements des joueurs
    def update(self):
        self.vitesse = vec(0, 8)
        pressed = pygame.key.get_pressed()

        if self.key_right:
            if pressed[pygame.K_RIGHT]:
                self.direction = self.right_direction
                self.vitesse.x = 5

        if self.key_left:
            if pressed[pygame.K_LEFT]:
                self.direction = self.left_direction
                self.vitesse.x = -5
        if self.key_jump == True:
            self.key_jump = False


        if self.en_saut == True and self.hauter_max_atteint == False:
            if self.pos.y > self.jumpMAX:
                self.vitesse.y = -20
            else:
                self.hauter_max_atteint = True
        self.key_left = True
        self.key_right = True
        self.pos += self.vitesse
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y


#créer des sprite de block pour les ajouter au groupe
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.image.load(perso_droite)


#fonction menu
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

#fonction game over
def game_over():
    fond_over = pygame.image.load("image/game_over/Game over.png").convert()
    fond_over = pygame.transform.scale(fond_over, (cote_fenetre_width, cote_fenetre_height))
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

#fonction de victoire
def victory():
    fenetre = pygame.display.set_mode((34 * 30, 22 * 30))
    fond_victory = pygame.image.load("image/victoire.png").convert()
    fond_victory = pygame.transform.scale(fond_victory, (cote_fenetre_width, cote_fenetre_height))
    play_button = pygame.image.load("image/Try again.png")
    play_button = pygame.transform.scale(play_button, (183, 54))
    play_button_rect = play_button.get_rect()
    play_button_rect.x = math.ceil(fenetre.get_width() / 2)
    play_button_rect.y = math.ceil(fenetre.get_height() / 1.2)
    fenetre.blit(fond_victory, (0, 0))
    fenetre.blit(play_button, (play_button_rect.x, play_button_rect.y))
    pygame.display.flip()

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
