#game_logic.py
import random
import pygame

ANCHO, ALTO = 900, 600


#------------------------- PARTÍCULAS -------------------------

def crear_particula(x, y, color):
    return {
        'x': x,
        'y': y,
        'color': color,
        'vx': random.uniform(-1, 1),
        'vy': random.uniform(1, 3),
        'vida': random.randint(15, 30),
        'radio': random.randint(2, 4)
    }

def actualizar_particula(p):
    p['x'] += p['vx']
    p['y'] += p['vy']
    p['vida'] -= 1
    if p['radio'] > 0.1:
        p['radio'] -= 0.05

def dibujar_particula(p, superficie):
    if p['vida'] > 0 and p['radio'] > 0:
        pygame.draw.circle(superficie, p['color'], (int(p['x']), int(p['y'])), int(p['radio']))


#------------------------- OBSTÁCULOS -------------------------

def crear_obstaculo(carril):
    if carril == 1:
        color = (240, 80, 20)          # naranja
        color_osc = (180, 40, 0)       # versión más oscura
    else:
        color = (60, 80, 220)          # azul
        color_osc = (30, 40, 150)      # versión más oscura

    # Posición aleatoria dentro del carril correspondiente
    if carril == 1:
        x = random.randint(183, 396)
    else:
        x = random.randint(458, 679)

    return {
        'x': x,
        'y': -90,
        'w': 44,               
        'h': 80,              
        'color': color,
        'color_osc': color_osc,
        'carril': carril,      # conservamos el carril para la puntuación
        'vivo': True,          # los obstáculos siempre están "vivos" hasta que salen
        'particulas': [],      # no explotan, pero mantenemos la lista vacía
        'vel_base': 0,         # no se usa, pero para compatibilidad
        'vel': 0,
        'limite_izq': 0,
        'limite_der': 0
    }

def mover_obstaculo(obs, velocidad):
    obs['y'] += velocidad

def fuera_obstaculo(obs):
    return obs['y'] > ALTO

def rect_obstaculo(obs):
    return pygame.Rect(obs['x'], obs['y'], obs['w'], obs['h'])


#------------------------- COCHES -----------------------------

def crear_carro(x, y, color, color_osc, limite_izq, limite_der):
    return {
        'x': x,
        'y': y,
        'w': 46,
        'h': 84,
        'color': color,
        'color_osc': color_osc,
        'limite_izq': limite_izq,
        'limite_der': limite_der,
        'vel': 5,               # velocidad fija
        'vivo': True,
        'particulas': []
    }

def mover_carro(carro, direccion):
    carro['x'] += direccion * carro['vel']
    if carro['x'] < carro['limite_izq']:
        carro['x'] = carro['limite_izq']
    if carro['x'] + carro['w'] > carro['limite_der']:
        carro['x'] = carro['limite_der'] - carro['w']

def explotar_carro(carro):
    for _ in range(30):
        carro['particulas'].append(crear_particula(
            carro['x'] + carro['w'] // 2,
            carro['y'] + carro['h'] // 2,
            (255, random.randint(50, 150), 0)
        ))

def actualizar_particulas_carro(carro):
    for p in carro['particulas'][:]:
        actualizar_particula(p)
        if p['vida'] <= 0:
            carro['particulas'].remove(p)

def dibujar_carro(carro, superficie):
    if not carro['vivo']:
        for p in carro['particulas']:
            dibujar_particula(p, superficie)
        return

    x, y, w, h = int(carro['x']), int(carro['y']), carro['w'], carro['h']
    color = carro['color']
    color_osc = carro['color_osc']

    # Sombra
    pygame.draw.ellipse(superficie, (10, 10, 10, 100), (x - 2, y + h - 8, w + 4, 16))

    # Llantas
    llanta_color = (20, 20, 20)
    llanta_w, llanta_h = 10, 20
    pygame.draw.rect(superficie, llanta_color, (x - 6, y + h - 24, llanta_w, llanta_h), border_radius=3)
    pygame.draw.rect(superficie, llanta_color, (x + w - 4, y + h - 24, llanta_w, llanta_h), border_radius=3)
    pygame.draw.rect(superficie, llanta_color, (x - 6, y + 6, llanta_w, llanta_h), border_radius=3)
    pygame.draw.rect(superficie, llanta_color, (x + w - 4, y + 6, llanta_w, llanta_h), border_radius=3)

    # Carrocería
    puntos = [
        (x + 4, y), (x + w - 4, y), (x + w - 2, y + 10), (x + w, y + 25),
        (x + w, y + h - 5), (x + w - 2, y + h), (x + 2, y + h), (x, y + h - 5),
        (x, y + 25), (x + 2, y + 10)
    ]
    pygame.draw.polygon(superficie, color, puntos)
    pygame.draw.polygon(superficie, color_osc, puntos, 2)

    # Techo
    pygame.draw.polygon(superficie, color_osc, [
        (x + 6, y + 20), (x + w - 6, y + 20), (x + w - 8, y + 45), (x + 8, y + 45)
    ])
    # Ventanas
    pygame.draw.polygon(superficie, (180, 220, 255), [
        (x + 8, y + 22), (x + w - 8, y + 22), (x + w - 10, y + 42), (x + 10, y + 42)
    ])

    # Faros delanteros
    pygame.draw.circle(superficie, (255, 255, 200), (x + 5, y + 8), 6)
    pygame.draw.circle(superficie, (255, 255, 200), (x + w - 5, y + 8), 6)
    # Pilotos traseros
    pygame.draw.circle(superficie, (255, 60, 60), (x + 6, y + h - 8), 5)
    pygame.draw.circle(superficie, (255, 60, 60), (x + w - 6, y + h - 8), 5)

    # Spoiler
    pygame.draw.rect(superficie, (30, 30, 30), (x - 2, y + h - 12, w + 4, 6), border_radius=2)

def rect_carro(carro):
    if not carro['vivo']:
        return pygame.Rect(-1000, -1000, 0, 0)
    return pygame.Rect(carro['x'], carro['y'], carro['w'], carro['h'])