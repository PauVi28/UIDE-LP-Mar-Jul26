import pygame
from ui.menu import mostrar_menu
from ui.partida import mostrar_juego
from ui.multijugador import mostrar_multijugador

from logica.game40 import Game40

pygame.init()

ANCHO = 1280
ALTO = 720

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("40 Ecuatoriano")

clock = pygame.time.Clock()

juego = Game40()
estado = "menu"

ejecutando = True

while ejecutando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:

            x, y = pygame.mouse.get_pos()

            print(f"CLICK X={x} Y={y}")

            if estado == "menu":

                if 410 <= x <= 790 and 220 <= y <= 290:
                    estado = "partida"
                    print("CAMBIO A PARTIDA")

                elif 410 <= x <= 790 and 320 <= y <= 390:
                    estado = "multijugador"
                    print("CAMBIO A MULTIJUGADOR")

                elif 410 <= x <= 790 and 420 <= y <= 490:
                    ejecutando = False

            elif estado == "partida":

                x_cartas = 180

                for i in range(len(juego.mano_jugador)):

                    if x_cartas <= x <= x_cartas + 120 and 500 <= y <= 670:

                        juego.carta_seleccionada = i

                        print("Carta seleccionada:", i)

                    x_cartas += 140

                if 430 <= x <= 810 and 560 <= y <= 630:

                    if juego.carta_seleccionada is not None:

                        juego.jugar_turno(juego.carta_seleccionada)

                elif 40 <= x <= 420 and 620 <= y <= 690:

                    estado = "menu"

            elif estado == "multijugador":

                if 40 <= x <= 420 and 600 <= y <= 670:
                    estado = "menu"

    if estado == "menu":

        mostrar_menu(pantalla, juego)

    elif estado == "partida":

        mostrar_juego(pantalla, juego)

    elif estado == "multijugador":

        mostrar_multijugador(pantalla, juego)

    pygame.display.update()

    clock.tick(60)

pygame.quit()
