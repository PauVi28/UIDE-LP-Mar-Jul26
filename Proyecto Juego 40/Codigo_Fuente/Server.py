import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pygame

from ui import recursos
from network import config
from multiplayer.host import Host
from ui.partida_lan import ejecutar_partida_lan


def _pantalla_espera(pantalla, reloj, fuentes, fondo, host):

    cx, cy = pantalla.get_width() // 2, pantalla.get_height() // 2
    aviso_cliente = False
    while True:
        dt = reloj.tick(60) / 1000.0
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return False

        if host.error:
            print("Error del servidor:", host.error)
            return False
        if host.conectado:
            if not aviso_cliente:
                print("Cliente conectado. Iniciando partida.")
            return True

        fondo.actualizar(dt)
        fondo.dibujar(pantalla)
        t1 = fuentes["grande"].render("SERVIDOR ACTIVO", True, recursos.BLANCO)
        pantalla.blit(t1, t1.get_rect(center=(cx, cy - 60)))
        t2 = fuentes["texto"].render("Esperando a que se conecte un jugador...",
                                     True, recursos.BLANCO)
        pantalla.blit(t2, t2.get_rect(center=(cx, cy)))
        t3 = fuentes["chico"].render("Puerto %d   (Esc para cancelar)" % config.PUERTO,
                                     True, recursos.DORADO)
        pantalla.blit(t3, t3.get_rect(center=(cx, cy + 44)))
        pygame.display.flip()


def main():
    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        pass

    pantalla = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("40 - Servidor (Host)")
    reloj = pygame.time.Clock()
    fuentes = recursos.cargar_fuentes()
    sonidos = recursos.cargar_sonidos()
    fondo = recursos.Fondo(1000, 600)

    host = Host()
    host.iniciar()
    print("==== Servidor del juego del 40 (modo LAN) ====")
    print("Escuchando en %s:%d ..." % (config.ESCUCHAR_EN, config.PUERTO))
    print("Esperando la conexion de un cliente.")

    if _pantalla_espera(pantalla, reloj, fuentes, fondo, host):
        ejecutar_partida_lan(pantalla, reloj, fuentes, sonidos, host=host)
    else:
        host.cerrar()

    print("Servidor cerrado.")
    pygame.quit()


if __name__ == "__main__":
    main()
