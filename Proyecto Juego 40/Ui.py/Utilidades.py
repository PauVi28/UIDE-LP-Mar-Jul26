import py_compile

from ui.colores import NEGRO
from ui.fuentes import *

def texto_sombra(pantalla, texto, fuente, color, x, y):

    sombra = fuente.render(
        texto,
        True,
        (0, 0, 0)
    )

    pantalla.blit(
        sombra,
        (x + 4, y + 4)
    )

    render = fuente.render(
        texto,
        True,
        color
    )

    pantalla.blit(
        render,
        (x, y)
    )

def dibujar_fondo(pantalla):

    pantalla.fill(NEGRO)

    for i in range(12):

        pygame.draw.circle(
            pantalla,
            (100, 0, 0),
            (150 + i * 100, 200),
            120,
            2
        )

    for i in range(12):

        pygame.draw.circle(
            pantalla,
            (0, 70, 150),
            (100 + i * 100, 500),
            120,
            2
        )
