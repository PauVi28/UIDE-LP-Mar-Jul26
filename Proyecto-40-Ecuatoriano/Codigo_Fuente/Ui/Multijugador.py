from ui.utilidades import *
from ui.botones import dibujar_boton
from ui.colores import *
from ui.fuentes import *

def mostrar_multijugador(pantalla, juego):

    dibujar_fondo(pantalla)

    texto_sombra(
        pantalla,
        "MULTIJUGADOR LAN",
        fuente_titulo,
        BLANCO,
        220,
        100
    )

    texto_sombra(
        pantalla,
        "Próximamente...",
        fuente_sub,
        DORADO,
        500,
        250
    )

    dibujar_boton(
        pantalla,
        "VOLVER",
        40,
        600,
        MORADO
    )
