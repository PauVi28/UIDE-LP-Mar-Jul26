import socket
import threading

from game_logic import (
    seleccionar_limite,
    generar_numero,
    verificar_numero
)

HOST = "0.0.0.0"
PORT = 5555

print("=== CONFIGURACIÓN DEL JUEGO ===")
print("1. Fácil")
print("2. Medio")
print("3. Difícil")

nivel = int(input("Seleccione nivel: "))

limite = seleccionar_limite(nivel)

numero_secreto = generar_numero(limite)

ganador = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen()

print("\nServidor iniciado...")
print("Esperando jugadores...")
print(f"Número generado entre 1 y {limite}")


def manejar_cliente(conn, addr):

    global ganador

    print(f"Jugador conectado: {addr}")

    conn.send(f"Juego iniciado del 1 al {limite}".encode())

    while not ganador:

        try:

            data = conn.recv(1024).decode()

            if not data:
                break

            intento = int(data)

            resultado = verificar_numero(
                intento,
                numero_secreto
            )

            if resultado == "correcto":

                conn.send(
                    "¡Felicidades! Has ganado.".encode()
                )

                print(f"Jugador {addr} ganó.")

                ganador = True

            elif resultado == "mayor":

                conn.send(
                    "El número secreto es mayor.".encode()
                )

            else:

                conn.send(
                    "El número secreto es menor.".encode()
                )

        except:
            break

    conn.close()


while True:

    conn, addr = server.accept()

    hilo = threading.Thread(
        target=manejar_cliente,
        args=(conn, addr)
    )

    hilo.start()