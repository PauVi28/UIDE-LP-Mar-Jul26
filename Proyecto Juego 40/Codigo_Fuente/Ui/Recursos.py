import os
import math
import random

import pygame

from logica import mazo
from logica import reglas40

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_SONIDOS = os.path.join(RAIZ, "assets", "sonidos")

BLANCO = (236, 238, 243)
NEGRO = (18, 18, 22)
CREMA = (248, 248, 250)
BORDE_CLARO = (212, 216, 222)
DORADO = (250, 205, 80)
ROJO_CARTA = (200, 35, 35)
GRIS_PANEL = (24, 26, 32)
ROJO = (175, 38, 42)
TEAL = (22, 145, 145)

PALOS_ROJOS = ("oros", "copas")

def cargar_fuentes():
    pygame.font.init()
    return {
        "titulo": pygame.font.SysFont("arialblack,arial,dejavusans", 130, bold=True),
        "boton": pygame.font.SysFont("arial,dejavusans", 28, bold=True),
        "texto": pygame.font.SysFont("arial,dejavusans", 22, bold=True),
        "chico": pygame.font.SysFont("arial,dejavusans", 18, bold=True),
        "carta": pygame.font.SysFont("arial,dejavusans", 22, bold=True),
        "grande": pygame.font.SysFont("arialblack,arial,dejavusans", 60, bold=True),
    }


def cargar_sonidos():

    sonidos = {}
    if pygame.mixer.get_init() is None:
        return sonidos
    nombres = ["clic", "carta", "captura", "caida", "limpia", "ganar", "repartir"]
    for nombre in nombres:
        ruta = os.path.join(DIR_SONIDOS, nombre + ".wav")
        if os.path.exists(ruta):
            try:
                sonidos[nombre] = pygame.mixer.Sound(ruta)
            except pygame.error:
                pass
    return sonidos


def reproducir(sonidos, nombre):
    if nombre in sonidos:
        sonidos[nombre].play()


def sonido_de_evento(sonidos, evento):
 
    if evento in ("captura", "caida", "limpia", "carta"):
        reproducir(sonidos, evento)

def cursor_mano(activo):
    try:
        if activo:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    except Exception:
        pass  

def dibujar_simbolo(pantalla, palo, cx, cy, tam, color):
    if palo == "oros":           
        puntos = [(cx, cy - tam), (cx + tam * 0.72, cy),
                  (cx, cy + tam), (cx - tam * 0.72, cy)]
        pygame.draw.polygon(pantalla, color, puntos)
    elif palo == "copas":         
        r = tam * 0.5
        pygame.draw.circle(pantalla, color, (int(cx - r * 0.6), int(cy - r * 0.35)), int(r))
        pygame.draw.circle(pantalla, color, (int(cx + r * 0.6), int(cy - r * 0.35)), int(r))
        pygame.draw.polygon(pantalla, color,
                            [(cx - tam * 0.95, cy - tam * 0.1),
                             (cx + tam * 0.95, cy - tam * 0.1),
                             (cx, cy + tam)])
    elif palo == "espadas":      
        pygame.draw.polygon(pantalla, color,
                            [(cx, cy - tam), (cx + tam * 0.85, cy + tam * 0.2),
                             (cx - tam * 0.85, cy + tam * 0.2)])
        r = tam * 0.42
        pygame.draw.circle(pantalla, color, (int(cx - r * 0.75), int(cy + tam * 0.15)), int(r))
        pygame.draw.circle(pantalla, color, (int(cx + r * 0.75), int(cy + tam * 0.15)), int(r))
        pygame.draw.polygon(pantalla, color,
                            [(cx - tam * 0.35, cy + tam * 0.85),
                             (cx + tam * 0.35, cy + tam * 0.85),
                             (cx, cy + tam * 0.45)])
    elif palo == "bastos":        
        r = tam * 0.42
        pygame.draw.circle(pantalla, color, (int(cx), int(cy - tam * 0.42)), int(r))
        pygame.draw.circle(pantalla, color, (int(cx - tam * 0.5), int(cy + tam * 0.08)), int(r))
        pygame.draw.circle(pantalla, color, (int(cx + tam * 0.5), int(cy + tam * 0.08)), int(r))
        pygame.draw.polygon(pantalla, color,
                            [(cx - tam * 0.28, cy + tam), (cx + tam * 0.28, cy + tam),
                             (cx, cy + tam * 0.3)])

def dibujar_carta(pantalla, fuentes, carta, x, y, ancho, alto, oculta=False, resaltar=False):
    rect = pygame.Rect(int(x), int(y), ancho, alto)

    if oculta:
        pygame.draw.rect(pantalla, (38, 58, 120), rect, border_radius=8)
        pygame.draw.rect(pantalla, BORDE_CLARO, rect, width=3, border_radius=8)
       
        for i in range(3):
            interno = rect.inflate(-12 - i * 8, -12 - i * 8)
            pygame.draw.rect(pantalla, (70, 95, 165), interno, width=2, border_radius=6)
        return rect

    pygame.draw.rect(pantalla, (0, 0, 0, 80), rect.move(0, 3), border_radius=8)
    pygame.draw.rect(pantalla, CREMA, rect, border_radius=8)
    color_borde = DORADO if resaltar else (70, 70, 80)
    grosor = 4 if resaltar else 2
    pygame.draw.rect(pantalla, color_borde, rect, width=grosor, border_radius=8)

    color = ROJO_CARTA if carta["palo"] in PALOS_ROJOS else (25, 25, 30)
    valor = mazo.texto_valor(carta["valor"])

    txt = fuentes["carta"].render(valor, True, color)
    pantalla.blit(txt, (rect.x + 7, rect.y + 5))
  
    dibujar_simbolo(pantalla, carta["palo"], rect.centerx, rect.centery, alto * 0.20, color)
   
    pantalla.blit(txt, (rect.right - txt.get_width() - 7, rect.bottom - txt.get_height() - 5))
    return rect
  
class Boton:
    def __init__(self, texto, x, y, ancho, alto, fuente):
        self.texto = texto
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.fuente = fuente
        self.hover = False

    def actualizar(self, pos_mouse):
        self.hover = self.rect.collidepoint(pos_mouse)

    def fue_clickeado(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)

    def dibujar(self, pantalla):
        r = self.rect
        base = (50, 56, 64) if self.hover else (30, 34, 40)
        pygame.draw.rect(pantalla, (8, 9, 12), r.move(0, 4), border_radius=12)
        pygame.draw.rect(pantalla, base, r, border_radius=12)
        pygame.draw.rect(pantalla, BORDE_CLARO, r, width=3, border_radius=12)
     
        pygame.draw.line(pantalla, (90, 96, 104),
                         (r.x + 10, r.y + 4), (r.right - 10, r.y + 4), 2)
        color_txt = DORADO if self.hover else BLANCO
        txt = self.fuente.render(self.texto, True, color_txt)
        pantalla.blit(txt, txt.get_rect(center=r.center))

def _crear_glow(radio, color):
    surf = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
    pasos = 36
    for i in range(pasos, 0, -1):
        r = int(radio * i / pasos)
        alpha = int(75 * (1 - i / pasos) ** 1.3)
        pygame.draw.circle(surf, (color[0], color[1], color[2], alpha),
                           (radio, radio), r)
    return surf


class Fondo:
    def __init__(self, ancho, alto, intensidad=1.0):
        self.ancho = ancho
        self.alto = alto
        self.intensidad = intensidad
        self.t = 0.0
        self.base = (12, 11, 16)
        colores = [ROJO, TEAL, ROJO, TEAL, (150, 30, 80), TEAL, ROJO]
        self.wisps = []
        for col in colores:
            self.wisps.append({
                "glow": _crear_glow(int(220 + random.random() * 170), col),
                "ax": random.uniform(0.18, 0.45),
                "ay": random.uniform(0.18, 0.42),
                "fx": random.uniform(0, 6.28),
                "fy": random.uniform(0, 6.28),
                "vx": random.uniform(0.04, 0.14),
                "vy": random.uniform(0.04, 0.14),
                "cx": random.uniform(0.25, 0.75),
                "cy": random.uniform(0.25, 0.75),
            })

    def actualizar(self, dt):
        self.t += dt

    def dibujar(self, pantalla):
        pantalla.fill(self.base)
        dospi = 2 * math.pi
        for w in self.wisps:
            x = (w["cx"] + w["ax"] * math.sin(self.t * w["vx"] * dospi + w["fx"])) * self.ancho
            y = (w["cy"] + w["ay"] * math.sin(self.t * w["vy"] * dospi + w["fy"])) * self.alto
            rect = w["glow"].get_rect(center=(int(x), int(y)))
            pantalla.blit(w["glow"], rect)
        if self.intensidad < 1.0:
            velo = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            velo.fill((8, 8, 12, int(170 * (1 - self.intensidad))))
            pantalla.blit(velo, (0, 0))

def vista_local(juego, yo):
    """Arma la vista desde un Game40 (host o cpu). yo = 1 (somos el jugador 1)."""
    rival_mano = juego.mano_cpu if juego.modo == "cpu" else juego.mano_jugador2
    gano = (juego.ganador == yo) if juego.ganador is not None else None
    return {
        "mesa": juego.mesa,
        "mi_mano": juego.mano_jugador,
        "rival_cantidad": len(rival_mano),
        "puntaje_mio": juego.puntaje_jugador,
        "puntaje_rival": juego.puntaje_jugador2,
        "carton_mio": len(juego.carton_jugador),
        "carton_rival": len(juego.carton_jugador2),
        "es_mi_turno": juego.turno == yo,
        "ganador": juego.ganador,
        "gane": gano,
    }


def vista_remota(estado):
    gano = (estado["ganador"] == 2) if estado["ganador"] is not None else None
    return {
        "mesa": estado["mesa"],
        "mi_mano": estado["mano_jugador2"],
        "rival_cantidad": len(estado["mano_jugador"]),
        "puntaje_mio": estado["puntaje_jugador2"],
        "puntaje_rival": estado["puntaje_jugador"],
        "carton_mio": estado["carton_jugador2"],
        "carton_rival": estado["carton_jugador"],
        "es_mi_turno": estado["turno"] == 2,
        "ganador": estado["ganador"],
        "gane": gano,
    }


def rects_mano(cantidad, ancho, alto):
   
    cw, ch = 84, 124
    sep = 16
    if cantidad == 0:
        return []
    total = cantidad * cw + (cantidad - 1) * sep
    x0 = (ancho - total) // 2
    y = alto - ch - 28
    return [pygame.Rect(x0 + i * (cw + sep), y, cw, ch) for i in range(cantidad)]


def _panel(pantalla, rect, alpha=170):
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    s.fill((GRIS_PANEL[0], GRIS_PANEL[1], GRIS_PANEL[2], alpha))
    pantalla.blit(s, rect.topleft)
    pygame.draw.rect(pantalla, BORDE_CLARO, rect, width=2, border_radius=8)


def dibujar_tablero(pantalla, fuentes, vista, pos_mouse):

    ancho, alto = pantalla.get_size()

    panel = pygame.Rect(16, 16, 250, 96)
    _panel(pantalla, panel)
    t1 = fuentes["chico"].render(
        "TU:  %d pts   (%d cartas)" % (vista["puntaje_mio"], vista["carton_mio"]),
        True, BLANCO)
    t2 = fuentes["chico"].render(
        "RIVAL:  %d pts   (%d cartas)" % (vista["puntaje_rival"], vista["carton_rival"]),
        True, BLANCO)
    t3 = fuentes["chico"].render("Meta: 40 puntos", True, (150, 155, 165))
    pantalla.blit(t1, (panel.x + 12, panel.y + 10))
    pantalla.blit(t2, (panel.x + 12, panel.y + 36))
    pantalla.blit(t3, (panel.x + 12, panel.y + 64))

    texto_turno = "TU TURNO" if vista["es_mi_turno"] else "TURNO DEL RIVAL"
    color_turno = DORADO if vista["es_mi_turno"] else (150, 155, 165)
    tt = fuentes["texto"].render(texto_turno, True, color_turno)
    pantalla.blit(tt, (ancho - tt.get_width() - 20, 24))

    cw, ch = 60, 90
    sep = 14
    cant = vista["rival_cantidad"]
    if cant > 0:
        total = cant * cw + (cant - 1) * sep
        x0 = (ancho - total) // 2
        for i in range(cant):
            dibujar_carta(pantalla, fuentes, None,
                          x0 + i * (cw + sep), 70, cw, ch, oculta=True)

    etiqueta = fuentes["chico"].render("MESA", True, (150, 155, 165))
    pantalla.blit(etiqueta, (ancho // 2 - etiqueta.get_width() // 2, 196))
    mesa = vista["mesa"]
    mw, mh = 74, 110
    msep = 14
    if mesa:
        total = len(mesa) * mw + (len(mesa) - 1) * msep
        x0 = (ancho - total) // 2
        for i, carta in enumerate(mesa):
            dibujar_carta(pantalla, fuentes, carta, x0 + i * (mw + msep), 224, mw, mh)
    else:
        vacio = fuentes["chico"].render("(vacia)", True, (90, 95, 105))
        pantalla.blit(vacio, (ancho // 2 - vacio.get_width() // 2, 270))

    rects = rects_mano(len(vista["mi_mano"]), ancho, alto)
    for i, carta in enumerate(vista["mi_mano"]):
        rect = rects[i]
        sobre = rect.collidepoint(pos_mouse) and vista["es_mi_turno"]
        
        puede = vista["es_mi_turno"] and len(reglas40.buscar_captura(mesa, carta)) > 0
        y = rect.y - 16 if sobre else rect.y
        dibujar_carta(pantalla, fuentes, carta, rect.x, y, rect.width, rect.height,
                      resaltar=(puede or sobre))
    return rects


def dibujar_fin(pantalla, fuentes, gane):
    """Muestra el cartel de fin de partida sobre un velo oscuro."""
    ancho, alto = pantalla.get_size()
    velo = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    velo.fill((0, 0, 0, 170))
    pantalla.blit(velo, (0, 0))

    texto = "GANASTE" if gane else "GANO EL RIVAL"
    color = DORADO if gane else BLANCO
    grande = fuentes["grande"].render(texto, True, color)
    pantalla.blit(grande, grande.get_rect(center=(ancho // 2, alto // 2 - 20)))
    sub = fuentes["texto"].render("Clic para volver al menu", True, (190, 195, 205))
    pantalla.blit(sub, sub.get_rect(center=(ancho // 2, alto // 2 + 40)))
