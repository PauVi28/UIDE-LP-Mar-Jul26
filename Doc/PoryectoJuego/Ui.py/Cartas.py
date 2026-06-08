import pygame

from ui.colores import *
from ui.fuentes import fuente_cartas

def dibujar_cartas(pantalla):

    cartas_fijas = [

        ("A", "♠️"),
        ("K", "♥️"),
        ("Q", "♣️"),
        ("J", "♦️"),
        ("10", "♠️")

    ]

    posiciones = [

        (240, 500),
        (390, 500),
        (540, 500),
        (690, 500),
        (840, 500)

    ]

    for i in range(5):

        numero = cartas_fijas[i][0]

        simbolo = cartas_fijas[i][1]

        x = posiciones[i][0]

        y = posiciones[i][1]

        pygame.draw.rect(
            pantalla,
            BLANCO,
            (x, y, 120, 170),
            border_radius=18
        )

        pygame.draw.rect(
            pantalla,
            DORADO,
            (x, y, 120, 170),
            4,
            border_radius=18
        )

        color = NEGRO

        if simbolo == "♥️" or simbolo == "♦️":

            color = ROJO

        texto_numero = fuente_cartas.render(
            numero,
            True,
            color
        )

        texto_simbolo = fuente_cartas.render(
            simbolo,
            True,
            color
        )

        pantalla.blit(
            texto_numero,
            (x + 12, y + 10)
        )

        pantalla.blit(
            texto_simbolo,
            (x + 42, y + 65)
        )
