import socket
from game_logic import imprimir_tablero, verificar_ganador

HOST = "0.0.0.0"
PORT = 65432

tablero = [" "] * 9

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Servidor iniciado. Esperando cliente...")
conn, addr = server.accept()
print("Cliente conectado:", addr)

while True:
    imprimir_tablero(tablero)

    jugada = int(input("Tu turno (X). Elige una posición del 0 al 8: "))

    if jugada < 0 or jugada > 8 or tablero[jugada] != " ":
        print("Movimiento inválido. Intenta otra vez.")
        continue

    tablero[jugada] = "X"

    ganador = verificar_ganador(tablero)
    conn.send(str(tablero).encode())

    if ganador:
        imprimir_tablero(tablero)
        print("Resultado:", ganador)
        break

    print("Esperando jugada del cliente...")
    datos = conn.recv(1024).decode()
    tablero = eval(datos)

    ganador = verificar_ganador(tablero)
    if ganador:
        imprimir_tablero(tablero)
        print("Resultado:", ganador)
        break

conn.close()
server.close()