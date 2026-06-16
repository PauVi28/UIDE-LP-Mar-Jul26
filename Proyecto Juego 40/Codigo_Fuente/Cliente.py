import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pygame

from ui import recursos
from network import config
from network.cliente import Cliente
from ui.partida_lan import ejecutar_partida_lan


def main():
    if len(sys.argv) > 1:
        ip = sys.argv[1].strip()
    else:
        ip = input("IP del host: ").strip()

    print("==== Cliente del juego del 40 (modo LAN) ====")
    print("Conectando a %s:%d ..." % (ip, config.PUERTO))

    cliente = Cliente(ip)
    try:
        cliente.conectar()
    except OSError as e:
        print("No se pudo conectar al servidor:", e)
        return
    print("Conectado al servidor. Iniciando partida.")

    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        pass

    pantalla = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("40 - Cliente")
    reloj = pygame.time.Clock()
    fuentes = recursos.cargar_fuentes()
    sonidos = recursos.cargar_sonidos()

    ejecutar_partida_lan(pantalla, reloj, fuentes, sonidos, cliente=cliente)

    print("Cliente cerrado.")
    pygame.quit()


if __name__ == "__main__":
    main()
