import pygame
import random
from game_logic import determinar_ganador
pygame.init()
# Tamaño de la ventana
ANCHO = 700
ALTO = 450
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Piedra, Papel o Tijera")
# Colores para pygame
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (60, 120, 200)
GRIS = (220, 220, 220)
# Fuentes para pygame
fuente_titulo = pygame.font.SysFont("Times New Roman", 36)
fuente_texto = pygame.font.SysFont("Times New Roman", 24)
# Opciones del juego
opciones = ["piedra", "papel", "tijera"]
# Textos iniciales
texto_jugador = ""
texto_computadora = ""
texto_resultado = "Elige una opción para jugar"
# Botones
boton_piedra = pygame.Rect(80, 170, 150, 60)
boton_papel = pygame.Rect(275, 170, 150, 60)
boton_tijera = pygame.Rect(470, 170, 150, 60)
def dibujar_texto(texto, fuente, color, x, y):
    imagen = fuente.render(texto, True, color)
    ventana.blit(imagen, (x, y))
def dibujar_boton(rectangulo, texto):
    pygame.draw.rect(ventana, AZUL, rectangulo)
    pygame.draw.rect(ventana, NEGRO, rectangulo, 2)
    texto_boton = fuente_texto.render(texto, True, BLANCO)
    texto_x = rectangulo.x + (rectangulo.width - texto_boton.get_width()) // 2
    texto_y = rectangulo.y + (rectangulo.height - texto_boton.get_height()) // 2
    ventana.blit(texto_boton, (texto_x, texto_y))
def jugar(eleccion_jugador):
    global texto_jugador, texto_computadora, texto_resultado
    eleccion_computadora = random.choice(opciones)
    resultado = determinar_ganador(eleccion_jugador, eleccion_computadora)
    texto_jugador = "Tú elegiste: " + eleccion_jugador
    texto_computadora = "Computadora eligió: " + eleccion_computadora
    if resultado == "Gana Jugador 1":
        texto_resultado = "Resultado: Ganaste"
    elif resultado == "Gana Jugador 2":
        texto_resultado = "Resultado: Perdiste"
    else:
        texto_resultado = "Resultado: Empate"
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_piedra.collidepoint(evento.pos):
                jugar("piedra")
            elif boton_papel.collidepoint(evento.pos):
                jugar("papel")
            elif boton_tijera.collidepoint(evento.pos):
                jugar("tijera")
    ventana.fill(BLANCO)
    dibujar_texto("Piedra, Papel o Tijera", fuente_titulo, NEGRO, 180, 40)
    dibujar_texto("Selecciona tu jugada:", fuente_texto, NEGRO, 240, 110)
    dibujar_boton(boton_piedra, "Piedra")
    dibujar_boton(boton_papel, "Papel")
    dibujar_boton(boton_tijera, "Tijera")
    dibujar_texto(texto_jugador, fuente_texto, NEGRO, 210, 270)
    dibujar_texto(texto_computadora, fuente_texto, NEGRO, 210, 310)
    dibujar_texto(texto_resultado, fuente_texto, NEGRO, 210, 360)
    pygame.display.update()
pygame.quit()