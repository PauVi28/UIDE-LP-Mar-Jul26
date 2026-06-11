import pygame
import random
import subprocess
import sys
import os
from game_logic import determinar_ganador
pygame.init()
ANCHO = 800
ALTO = 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Piedra, Papel o Tijera")
CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))
BLANCO = (255, 255, 255)
NEGRO = (20, 20, 20)
AZUL = (45, 105, 180)
AZUL_OSCURO = (25, 55, 110)
CELESTE = (180, 220, 255)
GRIS = (230, 230, 230)
VERDE = (40, 160, 90)
ROJO = (190, 60, 60)
AMARILLO = (240, 190, 60)
fuente_titulo = pygame.font.SysFont("Times New Roman", 44, bold=True)
fuente_subtitulo = pygame.font.SysFont("Times New Roman", 28, bold=True)
fuente_texto = pygame.font.SysFont("Times New Roman", 24)
fuente_pequena = pygame.font.SysFont("Times New Roman", 20)
opciones = ["piedra", "papel", "tijera"]
pantalla = "menu"
texto_resultado = "Elige una opción para jugar"
texto_jugador = "Jugador: -"
texto_computadora = "Computadora: -"
puntaje_jugador = 0
puntaje_computadora = 0
puntaje_empates = 0
eleccion_jugador_actual = None
eleccion_computadora_actual = None
boton_local = pygame.Rect(260, 230, 280, 65)
boton_lan = pygame.Rect(260, 320, 280, 65)
boton_servidor = pygame.Rect(260, 230, 280, 65)
boton_cliente = pygame.Rect(260, 320, 280, 65)
boton_volver = pygame.Rect(30, 530, 130, 45)
boton_reiniciar = pygame.Rect(620, 530, 140, 45)
imagen_piedra = pygame.image.load(os.path.join(CARPETA_BASE, "imagenes", "piedra.png"))
imagen_papel = pygame.image.load(os.path.join(CARPETA_BASE, "imagenes", "papel.png"))
imagen_tijera = pygame.image.load(os.path.join(CARPETA_BASE, "imagenes", "tijera.png"))
imagen_piedra = pygame.transform.scale(imagen_piedra, (120, 120))
imagen_papel = pygame.transform.scale(imagen_papel, (120, 120))
imagen_tijera = pygame.transform.scale(imagen_tijera, (120, 120))
imagenes_juego = {
    "piedra": imagen_piedra,
    "papel": imagen_papel,
    "tijera": imagen_tijera}
usar_fondo = False
try:
    fondo = pygame.image.load(os.path.join(CARPETA_BASE, "imagenes", "fondo.png"))
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    usar_fondo = True
except:
    usar_fondo = False
rect_piedra = imagen_piedra.get_rect(topleft=(120, 210))
rect_papel = imagen_papel.get_rect(topleft=(340, 210))
rect_tijera = imagen_tijera.get_rect(topleft=(560, 210))
def abrir_servidor():
    ruta_servidor = os.path.join(CARPETA_BASE, "servidor_grafico.py")
    subprocess.Popen([sys.executable, ruta_servidor], cwd=CARPETA_BASE)
def abrir_cliente():
    ruta_cliente = os.path.join(CARPETA_BASE, "cliente_grafico.py")
    subprocess.Popen([sys.executable, ruta_cliente], cwd=CARPETA_BASE)
def dibujar_fondo():
    if usar_fondo:
        ventana.blit(fondo, (0, 0))
    else:
        ventana.fill(CELESTE)
def dibujar_texto(texto, fuente, color, x, y):
    imagen = fuente.render(texto, True, color)
    ventana.blit(imagen, (x, y))
def dibujar_texto_centrado(texto, fuente, color, y):
    imagen = fuente.render(texto, True, color)
    x = (ANCHO - imagen.get_width()) // 2
    ventana.blit(imagen, (x, y))
def dibujar_panel(x, y, ancho, alto):
    panel = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(ventana, BLANCO, panel, border_radius=20)
    pygame.draw.rect(ventana, AZUL_OSCURO, panel, 3, border_radius=20)
def dibujar_boton(rectangulo, texto, color):
    pygame.draw.rect(ventana, color, rectangulo, border_radius=15)
    pygame.draw.rect(ventana, NEGRO, rectangulo, 2, border_radius=15)
    texto_boton = fuente_texto.render(texto, True, BLANCO)
    texto_x = rectangulo.x + (rectangulo.width - texto_boton.get_width()) // 2
    texto_y = rectangulo.y + (rectangulo.height - texto_boton.get_height()) // 2
    ventana.blit(texto_boton, (texto_x, texto_y))
def dibujar_opcion(imagen, rectangulo, nombre):
    pygame.draw.rect(ventana, GRIS, rectangulo.inflate(20, 20), border_radius=18)
    pygame.draw.rect(ventana, AZUL_OSCURO, rectangulo.inflate(20, 20), 3, border_radius=18)
    ventana.blit(imagen, rectangulo)
    texto = fuente_texto.render(nombre, True, NEGRO)
    texto_x = rectangulo.x + (rectangulo.width - texto.get_width()) // 2
    ventana.blit(texto, (texto_x, rectangulo.y + 130))
def dibujar_marcador():
    marcador = ("Jugador: " + str(puntaje_jugador) + "   |   Computadora: " + str(puntaje_computadora) +"   |   Empates: " + str(puntaje_empates))
    dibujar_texto_centrado(marcador, fuente_texto, NEGRO, 120)
def dibujar_elecciones():
    if eleccion_jugador_actual is not None:
        dibujar_texto("Tu elección", fuente_pequena, NEGRO, 155, 365)
        imagen = pygame.transform.scale(imagenes_juego[eleccion_jugador_actual], (80, 80))
        ventana.blit(imagen, (170, 395))
    if eleccion_computadora_actual is not None:
        dibujar_texto("Computadora", fuente_pequena, NEGRO, 555, 365)
        imagen = pygame.transform.scale(imagenes_juego[eleccion_computadora_actual], (80, 80))
        ventana.blit(imagen, (575, 395))
def jugar_local(eleccion_jugador):
    global texto_resultado, texto_jugador, texto_computadora
    global puntaje_jugador, puntaje_computadora, puntaje_empates
    global eleccion_jugador_actual, eleccion_computadora_actual
    eleccion_computadora = random.choice(opciones)
    eleccion_jugador_actual = eleccion_jugador
    eleccion_computadora_actual = eleccion_computadora
    resultado = determinar_ganador(eleccion_jugador, eleccion_computadora)
    texto_jugador = "Jugador: " + eleccion_jugador
    texto_computadora = "Computadora: " + eleccion_computadora
    if resultado == "Gana Jugador 1":
        texto_resultado = "¡Ganaste esta ronda!"
        puntaje_jugador = puntaje_jugador + 1
    elif resultado == "Gana Jugador 2":
        texto_resultado = "Perdiste esta ronda"
        puntaje_computadora = puntaje_computadora + 1
    else:
        texto_resultado = "Empate"
        puntaje_empates = puntaje_empates + 1
def reiniciar_puntaje():
    global puntaje_jugador, puntaje_computadora, puntaje_empates
    global texto_resultado, texto_jugador, texto_computadora
    global eleccion_jugador_actual, eleccion_computadora_actual

    puntaje_jugador = 0
    puntaje_computadora = 0
    puntaje_empates = 0

    texto_resultado = "Elige una opción para jugar"
    texto_jugador = "Jugador: -"
    texto_computadora = "Computadora: -"

    eleccion_jugador_actual = None
    eleccion_computadora_actual = None
def dibujar_menu():
    dibujar_panel(110, 100, 580, 350)
    dibujar_texto_centrado("PIEDRA, PAPEL O TIJERA", fuente_titulo, AZUL_OSCURO, 115)
    dibujar_texto_centrado("Proyecto Integrador", fuente_subtitulo, NEGRO, 170)
    dibujar_boton(boton_local, "Modo local", AZUL)
    dibujar_boton(boton_lan, "Multijugador LAN", VERDE)
    dibujar_texto_centrado("EQUIPO 1 GUDIÑO, HURTADO, NARANJO", fuente_pequena, NEGRO, 420)
def dibujar_juego_local():
    dibujar_panel(90, 40, 620, 480)
    dibujar_texto_centrado("MODO LOCAL", fuente_titulo, AZUL_OSCURO, 50)
    dibujar_texto_centrado("Haz clic en una imagen para jugar", fuente_texto, NEGRO, 95)
    dibujar_marcador()
    dibujar_opcion(imagen_piedra, rect_piedra, "Piedra")
    dibujar_opcion(imagen_papel, rect_papel, "Papel")
    dibujar_opcion(imagen_tijera, rect_tijera, "Tijera")
    dibujar_elecciones()
    dibujar_texto_centrado(texto_resultado, fuente_subtitulo, AZUL_OSCURO, 485)
    dibujar_boton(boton_volver, "Volver", ROJO)
    dibujar_boton(boton_reiniciar, "Reiniciar", AMARILLO)
def dibujar_lan():
    dibujar_panel(75, 90, 650, 380)
    dibujar_texto_centrado("MODO MULTIJUGADOR LAN", fuente_titulo, AZUL_OSCURO, 120)
    dibujar_texto_centrado("Selecciona el rol de esta máquina", fuente_texto, NEGRO, 180)
    dibujar_boton(boton_servidor, "Ser servidor", AZUL)
    dibujar_boton(boton_cliente, "Ser cliente", VERDE)
    dibujar_texto_centrado("Servidor = Jugador 1", fuente_pequena, NEGRO, 410)
    dibujar_texto_centrado("Cliente = Jugador 2", fuente_pequena, NEGRO, 440)
    dibujar_boton(boton_volver, "Volver", ROJO)


ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if pantalla == "menu":
                if boton_local.collidepoint(evento.pos):
                    pantalla = "local"
                elif boton_lan.collidepoint(evento.pos):
                    pantalla = "lan"
            elif pantalla == "local":
                if rect_piedra.collidepoint(evento.pos):
                    jugar_local("piedra")
                elif rect_papel.collidepoint(evento.pos):
                    jugar_local("papel")
                elif rect_tijera.collidepoint(evento.pos):
                    jugar_local("tijera")
                elif boton_volver.collidepoint(evento.pos):
                    pantalla = "menu"
                elif boton_reiniciar.collidepoint(evento.pos):
                    reiniciar_puntaje()
            elif pantalla == "lan":
                if boton_servidor.collidepoint(evento.pos):
                    abrir_servidor()
                elif boton_cliente.collidepoint(evento.pos):
                    abrir_cliente()
                elif boton_volver.collidepoint(evento.pos):
                    pantalla = "menu"
    dibujar_fondo()
    if pantalla == "menu":
        dibujar_menu()
    elif pantalla == "local":
        dibujar_juego_local()
    elif pantalla == "lan":
        dibujar_lan()
    pygame.display.update()
pygame.quit()