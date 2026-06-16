#client.py
import pygame
import sys
import socket
import threading
import random
import time
from game_logic import (
    crear_carro, mover_carro, explotar_carro,
    actualizar_particulas_carro, dibujar_carro, rect_carro,
    crear_obstaculo, fuera_obstaculo, rect_obstaculo,
    crear_particula, actualizar_particula, dibujar_particula, mover_obstaculo
)

pygame.init()
ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("FuriosCar2D – Local / Multijugador")
reloj = pygame.time.Clock()

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (65, 65, 65)
GRIS_CLARO = (180, 180, 180)
ROJO = (230, 30, 30)
ROJO_OSC = (150, 0, 0)
AZUL = (0, 100, 255)
AZUL_OSC = (0, 50, 160)
VERDE = (0, 220, 80)
AMARILLO = (255, 220, 0)
NARANJA = (255, 140, 0)
CELESTE = (100, 200, 255)
CYAN = (0, 255, 255)

# --- Fuente pixelada personalizada ---
try:
    fuente_pixel = pygame.font.Font("PressStart2P-Regular.ttf", 14)
    fuente_pixel_grande = pygame.font.Font("PressStart2P-Regular.ttf", 36)
    fuente_pixel_med = pygame.font.Font("PressStart2P-Regular.ttf", 20)
    fuente_pixel_peq = pygame.font.Font("PressStart2P-Regular.ttf", 12)
except:
    print("No se encontró PressStart2P-Regular.ttf, usando Arial")
    fuente_pixel = pygame.font.SysFont("Arial", 18, bold=True)
    fuente_pixel_grande = pygame.font.SysFont("Arial", 40, bold=True)
    fuente_pixel_med = pygame.font.SysFont("Arial", 24, bold=True)
    fuente_pixel_peq = pygame.font.SysFont("Arial", 16)

fuente_hud = fuente_pixel
fuente_med = fuente_pixel_med
fuente_peq = fuente_pixel_peq
fuente_grande = pygame.font.SysFont("Arial", 56, bold=True)

PISTA_IZQ, PISTA_DER, BARANDA_W = 175, 725, 22
STRIPE_SPACE = 55
PISTA_ANCHO = PISTA_DER - PISTA_IZQ
MITAD = (PISTA_IZQ + PISTA_DER) // 2
CARRIL1_IZQ, CARRIL1_DER = PISTA_IZQ + 8, MITAD - 8
CARRIL2_IZQ, CARRIL2_DER = MITAD + 8, PISTA_DER - 8
CAR_W, CAR_H = 46, 84

road_offset = 0
baranda_offset = 0
particles_fondo = []

datos_servidor = "menu,60.0,4.0,0,1,0,1,0,0,0,0,0,0,,NONE,NONE"
modo_local = False
teclas_j1 = "NONE"
mi_id = 0
estado_net = "menu"

# --- Carga de portadas ---
try:
    portada_local = pygame.image.load("portada_local.png").convert()
    portada_local = pygame.transform.scale(portada_local, (ANCHO, ALTO))
except:
    portada_local = None
try:
    portada_j1 = pygame.image.load("portadaJ1.png").convert()
    portada_j1 = pygame.transform.scale(portada_j1, (ANCHO, ALTO))
except:
    portada_j1 = None
try:
    portada_j2 = pygame.image.load("portadaJ2.png").convert()
    portada_j2 = pygame.transform.scale(portada_j2, (ANCHO, ALTO))
except:
    portada_j2 = None
try:
    portada_menu = pygame.image.load("Portadamenu.png").convert()
    portada_menu = pygame.transform.scale(portada_menu, (ANCHO, ALTO))
except:
    portada_menu = None

# Coches
j1 = crear_carro(0, ALTO - CAR_H - 30, ROJO, ROJO_OSC, CARRIL1_IZQ, CARRIL1_DER)
j2 = crear_carro(0, ALTO - CAR_H - 30, AZUL, AZUL_OSC, CARRIL2_IZQ, CARRIL2_DER)
j2['vivo'] = False

# ================= PANTALLA DE SELECCIÓN DE MODO =================
def dibujar_menu_seleccion():
    if portada_menu:
        pantalla.blit(portada_menu, (0, 0))
    else:
        pantalla.fill(NEGRO)
    pygame.display.update()

modo_elegido = None
while modo_elegido is None:
    reloj.tick(30)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_1:
                modo_elegido = "local"
            elif ev.key == pygame.K_2:
                modo_elegido = "multi"
    dibujar_menu_seleccion()

# ================= CONFIGURACIÓN SEGÚN MODO =================
if modo_elegido == "multi":
    PUERTO = 5555
    if len(sys.argv) > 1:
        SERVER_IP = sys.argv[1]
    else:
        SERVER_IP = input("Ingresa la IP del servidor (Enter para localhost): ").strip()
        if SERVER_IP == "":
            SERVER_IP = "localhost"

    print(f"[CLIENTE] Conectando a {SERVER_IP}:{PUERTO} ...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)

    try:
        client_socket.connect((SERVER_IP, PUERTO))
        client_socket.settimeout(None)
        raw = client_socket.recv(1024).decode('utf-8')
        mi_id = int(raw.split('\n')[0].strip())
        print(f"[CLIENTE] Conectado como Jugador {mi_id + 1}")
    except socket.timeout:
        print("Error: tiempo de conexión agotado.")
        pygame.quit()
        sys.exit(1)
    except ConnectionRefusedError:
        print("Error: conexión rechazada.")
        pygame.quit()
        sys.exit(1)
    except Exception as e:
        print(f"Error al conectar: {e}")
        pygame.quit()
        sys.exit(1)

    def recibir_datos():
        global datos_servidor
        buffer = ""
        while True:
            try:
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                buffer += data
                if "\n" in buffer:
                    lineas = buffer.split("\n")
                    datos_servidor = lineas[-2]
                    buffer = lineas[-1]
            except:
                break

    threading.Thread(target=recibir_datos, daemon=True).start()

else:
    modo_local = True
    mi_id = 0
    j1['limite_izq'] = PISTA_IZQ + 10
    j1['limite_der'] = PISTA_DER - 10

    def logica_local():
        global datos_servidor, teclas_j1
        ALTO = 600
        DURACION = 60
        estado = "menu"
        vel_actual = 4.0
        tiempo_inicio = 0
        tiempo_restante = 60.0
        spawn_timer = 0
        obstaculos = []
        score = 0
        ganador = ""

        while True:
            time.sleep(1/60)

            if estado == "menu":
                if teclas_j1 == "START":
                    obstaculos.clear()
                    j1['vivo'] = True
                    j1['x'] = MITAD - CAR_W//2
                    score = 0
                    vel_actual = 4.0
                    tiempo_inicio = time.time()
                    estado = "jugando"
                    teclas_j1 = "NONE"

            elif estado == "jugando":
                tiempo_seg = time.time() - tiempo_inicio
                tiempo_restante = max(0.0, DURACION - tiempo_seg)
                vel_actual = 4.0 + (tiempo_seg * 0.18)

                if j1['vivo']:
                    if "A" in teclas_j1: mover_carro(j1, -1)
                    if "D" in teclas_j1: mover_carro(j1, 1)

                spawn_timer += 1
                intervalo_spawn = max(35, 85 - int(tiempo_seg * 0.7))
                if spawn_timer >= intervalo_spawn:
                    spawn_timer = 0
                    obs = crear_obstaculo(1)
                    obs['x'] = random.randint(PISTA_IZQ + 20, PISTA_DER - obs['w'] - 20)
                    obstaculos.append(obs)

                for obs in obstaculos[:]:
                    mover_obstaculo(obs, vel_actual)
                    if j1['vivo'] and rect_carro(j1).colliderect(rect_obstaculo(obs)):
                        j1['vivo'] = False
                        explotar_carro(j1)
                    if fuera_obstaculo(obs):
                        if j1['vivo']: score += 1
                        obstaculos.remove(obs)

                if tiempo_restante <= 0 or not j1['vivo']:
                    ganador = "¡HAS GANADO!" if j1['vivo'] else "¡HAS CHOCADO!"
                    estado = "fin"

            elif estado == "fin":
                if teclas_j1 == "RESET":
                    estado = "menu"
                    teclas_j1 = "NONE"

            obs_string = "/".join([f"1:{o['x']}:{o['y']}" for o in obstaculos]) if obstaculos else "NONE"

            paquete = (f"{estado},{tiempo_restante:.1f},{vel_actual:.2f},"
                       f"{j1['x']},{int(j1['vivo'])},0,0,"
                       f"{score},0,"
                       f"0,0,0,0,"
                       f"{ganador},{obs_string},NONE")

            datos_servidor = paquete

    threading.Thread(target=logica_local, daemon=True).start()

# ================= FUNCIONES GRÁFICAS =================
def dibujar_pista(vel):
    global road_offset, baranda_offset
    road_offset = (road_offset + vel) % STRIPE_SPACE
    baranda_offset = (baranda_offset + vel) % 50
    pygame.draw.rect(pantalla, (45, 45, 45), (PISTA_IZQ, 0, PISTA_ANCHO, ALTO))
    pygame.draw.rect(pantalla, GRIS_CLARO, (PISTA_IZQ-2, 0, 4, ALTO))
    pygame.draw.rect(pantalla, GRIS_CLARO, (PISTA_DER-2, 0, 4, ALTO))
    if not modo_local:
        for i in range(-1, ALTO // STRIPE_SPACE + 2):
            yo = i * STRIPE_SPACE + int(road_offset)
            pygame.draw.rect(pantalla, BLANCO, (MITAD - 3, yo, 6, 28))
    pygame.draw.rect(pantalla, (200, 200, 200), (PISTA_IZQ - BARANDA_W, 0, BARANDA_W, ALTO))
    pygame.draw.rect(pantalla, (160, 160, 160), (PISTA_IZQ - BARANDA_W + 4, 0, 6, ALTO))
    pygame.draw.rect(pantalla, (200, 200, 200), (PISTA_DER, 0, BARANDA_W, ALTO))
    pygame.draw.rect(pantalla, (160, 160, 160), (PISTA_DER + 4, 0, 6, ALTO))
    for i in range(-1, ALTO // 50 + 2):
        yo = i * 50 + int(baranda_offset)
        pygame.draw.rect(pantalla, NEGRO, (PISTA_IZQ - BARANDA_W, yo, BARANDA_W, 10))
        pygame.draw.rect(pantalla, NEGRO, (PISTA_DER, yo, BARANDA_W, 10))

def dibujar_coche(superficie, carro):
    dibujar_carro(carro, superficie)

def dibujar_hud_simple(tiempo_restante, score, j1_vivo):
    tiempo_restante = float(tiempo_restante)
    seg = int(tiempo_restante)
    alto_panel = 65
    panel = pygame.Rect(0, 0, ANCHO, alto_panel)
    pygame.draw.rect(pantalla, (10, 10, 10, 200), panel)
    pygame.draw.line(pantalla, AMARILLO, (0, alto_panel), (ANCHO, alto_panel), 2)

    txt_jugador = fuente_pixel.render("Jugador 1", True, ROJO if j1_vivo else GRIS)
    pantalla.blit(txt_jugador, (20, 8))
    if not j1_vivo:
        pantalla.blit(fuente_pixel_peq.render("ELIMINADO", True, ROJO), (20, 28))
    else:
        txt_score = fuente_pixel_peq.render(f"Obstaculos: {score}", True, BLANCO)
        pantalla.blit(txt_score, (20, 34))

    col_t = VERDE if seg > 15 else (AMARILLO if seg > 5 else ROJO)
    txt_timer = fuente_pixel_med.render(f"{seg:02d}", True, col_t)
    pantalla.blit(txt_timer, (ANCHO//2 - txt_timer.get_width()//2, 8))

    barra_ancho = 180
    progreso = tiempo_restante / 60.0
    pygame.draw.rect(pantalla, (30, 30, 30), (ANCHO//2 - barra_ancho//2, 42, barra_ancho, 10))
    pygame.draw.rect(pantalla, col_t, (ANCHO//2 - barra_ancho//2, 42, int(barra_ancho * progreso), 10))

def dibujar_hud_completo(tiempo_restante, score1, score2, j1_vivo, j2_vivo):
    tiempo_restante = float(tiempo_restante)
    seg = int(tiempo_restante)
    alto_panel = 65
    panel = pygame.Rect(0, 0, ANCHO, alto_panel)
    pygame.draw.rect(pantalla, (10, 10, 10, 200), panel)
    pygame.draw.line(pantalla, AMARILLO, (0, alto_panel), (ANCHO, alto_panel), 2)

    txt_j1 = fuente_pixel.render("Jugador 1", True, ROJO if j1_vivo else GRIS)
    pantalla.blit(txt_j1, (20, 8))
    if not j1_vivo:
        pantalla.blit(fuente_pixel_peq.render("ELIMINADO", True, ROJO), (20, 28))
    else:
        txt_score1 = fuente_pixel_peq.render(f"Obstaculos: {score1}", True, BLANCO)
        pantalla.blit(txt_score1, (20, 34))

    txt_j2 = fuente_pixel.render("Jugador 2", True, AZUL if j2_vivo else GRIS)
    pantalla.blit(txt_j2, (ANCHO - 180, 8))
    if not j2_vivo:
        pantalla.blit(fuente_pixel_peq.render("ELIMINADO", True, ROJO), (ANCHO - 180, 28))
    else:
        txt_score2 = fuente_pixel_peq.render(f"Obstaculos: {score2}", True, BLANCO)
        pantalla.blit(txt_score2, (ANCHO - 180, 34))

    col_t = VERDE if seg > 15 else (AMARILLO if seg > 5 else ROJO)
    txt_timer = fuente_pixel_med.render(f"{seg:02d}", True, col_t)
    pantalla.blit(txt_timer, (ANCHO//2 - txt_timer.get_width()//2, 8))

    barra_ancho = 180
    progreso = tiempo_restante / 60.0
    pygame.draw.rect(pantalla, (30, 30, 30), (ANCHO//2 - barra_ancho//2, 42, barra_ancho, 10))
    pygame.draw.rect(pantalla, col_t, (ANCHO//2 - barra_ancho//2, 42, int(barra_ancho * progreso), 10))

# ================= BUCLE PRINCIPAL =================
while True:
    reloj.tick(60)
    pantalla.fill(NEGRO)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()
    string_envio = "NONE"

    if modo_local:
        if estado_net == "menu":
            if teclas[pygame.K_o]:
                string_envio = "START"
        elif estado_net == "jugando":
            inputs = []
            if teclas[pygame.K_a]: inputs.append("A")
            if teclas[pygame.K_d]: inputs.append("D")
            if inputs: string_envio = "+".join(inputs)
        elif estado_net == "fin":
            if teclas[pygame.K_r]:
                string_envio = "RESET"
        teclas_j1 = string_envio
    else:
        if estado_net == "menu":
            if mi_id == 0 and teclas[pygame.K_SPACE]: string_envio = "START"
        elif estado_net == "jugando":
            inputs = []
            if mi_id == 0:
                if teclas[pygame.K_a]: inputs.append("A")
                if teclas[pygame.K_d]: inputs.append("D")
            else:
                if teclas[pygame.K_LEFT]: inputs.append("LEFT")
                if teclas[pygame.K_RIGHT]: inputs.append("RIGHT")
            if inputs: string_envio = "+".join(inputs)
        elif estado_net == "fin":
            if teclas[pygame.K_r]: string_envio = "RESET"

        try:
            client_socket.send(string_envio.encode('utf-8'))
        except:
            pass

    try:
        partes = datos_servidor.split(",")
        estado_net = partes[0]
        tiempo_net = partes[1]
        vel_net = float(partes[2])
        j1['x'] = float(partes[3])
        was_vivo1 = j1['vivo']; j1['vivo'] = bool(int(partes[4]))
        j2['x'] = float(partes[5])
        was_vivo2 = j2['vivo']; j2['vivo'] = bool(int(partes[6]))
        score1_net = int(partes[7])
        score2_net = int(partes[8])
        # ignoramos partes 9-12 (nitro)
        ganador_net = partes[13]
        obs_string = partes[14]
        # nitros_string partes[15] ignorado

        if was_vivo1 and not j1['vivo']: explotar_carro(j1)
        if was_vivo2 and not j2['vivo']: explotar_carro(j2)
    except:
        continue

    # --- RENDERIZADO ---
    if estado_net == "menu":
        if modo_local:
            if portada_local:
                pantalla.blit(portada_local, (0, 0))
            else:
                dibujar_pista(3)
            aviso = fuente_med.render("Presiona O para iniciar", True, BLANCO)
            pantalla.blit(aviso, (ANCHO//2 - aviso.get_width()//2, ALTO - 80))
        else:
            if mi_id == 0 and portada_j1:
                pantalla.blit(portada_j1, (0, 0))
            elif mi_id == 1 and portada_j2:
                pantalla.blit(portada_j2, (0, 0))
            else:
                dibujar_pista(3)

    elif estado_net == "jugando":
        dibujar_pista(vel_net)

        if obs_string != "NONE":
            for obs_data in obs_string.split("/"):
                carril_o, x_o, y_o = map(float, obs_data.split(":"))
                obs_temp = crear_obstaculo(int(carril_o))
                obs_temp['x'] = x_o
                obs_temp['y'] = y_o
                # Ahora dibujamos con el mismo diseño de coche
                dibujar_coche(pantalla, obs_temp)

        if j1['vivo'] and random.random() < 0.3:
            particles_fondo.append(crear_particula(int(j1['x']+10), int(j1['y']+CAR_H+2), (180, 180, 180)))
        if not modo_local and j2['vivo'] and random.random() < 0.3:
            particles_fondo.append(crear_particula(int(j2['x']+10), int(j2['y']+CAR_H+2), (180, 180, 180)))
        for p in particles_fondo[:]:
            actualizar_particula(p)
            dibujar_particula(p, pantalla)
            if p['vida'] <= 0: particles_fondo.remove(p)

        actualizar_particulas_carro(j1)
        if not modo_local:
            actualizar_particulas_carro(j2)

        dibujar_coche(pantalla, j1)
        if not modo_local:
            dibujar_coche(pantalla, j2)

        if modo_local:
            dibujar_hud_simple(tiempo_net, score1_net, j1['vivo'])
        else:
            dibujar_hud_completo(tiempo_net, score1_net, score2_net, j1['vivo'], j2['vivo'])

    elif estado_net == "fin":
        dibujar_pista(0)
        ov = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 180))
        pantalla.blit(ov, (0, 0))
        t = fuente_grande.render(ganador_net, True, AMARILLO)
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, 200))
        r = fuente_med.render("Presiona R para volver al menú", True, BLANCO)
        pantalla.blit(r, (ANCHO//2 - r.get_width()//2, 400))

    pygame.display.update()