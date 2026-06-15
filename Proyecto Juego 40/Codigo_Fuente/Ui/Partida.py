import pygame

from logica.game40 import Game40
from ui import recursos


def ejecutar_partida(pantalla, reloj, fuentes, sonidos):
    ancho, alto = pantalla.get_size()
    fondo = recursos.Fondo(ancho, alto, intensidad=0.55)
    juego = Game40(modo="cpu")

    boton_menu = recursos.Boton("MENU", 20, alto - 52, 120, 40, fuentes["boton"])

    espera_cpu = 0.0     
    gano_sonado = False 

    recursos.reproducir(sonidos, "repartir")

    while True:
        dt = reloj.tick(60) / 1000.0
        pos = pygame.mouse.get_pos()
        termino = juego.ganador is not None

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if boton_menu.fue_clickeado(pos):
                    recursos.reproducir(sonidos, "clic")
                    return "menu"
                if termino:
                    recursos.reproducir(sonidos, "clic")
                    return "menu"
             
                if juego.turno == 1:
                    rects = recursos.rects_mano(len(juego.mano_jugador), ancho, alto)
                    for i, rect in enumerate(rects):
                        if rect.collidepoint(pos):
                            juego.jugar_carta(1, i)
                            recursos.sonido_de_evento(sonidos, juego.evento)
                            espera_cpu = 0.0
                            break

        if not termino and juego.turno == 2:
            espera_cpu += dt
            if espera_cpu >= 0.6:
                juego.turno_cpu()
                recursos.sonido_de_evento(sonidos, juego.evento)
                espera_cpu = 0.0

        fondo.actualizar(dt)
        fondo.dibujar(pantalla)
        vista = recursos.vista_local(juego, 1)
        recursos.dibujar_tablero(pantalla, fuentes, vista, pos)

        boton_menu.actualizar(pos)
        boton_menu.dibujar(pantalla)

        hover_carta = False
        if juego.turno == 1 and not termino:
            for rect in recursos.rects_mano(len(juego.mano_jugador), ancho, alto):
                if rect.collidepoint(pos):
                    hover_carta = True
        recursos.cursor_mano(boton_menu.hover or hover_carta or termino)

        if termino:
            if not gano_sonado:
                recursos.reproducir(sonidos, "ganar")
                gano_sonado = True
            recursos.dibujar_fin(pantalla, fuentes, vista["gane"])

        pygame.display.flip()
