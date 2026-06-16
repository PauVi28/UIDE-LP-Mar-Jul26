import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pygame

from ui import recursos
from ui.menu import ejecutar_menu
from ui.partida import ejecutar_partida
from ui.multijugador import ejecutar_multijugador

ANCHO = 1000
ALTO = 600


def main():
    pygame.init()
 
    try:
        pygame.mixer.init()
    except pygame.error:
        pass

    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("40 - Juego de cartas ecuatoriano")
    reloj = pygame.time.Clock()

    fuentes = recursos.cargar_fuentes()
    sonidos = recursos.cargar_sonidos()

    estado = "menu"
    while estado != "salir":
        if estado == "menu":
            estado = ejecutar_menu(pantalla, reloj, fuentes, sonidos)
        elif estado == "jugar":
            estado = ejecutar_partida(pantalla, reloj, fuentes, sonidos)
        elif estado == "multijugador":
            estado = ejecutar_multijugador(pantalla, reloj, fuentes, sonidos)
        else:
            estado = "salir"

    pygame.quit()


if __name__ == "__main__":
    main()
