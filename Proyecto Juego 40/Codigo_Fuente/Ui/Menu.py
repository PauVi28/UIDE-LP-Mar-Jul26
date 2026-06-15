import math

import pygame

from ui import recursos


def _dibujar_texto_borde(pantalla, fuente, texto, centro, color, borde):

    base = fuente.render(texto, True, borde)
    cx, cy = centro
    for dx in (-4, -2, 0, 2, 4):
        for dy in (-4, -2, 0, 2, 4):
            pantalla.blit(base, base.get_rect(center=(cx + dx, cy + dy)))
    frente = fuente.render(texto, True, color)
    pantalla.blit(frente, frente.get_rect(center=centro))


def _superficie_as(fuentes):

    w, h = 120, 170
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    rect = surf.get_rect()
    pygame.draw.rect(surf, recursos.CREMA, rect, border_radius=12)
    pygame.draw.rect(surf, (70, 70, 80), rect, width=3, border_radius=12)
    color = (25, 25, 30)
    txt = fuentes["grande"].render("A", True, color)
    surf.blit(txt, (10, 4))
    recursos.dibujar_simbolo(surf, "espadas", w // 2, h // 2 + 6, 34, color)
    chico = fuentes["texto"].render("A", True, color)
    chico = pygame.transform.rotate(chico, 180)
    surf.blit(chico, (w - chico.get_width() - 10, h - chico.get_height() - 6))
    return surf


def _dibujar_logo(pantalla, fuentes, cx, cy):
    f = fuentes["titulo"]
    _dibujar_texto_borde(pantalla, f, "4", (cx - 150, cy), recursos.BLANCO, (16, 18, 24))
    _dibujar_texto_borde(pantalla, f, "0", (cx + 150, cy), recursos.BLANCO, (16, 18, 24))
    carta = _superficie_as(fuentes)
    carta = pygame.transform.rotozoom(carta, 7, 1.0)
    pantalla.blit(carta, carta.get_rect(center=(cx, cy + 4)))


def _dibujar_jokers(pantalla, fuentes, ancho):

    base_x = ancho - 230
    base_y = 40
    angulos = [-16, -2, 12]
    colores = [(40, 120, 70), (90, 90, 100), (210, 70, 60)]
    for i, ang in enumerate(angulos):
        w, h = 110, 150
        carta = pygame.Surface((w, h), pygame.SRCALPHA)
        r = carta.get_rect()
        pygame.draw.rect(carta, recursos.CREMA, r, border_radius=10)
        pygame.draw.rect(carta, (70, 70, 80), r, width=3, border_radius=10)
 
        letras = fuentes["chico"].render("JOKER", True, (40, 40, 50))
        letras = pygame.transform.rotate(letras, 90)
        carta.blit(letras, (8, h // 2 - letras.get_height() // 2))

        cx, cy = w // 2 + 6, h // 2
        col = colores[i]
        pygame.draw.polygon(carta, col, [(cx, cy - 34), (cx - 20, cy + 6), (cx + 20, cy + 6)])
        pygame.draw.circle(carta, recursos.DORADO, (cx - 20, cy + 6), 5)
        pygame.draw.circle(carta, recursos.DORADO, (cx + 20, cy + 6), 5)
        pygame.draw.circle(carta, recursos.DORADO, (cx, cy - 34), 5)
        pygame.draw.circle(carta, (245, 230, 220), (cx, cy + 22), 14) 
        carta = pygame.transform.rotozoom(carta, ang, 1.0)
        pantalla.blit(carta, (base_x + i * 26, base_y + abs(ang)))


def ejecutar_menu(pantalla, reloj, fuentes, sonidos):
    ancho, alto = pantalla.get_size()
    fondo = recursos.Fondo(ancho, alto)
    cx = ancho // 2

    botones = [
        recursos.Boton("JUGAR", cx - 180, 330, 360, 56, fuentes["boton"]),
        recursos.Boton("MULTIJUGADOR LOCAL", cx - 180, 402, 360, 56, fuentes["boton"]),
        recursos.Boton("SALIR", cx - 180, 474, 360, 56, fuentes["boton"]),
    ]
    acciones = ["jugar", "multijugador", "salir"]

    while True:
        dt = reloj.tick(60) / 1000.0
        pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for boton, accion in zip(botones, acciones):
                    if boton.fue_clickeado(pos):
                        recursos.reproducir(sonidos, "clic")
                        return accion

   
        fondo.actualizar(dt)
        fondo.dibujar(pantalla)
        _dibujar_jokers(pantalla, fuentes, ancho)
        _dibujar_logo(pantalla, fuentes, cx, 170)

        hay_hover = False
        for boton in botones:
            boton.actualizar(pos)
            hay_hover = hay_hover or boton.hover
            boton.dibujar(pantalla)
        recursos.cursor_mano(hay_hover)

        pygame.display.flip()
