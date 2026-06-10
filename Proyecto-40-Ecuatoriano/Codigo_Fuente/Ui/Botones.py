from ui.utilidades import *
from ui.botones import dibujar_boton
from ui.cartas import dibujar_cartas
from ui.colores import *
from ui.fuentes import *

def mostrar_menu(
        pantalla,
        juego):

    dibujar_fondo(pantalla)

    texto_sombra(
        pantalla,
        "40 ECUATORIANO",
        fuente_titulo,
        BLANCO,
        250,
        70
    )

    texto_sombra(
        pantalla,
        "Inspirado en Balatro",
        fuente_sub,
        ROJO,
        470,
        160
    )

    dibujar_boton(
        pantalla,
        "JUGAR",
        410,
        220,
        ROJO
    )

    dibujar_boton(
        pantalla,
        "MULTIJUGADOR LAN",
        410,
        320,
        AZUL
    )

    dibujar_boton(
        pantalla,
        "SALIR",
        410,
        420,
        MORADO
    )

    dibujar_cartas(pantalla)
