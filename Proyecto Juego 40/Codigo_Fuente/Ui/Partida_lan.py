import threading

import pygame

from ui import recursos
from multiplayer import estados


def _escuchar_cliente(cliente, estado_ref, hay_nuevo, activo, lock):
   
    while activo[0]:
        try:
            datos = cliente.recibir()
        except OSError:
            break
        if datos is None:
            break
        with lock:
            estado_ref[0] = datos
            hay_nuevo[0] = True


def ejecutar_partida_lan(pantalla, reloj, fuentes, sonidos, host=None, cliente=None):
 
    ancho, alto = pantalla.get_size()
    fondo = recursos.Fondo(ancho, alto, intensidad=0.55)
    soy_host = host is not None

    boton_menu = recursos.Boton("SALIR", 20, alto - 52, 120, 40, fuentes["boton"])
    gano_sonado = False

    estado_ref = [estados.estado_vacio()]
    hay_nuevo = [False]
    activo = [True]
    lock = threading.Lock()
    if not soy_host:
        hilo = threading.Thread(
            target=_escuchar_cliente,
            args=(cliente, estado_ref, hay_nuevo, activo, lock),
            daemon=True)
        hilo.start()

    recursos.reproducir(sonidos, "repartir")

    def terminar(accion):
        activo[0] = False
        if soy_host:
            host.cerrar()
        else:
            cliente.cerrar()
        return accion

    while True:
        dt = reloj.tick(60) / 1000.0
        pos = pygame.mouse.get_pos()

        if soy_host:
            turno_antes = host.juego.turno
            host.procesar()               
            if host.juego.turno != turno_antes:
                recursos.sonido_de_evento(sonidos, host.juego.evento)
            vista = recursos.vista_local(host.juego, 1)
            mi_mano = host.juego.mano_jugador
            mi_turno = host.juego.turno == 1
            termino = host.juego.ganador is not None
        else:
            with lock:
                estado = estado_ref[0]
                nuevo = hay_nuevo[0]
                hay_nuevo[0] = False
            if nuevo:
                recursos.sonido_de_evento(sonidos, estado.get("evento", ""))
            vista = recursos.vista_remota(estado)
            mi_mano = estado["mano_jugador2"]
            mi_turno = estado["turno"] == 2
            termino = estado["ganador"] is not None

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return terminar("salir")
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if boton_menu.fue_clickeado(pos):
                    recursos.reproducir(sonidos, "clic")
                    return terminar("menu")
                if mi_turno and not termino:
                    rects = recursos.rects_mano(len(mi_mano), ancho, alto)
                    for i, rect in enumerate(rects):
                        if rect.collidepoint(pos):
                            if soy_host:
                                host.jugar_host(i)
                                recursos.sonido_de_evento(sonidos, host.juego.evento)
                            else:
                                cliente.enviar({"tipo": "jugar", "indice": i})
                            break

        fondo.actualizar(dt)
        fondo.dibujar(pantalla)
        recursos.dibujar_tablero(pantalla, fuentes, vista, pos)

        boton_menu.actualizar(pos)
        boton_menu.dibujar(pantalla)

        hover_carta = False
        if mi_turno and not termino:
            for rect in recursos.rects_mano(len(mi_mano), ancho, alto):
                if rect.collidepoint(pos):
                    hover_carta = True
        recursos.cursor_mano(boton_menu.hover or hover_carta)

        if termino:
            if not gano_sonado:
                recursos.reproducir(sonidos, "ganar")
                gano_sonado = True
            recursos.dibujar_fin(pantalla, fuentes, vista["gane"])

        pygame.display.flip()
