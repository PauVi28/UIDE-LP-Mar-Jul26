import pygame
import socket
import threading
pygame.init()
ANCHO = 800
ALTO = 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Cliente - Piedra, Papel o Tijera")
BLANCO = (255, 255, 255)
NEGRO = (20, 20, 20)
VERDE = (40, 160, 90)
VERDE_OSCURO = (20, 90, 50)
CELESTE = (180, 220, 255)
GRIS = (230, 230, 230)
ROJO = (190, 60, 60)
fuente_titulo = pygame.font.SysFont("Times New Roman", 42, bold=True)
fuente_texto = pygame.font.SysFont("Times New Roman", 24)
HOST = "127.0.0.1"
PUERTO = 5000
cliente_socket = None
conectado = False
puede_jugar = False
mensaje = "Conectando al servidor..."
resultado_texto = "Espera la jugada del servidor."
jugada_servidor = ""
jugada_cliente = ""
imagen_piedra = pygame.image.load("imagenes/piedra.png")
imagen_papel = pygame.image.load("imagenes/papel.png")
imagen_tijera = pygame.image.load("imagenes/tijera.png")
imagen_piedra = pygame.transform.scale(imagen_piedra, (120, 120))
imagen_papel = pygame.transform.scale(imagen_papel, (120, 120))
imagen_tijera = pygame.transform.scale(imagen_tijera, (120, 120))
rect_piedra = imagen_piedra.get_rect(topleft=(120, 230))
rect_papel = imagen_papel.get_rect(topleft=(340, 230))
rect_tijera = imagen_tijera.get_rect(topleft=(560, 230))
boton_salir = pygame.Rect(30, 530, 120, 45)
def dibujar_texto(texto, fuente, color, x, y):
    imagen = fuente.render(texto, True, color)
    ventana.blit(imagen, (x, y))
def dibujar_texto_centrado(texto, fuente, color, y):
    imagen = fuente.render(texto, True, color)
    x = (ANCHO - imagen.get_width()) // 2
    ventana.blit(imagen, (x, y))
def dibujar_boton(rectangulo, texto, color):
    pygame.draw.rect(ventana, color, rectangulo, border_radius=15)
    pygame.draw.rect(ventana, NEGRO, rectangulo, 2, border_radius=15)
    texto_boton = fuente_texto.render(texto, True, BLANCO)
    texto_x = rectangulo.x + (rectangulo.width - texto_boton.get_width()) // 2
    texto_y = rectangulo.y + (rectangulo.height - texto_boton.get_height()) // 2
    ventana.blit(texto_boton, (texto_x, texto_y))
def dibujar_opcion(imagen, rectangulo, nombre):
    pygame.draw.rect(ventana, GRIS, rectangulo.inflate(20, 20), border_radius=18)
    pygame.draw.rect(ventana, VERDE_OSCURO, rectangulo.inflate(20, 20), 3, border_radius=18)
    ventana.blit(imagen, rectangulo)
    texto = fuente_texto.render(nombre, True, NEGRO)
    texto_x = rectangulo.x + (rectangulo.width - texto.get_width()) // 2
    ventana.blit(texto, (texto_x, rectangulo.y + 130))
def conectar_servidor():
    global cliente_socket, conectado, mensaje, jugada_servidor, puede_jugar, resultado_texto
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((HOST, PUERTO))
        conectado = True
        mensaje = "Conectado al servidor"
        resultado_texto = "Esperando jugada del servidor..."
        while True:
            jugada_servidor = cliente_socket.recv(1024).decode()

            if jugada_servidor == "":
                mensaje = "Servidor desconectado"
                break
            puede_jugar = True
            resultado_texto = "Servidor ya eligió. Ahora elige tú."
    except:
        mensaje = "No se pudo conectar al servidor."
def jugar_cliente(eleccion):
    global jugada_cliente, resultado_texto, puede_jugar
    if not conectado:
        resultado_texto = "No estás conectado al servidor."
        return
    if not puede_jugar:
        resultado_texto = "Espera la jugada del servidor."
        return
    jugada_cliente = eleccion
    cliente_socket.send(jugada_cliente.encode())
    resultado_texto = cliente_socket.recv(1024).decode()
    puede_jugar = False
hilo = threading.Thread(target=conectar_servidor)
hilo.daemon = True
hilo.start()
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if rect_piedra.collidepoint(evento.pos):
                jugar_cliente("piedra")
            elif rect_papel.collidepoint(evento.pos):
                jugar_cliente("papel")
            elif rect_tijera.collidepoint(evento.pos):
                jugar_cliente("tijera")
            elif boton_salir.collidepoint(evento.pos):
                ejecutando = False
    ventana.fill(CELESTE)
    dibujar_texto_centrado("CLIENTE - JUGADOR 2", fuente_titulo, VERDE_OSCURO, 40)
    dibujar_texto_centrado(mensaje, fuente_texto, NEGRO, 105)
    dibujar_texto_centrado("Elige tu jugada cuando el servidor haya elegido", fuente_texto, NEGRO, 160)
    dibujar_opcion(imagen_piedra, rect_piedra, "Piedra")
    dibujar_opcion(imagen_papel, rect_papel, "Papel")
    dibujar_opcion(imagen_tijera, rect_tijera, "Tijera")
    dibujar_texto_centrado("Servidor eligió: " + jugada_servidor, fuente_texto, NEGRO, 420)
    dibujar_texto_centrado("Cliente eligió: " + jugada_cliente, fuente_texto, NEGRO, 455)
    dibujar_texto_centrado(resultado_texto, fuente_texto, VERDE_OSCURO, 490)
    dibujar_boton(boton_salir, "Salir", ROJO)
    pygame.display.update()
try:
    if cliente_socket:
        cliente_socket.close()
except:
    pass
pygame.quit()