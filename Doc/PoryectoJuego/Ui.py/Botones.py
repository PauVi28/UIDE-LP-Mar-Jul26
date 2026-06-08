import pygame

from ui.colores import BLANCO
from ui.fuentes import fuente_menu

def dibujar_boton(
        pantalla,
        texto,
        x,
        y,
        color):

    rect = pygame.Rect(
        x,
        y,
        380,
        70
    )

    mouse = pygame.mouse.get_pos()

    color_actual = color

    if rect.collidepoint(mouse):

        color_actual = (

            min(color[0] + 40, 255),
            min(color[1] + 40, 255),
            min(color[2] + 40, 255)
        )

    pygame.draw.rect(
        pantalla,
        color_actual,
        rect,
        border_radius=18
    )

    pygame.draw.rect(
        pantalla,
        BLANCO,
        rect,
        3,
        border_radius=18
    )

    texto_render = fuente_menu.render(
        texto,
        True,
        BLANCO
    )

    pantalla.blit(
        texto_render,
        (x + 50, y + 18)
    )
