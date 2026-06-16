import pygame
import socket
import threading
from game_logic import determinar_ganador
pygame.init()
ANCHO = 800
ALTO = 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Servidor - Piedra, Papel o Tijera")
BLANCO = (255, 255, 255)
NEGRO = (20, 20, 20)
AZUL = (45, 105, 180)
AZUL_OSCURO = (25, 55, 110)
CELESTE = (180, 220, 255)
GRIS = (230, 230, 230)
ROJO = (190, 60, 60)
fuente_titulo = pygame.font.SysFont("Times New Roman", 42, bold=True)
fuente_texto = pygame.font.SysFont("Times New Roman", 24)
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
HOST = "0.0.0.0"
PUERTO = 5000
servidor_socket = None
cliente_socket = None
conectado = False
ronda_en_proceso = False
mensaje = "Esperando conexión del cliente..."
resultado_texto = "Cuando el cliente se conecte, elige una jugada."
jugada_servidor = ""
jugada_cliente = ""
puntaje_servidor = 0
puntaje_cliente = 0
empates = 0
def enviar_mensaje(socket_destino, mensaje):
    socket_destino.send((mensaje + "\n").encode())
def recibir_mensaje(socket_origen):
    datos = ""
    while True:
        parte = socket_origen.recv(1).decode()
        if parte == "":
            return ""
        if parte == "\n":
            break
        datos = datos + parte
    return datos
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
    pygame.draw.rect(ventana, AZUL_OSCURO, rectangulo.inflate(20, 20), 3, border_radius=18)
    ventana.blit(imagen, rectangulo)
    texto = fuente_texto.render(nombre, True, NEGRO)
    texto_x = rectangulo.x + (rectangulo.width - texto.get_width()) // 2
    ventana.blit(texto, (texto_x, rectangulo.y + 130))
def esperar_cliente():
    global servidor_socket, cliente_socket, conectado, mensaje
    try:
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor_socket.bind((HOST, PUERTO))
        servidor_socket.listen(1)
        cliente_socket, direccion = servidor_socket.accept()
        conectado = True
        mensaje = "Cliente conectado desde: " + str(direccion[0])
    except:
        mensaje = "Error al iniciar el servidor."
def procesar_ronda(eleccion):
    global jugada_servidor, jugada_cliente, resultado_texto
    global puntaje_servidor, puntaje_cliente, empates
    global ronda_en_proceso, mensaje
    try:
        ronda_en_proceso = True
        jugada_servidor = eleccion
        jugada_cliente = ""
        resultado_texto = "Esperando jugada del cliente..."
        enviar_mensaje(cliente_socket, "TURNO")
        mensaje_cliente = recibir_mensaje(cliente_socket)
        if mensaje_cliente == "":
            mensaje = "Cliente desconectado."
            conectado = False
            ronda_en_proceso = False
            return
        if mensaje_cliente.startswith("CLIENTE:"):
            jugada_cliente = mensaje_cliente.replace("CLIENTE:", "")
        resultado = determinar_ganador(jugada_servidor, jugada_cliente)
        if resultado == "Gana Jugador 1":
            resultado_servidor = "Ganaste esta ronda"
            resultado_cliente = "Perdiste esta ronda"
            puntaje_servidor = puntaje_servidor + 1
        elif resultado == "Gana Jugador 2":
            resultado_servidor = "Perdiste esta ronda"
            resultado_cliente = "Ganaste esta ronda"
            puntaje_cliente = puntaje_cliente + 1
        else:
            resultado_servidor = "Empate"
            resultado_cliente = "Empate"
            empates = empates + 1
        resultado_texto = resultado_servidor
        enviar_mensaje(cliente_socket, "RESULTADO:" + resultado_cliente + "|SERVIDOR:" + jugada_servidor)
        ronda_en_proceso = False
    except:
        mensaje = "Error de conexión con el cliente."
        ronda_en_proceso = False
def jugar_servidor(eleccion):
    global resultado_texto
    if not conectado:
        resultado_texto = "Todavía no hay cliente conectado."
        return
    if ronda_en_proceso:
        resultado_texto = "Espera a que termine la ronda actual."
        return
    hilo_ronda = threading.Thread(target=procesar_ronda, args=(eleccion,))
    hilo_ronda.daemon = True
    hilo_ronda.start()
hilo = threading.Thread(target=esperar_cliente)
hilo.daemon = True
hilo.start()
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if rect_piedra.collidepoint(evento.pos):
                jugar_servidor("piedra")
            elif rect_papel.collidepoint(evento.pos):
                jugar_servidor("papel")
            elif rect_tijera.collidepoint(evento.pos):
                jugar_servidor("tijera")
            elif boton_salir.collidepoint(evento.pos):
                ejecutando = False
    ventana.fill(CELESTE)
    dibujar_texto_centrado("SERVIDOR - JUGADOR 1", fuente_titulo, AZUL_OSCURO, 40)
    dibujar_texto_centrado(mensaje, fuente_texto, NEGRO, 105)
    marcador = "Servidor: " + str(puntaje_servidor) + "   |   Cliente: " + str(puntaje_cliente) + "   |   Empates: " + str(empates)
    dibujar_texto_centrado(marcador, fuente_texto, NEGRO, 150)
    dibujar_texto_centrado("Elige tu jugada:", fuente_texto, NEGRO, 190)
    dibujar_opcion(imagen_piedra, rect_piedra, "Piedra")
    dibujar_opcion(imagen_papel, rect_papel, "Papel")
    dibujar_opcion(imagen_tijera, rect_tijera, "Tijera")
    dibujar_texto_centrado("Servidor eligió: " + jugada_servidor, fuente_texto, NEGRO, 420)
    dibujar_texto_centrado("Cliente eligió: " + jugada_cliente, fuente_texto, NEGRO, 455)
    dibujar_texto_centrado(resultado_texto, fuente_texto, AZUL_OSCURO, 490)
    dibujar_boton(boton_salir, "Salir", ROJO)
    pygame.display.update()
try:
    if cliente_socket:
        cliente_socket.close()
    if servidor_socket:
        servidor_socket.close()
except:
    pass
pygame.quit()