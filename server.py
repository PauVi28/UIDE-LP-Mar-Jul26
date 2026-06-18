#server.py
import socket
import threading
import time
import random
from game_logic import (
    crear_carro, mover_carro,
    explotar_carro, rect_carro,
    crear_obstaculo, mover_obstaculo, fuera_obstaculo, rect_obstaculo,
)

# ============================================================
#------------------- CONFIGURACIÓN DEL SERVIDOR ----------------
# ============================================================
HOST = '0.0.0.0'
PUERTO = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PUERTO))
server.listen(2)

clientes = []
teclas_jugadores = {0: "NONE", 1: "NONE"}
lock = threading.Lock()

print(f"[SERVIDOR] Escuchando en el puerto {PUERTO}...")
print(f"[SERVIDOR] Comparte tu IP local con los clientes (ver con 'ipconfig' en Windows o 'ip a' en Linux)")

# ============================================================
#------------------ VARIABLES GLOBALES DEL JUEGO ---------------
# ============================================================
ALTO = 600
CAR_W, CAR_H = 46, 84
CARRIL1_IZQ, CARRIL1_DER = 183, 442
CARRIL2_IZQ, CARRIL2_DER = 458, 725

j1 = crear_carro(CARRIL1_IZQ + (259 - CAR_W) // 2, ALTO - CAR_H - 30,
                 (230, 30, 30), (150, 0, 0), CARRIL1_IZQ, CARRIL1_DER)
j2 = crear_carro(CARRIL2_IZQ + (259 - CAR_W) // 2, ALTO - CAR_H - 30,
                 (0, 100, 255), (0, 50, 160), CARRIL2_IZQ, CARRIL2_DER)

estado = "menu"
vel_actual = 4.0
tiempo_inicio = 0
DURACION = 60
tiempo_restante = 60.0
spawn_timer = 0
obstaculos = []
score1 = 0
score2 = 0
ganador = ""

# ============================================================
#----------------- MANEJO DE CLIENTES (HILO) ------------------
# ============================================================
def manejar_cliente(conn, jugador_id):
    try:
        conn.send((str(jugador_id) + "\n").encode('utf-8'))
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            with lock:
                teclas_jugadores[jugador_id] = data
    except:
        pass
    finally:
        print(f"[SERVIDOR] Jugador {jugador_id + 1} desconectado.")
        with lock:
            teclas_jugadores[jugador_id] = "NONE"
            if conn in clientes:
                clientes.remove(conn)
        conn.close()

# ============================================================
#------------------ BUCLE PRINCIPAL DEL JUEGO ------------------
# ============================================================
def bucle_logica_juego():
    global estado, tiempo_inicio, tiempo_restante, vel_actual, spawn_timer, ganador
    global score1, score2, obstaculos

    while True:
        time.sleep(1/60)
        if len(clientes) < 2:
            continue

        if estado == "menu":
            if teclas_jugadores[0] == "START":
                obstaculos.clear()
                j1['vivo'] = True
                j2['vivo'] = True
                j1['x'] = CARRIL1_IZQ + (259 - CAR_W) // 2
                j2['x'] = CARRIL2_IZQ + (259 - CAR_W) // 2
                score1 = 0
                score2 = 0
                vel_actual = 4.0
                tiempo_inicio = time.time()
                estado = "jugando"
                teclas_jugadores[0] = "NONE"

        elif estado == "jugando":
            tiempo_seg = time.time() - tiempo_inicio
            tiempo_restante = max(0.0, DURACION - tiempo_seg)
            vel_actual = 4.0 + (tiempo_seg * 0.18)

            # Movimiento de los coches
            if j1['vivo']:
                if "A" in teclas_jugadores[0]: mover_carro(j1, -1)
                if "D" in teclas_jugadores[0]: mover_carro(j1, 1)
            if j2['vivo']:
                if "LEFT" in teclas_jugadores[1]: mover_carro(j2, -1)
                if "RIGHT" in teclas_jugadores[1]: mover_carro(j2, 1)

            # Spawn de obstáculos
            spawn_timer += 1
            intervalo_spawn = max(35, 85 - int(tiempo_seg * 0.7))
            if spawn_timer >= intervalo_spawn:
                spawn_timer = 0
                obstaculos.append(crear_obstaculo(random.choice([1, 2])))

            # Movimiento de obstáculos
            for obs in obstaculos[:]:
                mover_obstaculo(obs, vel_actual)
                if j1['vivo'] and rect_carro(j1).colliderect(rect_obstaculo(obs)):
                    j1['vivo'] = False
                    explotar_carro(j1)
                if j2['vivo'] and rect_carro(j2).colliderect(rect_obstaculo(obs)):
                    j2['vivo'] = False
                    explotar_carro(j2)
                if fuera_obstaculo(obs):
                    if obs['carril'] == 1 and j1['vivo']: score1 += 1
                    if obs['carril'] == 2 and j2['vivo']: score2 += 1
                    obstaculos.remove(obs)

            # Fin de partida
            if tiempo_restante <= 0 or (not j1['vivo'] and not j2['vivo']):
                if j1['vivo'] and j2['vivo']:
                    ganador = "¡JUGADOR 1 GANA!" if score1 > score2 else ("¡JUGADOR 2 GANA!" if score2 > score1 else "¡EMPATE!")
                elif j1['vivo'] and not j2['vivo']:
                    ganador = "¡JUGADOR 1 GANA!"
                elif j2['vivo'] and not j1['vivo']:
                    ganador = "¡JUGADOR 2 GANA!"
                else:
                    ganador = "¡JUGADOR 1 GANA!" if score1 > score2 else ("¡JUGADOR 2 GANA!" if score2 > score1 else "¡EMPATE!")
                estado = "fin"

        elif estado == "fin":
            if teclas_jugadores[0] == "RESET" or teclas_jugadores[1] == "RESET":
                estado = "menu"
                teclas_jugadores[0] = "NONE"
                teclas_jugadores[1] = "NONE"

        # Construcción y envío del paquete de datos
        obs_string = "/".join([f"{o['carril']}:{o['x']}:{o['y']}" for o in obstaculos]) if obstaculos else "NONE"

        paquete = (f"{estado},{tiempo_restante:.1f},{vel_actual:.2f},"
                   f"{j1['x']},{int(j1['vivo'])},{j2['x']},{int(j2['vivo'])},"
                   f"{score1},{score2},"
                   f"0,0,0,0,"            
                   f"{ganador},{obs_string},NONE")  

        for c in clientes[:]:
            try:
                c.send((paquete + "\n").encode('utf-8'))
            except:
                pass

# ============================================================
#------------------ INICIAR HILO DEL JUEGO --------------------
# ============================================================
threading.Thread(target=bucle_logica_juego, daemon=True).start()

# ============================================================
#------------ BUCLE DE ACEPTACIÓN DE CONEXIONES ---------------
# ============================================================
while True:
    try:
        conn, addr = server.accept()
        with lock:
            if len(clientes) < 2:
                jugador_id = len(clientes)
                clientes.append(conn)
        print(f"[SERVIDOR] Jugador {jugador_id + 1} conectado desde {addr}")
        threading.Thread(target=manejar_cliente, args=(conn, jugador_id), daemon=True).start()
    except:
        break