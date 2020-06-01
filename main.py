import pygame
import sys

vec = pygame.math.Vector2
pygame.init()

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
perso_droite = "image/player_right.png"
perso_gauche = "image/player_left.png"
SCREEN_RECT = pygame.Rect((0, 0, cote_fenetre, cote_fenetre))
speed = 8
jump_speed = 30
perso_taille = taille_sprite * 2
gravite = 10
player_largeur = 60
player_longueur = 60



def exit():
    pygame.quit()
    sys.exit()


def main():
    global player_x, player_y



    pygame.display.set_caption(titre_fenetre)

    screen = pygame.display.set_mode(SCREEN_RECT.size)
    fond = pygame.image.load(image_fond).convert()

    carte = niveaux(map1)
    carte.lecture_map()
    carte.affichage(screen)

    All_Block = pygame.sprite.Group()

    num_j = 0
    for i in carte.structure:
        num_i = 0
        k = 0
        for sprite in i:
            x = num_i * taille_sprite
            y = num_j * taille_sprite
            if sprite == 'S':
                player_x = x
                player_y = y
            if sprite == 'B':
                k += 1
                bloc_k = Block(x, y, taille_sprite, taille_sprite, image_mur)
                All_Block.add(bloc_k)
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

        player.update()

        collision = pygame.sprite.spritecollide(player, All_Block, False)
        if collision:
            pressed = pygame.key.get_pressed()
            if player.pos.y < collision[0].rect.top:
                player.pos.y = collision[0].rect.top - perso_taille
                player.vitesse.y = 0


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

        self.vitesse = vec(0, 0)
        self.pos = vec(x, y)

    def update(self):
        self.vitesse = vec(0, 2)
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]: self.vitesse.x = 5
        if pressed[pygame.K_LEFT]:  self.vitesse.x = -5
        self.pos += self.vitesse
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.image.load(perso_droite)



if __name__ == '__main__':
    main()
