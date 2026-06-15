import pygame
import time
from ui.menu import mostrar_menu
from ui.partida import mostrar_juego
from ui.multijugador import mostrar_multijugador
from multiplayer import estados
from logica.game40 import Game40

pygame.init()

ANCHO = 1280
ALTO = 720

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("40 Ecuatoriano")

clock = pygame.time.Clock()

juego = Game40()
estado = "menu"
host_iniciado = False
cliente=None

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

                if 430 <= x <= 810 and 560 <= y <= 630:

                    print("BOTON JUGAR PRESIONADO")

                    if juego.carta_seleccionada is not None:
                        if estados.conectado:
                            estados.cliente.enviar({
                                "tipo": "jugada",
                                "indice": juego.carta_seleccionada
                            })
                        else:
                            juego.jugar_turno(juego.carta_seleccionada)

                elif 40 <= x <= 420 and 620 <= y <= 690:

                    estado = "menu"
                else:

                    x_cartas = 180

                    for i in range(len(juego.mano_jugador)):

                        if (
                            x_cartas <= x <= x_cartas + 120
                            and
                            500 <= y <= 670
                        ):

                            juego.carta_seleccionada = i

                            print(
                                "Carta seleccionada:",
                                i
                            )

                            break

                        x_cartas += 140
         
                if 430 <= x <= 810 and 400 <= y <= 470:
                    print("BOTON JUGAR PRESIONADO")

                    if juego.carta_seleccionada is not None:

                        juego.jugar_turno(juego.carta_seleccionada)

                elif 40 <= x <= 420 and 620 <= y <= 690:

                    estado = "menu"

            elif estado == "multijugador":
                
                if 420 <= x <= 800 and 250 <= y <= 320:

                    print("CREAR PARTIDA")

                    from multiplayer.host import iniciar_host
                    if not host_iniciado:
                        iniciar_host()
                        time.sleep(1)
                        estados.es_host = True
                        host_iniciado = True
                        print("HOST INICIADO")
            
                elif 420 <= x <= 800 and 350 <= y <= 420:

                    print("UNIRSE A PARTIDA")

                    from network.cliente import ClienteLAN
                    try:
                        cliente = ClienteLAN("127.0.0.1")
                        from multiplayer import estados
                        estados.cliente=cliente
                        estados.conectado=True
                        print("CONECTADO")
                        cliente.enviar({
                            "tipo": "mensaje",
                            "texto": "Hola desde LAN"
                        })

                        print("MENSAJE ENVIADO")
                    except Exception as e:
                        print("ERROR",e)
               
                elif 40 <= x <= 420 and 600 <= y <= 670:
                    estado = "menu"

    if estado == "menu":

        mostrar_menu(pantalla, juego)

    elif estado == "partida":

        mostrar_juego(pantalla, juego)

    elif estado == "multijugador":

        mostrar_multijugador(pantalla, juego)
    fuente = pygame.font.SysFont(
        None,
        60
    )
    if juego.ganador is not None:

        texto = fuente.render(
            f"GANADOR: {juego.ganador}",
            True,
            (255, 255, 0)
        )

        pantalla.blit(
            texto,
            (300, 200)
        )

    if cliente is not None:

        while len(cliente.mensajes) > 0:

            mensaje = cliente.mensajes.pop(0)
            if mensaje["tipo"] == "jugada":
                print("JUGADA RECIBIDA:", mensaje["indice"])

            print("RECIBIDO:", mensaje)
    pygame.display.update()


    clock.tick(60)

pygame.quit()
