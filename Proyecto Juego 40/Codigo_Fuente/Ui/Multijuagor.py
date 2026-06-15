import socket

import pygame

from network import config
from network.cliente import Cliente
from multiplayer.host import Host
from ui import recursos
from ui.partida_lan import ejecutar_partida_lan


def _ip_local():
  
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))    
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "tu IP local"


def _texto_centrado(pantalla, fuente, texto, y, color):
    img = fuente.render(texto, True, color)
    pantalla.blit(img, img.get_rect(center=(pantalla.get_width() // 2, y)))


def ejecutar_multijugador(pantalla, reloj, fuentes, sonidos):
    ancho, alto = pantalla.get_size()
    fondo = recursos.Fondo(ancho, alto)
    cx = ancho // 2

    pantalla_actual = "elegir" 
    ip_texto = ""
    mensaje_error = ""
    host = None

    b_host = recursos.Boton("SER HOST", cx - 180, 290, 360, 56, fuentes["boton"])
    b_unir = recursos.Boton("UNIRSE A PARTIDA", cx - 180, 362, 360, 56, fuentes["boton"])
    b_volver = recursos.Boton("VOLVER", cx - 180, 434, 360, 56, fuentes["boton"])

    b_conectar = recursos.Boton("CONECTAR", cx - 180, 372, 360, 56, fuentes["boton"])
    b_volver2 = recursos.Boton("VOLVER", cx - 180, 444, 360, 56, fuentes["boton"])
    campo_ip = pygame.Rect(cx - 180, 300, 360, 50)

    b_cancelar = recursos.Boton("CANCELAR", cx - 180, 430, 360, 56, fuentes["boton"])

    while True:
        dt = reloj.tick(60) / 1000.0
        pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if host:
                    host.cerrar()
                return "salir"

            if pantalla_actual == "ip" and evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    ip_texto = ip_texto[:-1]
                elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    pantalla_actual = "_conectar"
                elif evento.unicode and (evento.unicode.isdigit() or evento.unicode == "."):
                    if len(ip_texto) < 15:
                        ip_texto += evento.unicode

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if pantalla_actual == "elegir":
                    if b_host.fue_clickeado(pos):
                        recursos.reproducir(sonidos, "clic")
                        host = Host()
                        host.iniciar()
                        pantalla_actual = "esperando"
                    elif b_unir.fue_clickeado(pos):
                        recursos.reproducir(sonidos, "clic")
                        ip_texto = ""
                        mensaje_error = ""
                        pantalla_actual = "ip"
                    elif b_volver.fue_clickeado(pos):
                        recursos.reproducir(sonidos, "clic")
                        return "menu"

                elif pantalla_actual == "ip":
                    if b_conectar.fue_clickeado(pos):
                        pantalla_actual = "_conectar"
                    elif b_volver2.fue_clickeado(pos):
                        recursos.reproducir(sonidos, "clic")
                        pantalla_actual = "elegir"

                elif pantalla_actual == "esperando":
                    if b_cancelar.fue_clickeado(pos):
                        recursos.reproducir(sonidos, "clic")
                        host.cerrar()
                        host = None
                        pantalla_actual = "elegir"

        if pantalla_actual == "_conectar":
            recursos.reproducir(sonidos, "clic")
            cliente = Cliente(ip_texto.strip())
            try:
                cliente.conectar()
            except OSError:
                mensaje_error = "No se pudo conectar a esa IP"
                pantalla_actual = "ip"
            else:
                accion = ejecutar_partida_lan(pantalla, reloj, fuentes, sonidos,
                                              cliente=cliente)
                return accion

        if pantalla_actual == "esperando" and host is not None:
            if host.error:
                mensaje_error = host.error
                host = None
                pantalla_actual = "elegir"
            elif host.conectado:
                accion = ejecutar_partida_lan(pantalla, reloj, fuentes, sonidos,
                                              host=host)
                host = None
                return accion

        fondo.actualizar(dt)
        fondo.dibujar(pantalla)
        _texto_centrado(pantalla, fuentes["grande"], "MULTIJUGADOR LOCAL",
                        120, recursos.BLANCO)

        hover = False
        if pantalla_actual == "elegir":
            if mensaje_error:
                _texto_centrado(pantalla, fuentes["chico"], mensaje_error,
                                250, recursos.ROJO_CARTA)
            for b in (b_host, b_unir, b_volver):
                b.actualizar(pos)
                hover = hover or b.hover
                b.dibujar(pantalla)

        elif pantalla_actual == "ip":
            _texto_centrado(pantalla, fuentes["texto"],
                            "Escribe la IP del host:", 250, recursos.BLANCO)
            recursos._panel(pantalla, campo_ip, alpha=200)
            mostrado = ip_texto if ip_texto else "___.___.___.___"
            color_ip = recursos.BLANCO if ip_texto else (110, 115, 125)
            txt = fuentes["texto"].render(mostrado, True, color_ip)
            pantalla.blit(txt, txt.get_rect(center=campo_ip.center))
            if mensaje_error:
                _texto_centrado(pantalla, fuentes["chico"], mensaje_error,
                                510, recursos.ROJO_CARTA)
            for b in (b_conectar, b_volver2):
                b.actualizar(pos)
                hover = hover or b.hover
                b.dibujar(pantalla)

        elif pantalla_actual == "esperando":
            _texto_centrado(pantalla, fuentes["texto"],
                            "Esperando a que se conecte un jugador...",
                            280, recursos.BLANCO)
            _texto_centrado(pantalla, fuentes["chico"],
                            "Tu IP: %s    (puerto %d)" % (_ip_local(), config.PUERTO),
                            330, recursos.DORADO)
            b_cancelar.actualizar(pos)
            hover = b_cancelar.hover
            b_cancelar.dibujar(pantalla)

        recursos.cursor_mano(hover)
        pygame.display.flip()
