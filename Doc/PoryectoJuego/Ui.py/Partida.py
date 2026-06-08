import pygame

from ui.menu import (
    texto_sombra,
    dibujar_fondo,
    dibujar_boton,
    fuente_titulo,
    fuente_sub,
    fuente_cartas,
    BLANCO,
    ROJO,
    DORADO,
    NEGRO,
    MORADO
)

def mostrar_juego(
        pantalla,
        juego):

    dibujar_fondo(pantalla)

    texto_sombra(
        pantalla,
        "PARTIDA LOCAL",
        fuente_titulo,
        BLANCO,
        320,
        40
    )

    texto_sombra(
        pantalla,
        f"Jugador: {juego.puntaje_jugador}",
        fuente_sub,
        DORADO,
        50,
        150
    )

    texto_sombra(
        pantalla,
        f"CPU: {juego.puntaje_cpu}",
        fuente_sub,
        DORADO,
        1000,
        150
    )

    x = 180

    for i, carta in enumerate(juego.mano_jugador):

        borde = DORADO

        if juego.carta_seleccionada == i:

            borde = (0, 255, 0)

        pygame.draw.rect(
            pantalla,
            BLANCO,
            (x, 500, 120, 170),
            border_radius=18
        )

        pygame.draw.rect(
            pantalla,
            borde,
            (x, 500, 120, 170),
            4,
            border_radius=18
        )

        valor = carta[:-1]

        palo = carta[-1]

        color = NEGRO

        if palo in ["♥️", "♦️"]:

            color = ROJO

        texto_valor = fuente_cartas.render(
            valor,
            True,
            color
        )

        texto_palo = fuente_cartas.render(
            palo,
            True,
            color
        )

        pantalla.blit(
            texto_valor,
            (x + 15, 520)
        )

        pantalla.blit(
            texto_palo,
            (x + 40, 580)
        )

        x += 140

    texto_sombra(
        pantalla,
        "MESA",
        fuente_sub,
        BLANCO,
        580,
        250
    )

    x_mesa = 350

    for carta_mesa in juego.mesa:

        pygame.draw.rect(
            pantalla,
            BLANCO,
            (x_mesa, 300, 100, 140),
            border_radius=14
        )

        pygame.draw.rect(
            pantalla,
            DORADO,
            (x_mesa, 300, 100, 140),
            3,
            border_radius=14
        )

        valor = carta_mesa[:-1]

        palo = carta_mesa[-1]

        color = NEGRO

        if palo in ["♥️", "♦️"]:

            color = ROJO

        texto_valor = fuente_cartas.render(
            valor,
            True,
            color
        )

        texto_palo = fuente_cartas.render(
            palo,
            True,
            color
        )

        pantalla.blit(
            texto_valor,
            (x_mesa + 10, 315)
        )

        pantalla.blit(
            texto_palo,
            (x_mesa + 35, 370)
        )

        x_mesa += 120

    dibujar_boton(
        pantalla,
        "JUGAR CARTA",
        430,
        560,
        ROJO
    )

    dibujar_boton(
        pantalla,
        "VOLVER",
        40,
        620,
        MORADO
    )
