import pygame as pg

pg.init()

fenetre_x = 900
fenetre_y = 900

fenetre = pg.display.set_mode((fenetre_x,fenetre_y))


background = [100, 100, 100]
#background = pg.image.load()
green = (0, 255, 0)


fenetre.fill(background)
perso = pg.draw.rect(fenetre, green, (50, 50, 50, 50))
pg.display.flip()

game = True
while game:
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False
        elif event.type == pg.KEYDOWN:
            if event.type == pg.K_SPACE:
                while
pg.quit()