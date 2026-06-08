import socket
from game_logic import imprimir_tablero, verificar_ganador

HOST = "192.168.10.98"
PORT = 65432

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

print("Conectado al servidor.")

while True:
    print("Esperando jugada del servidor...")
    datos = cliente.recv(1024).decode()
    tablero = eval(datos)

    ganador = verificar_ganador(tablero)
    if ganador:
        imprimir_tablero(tablero)
        print("Resultado:", ganador)
        break

    imprimir_tablero(tablero)

    jugada = int(input("Tu turno (O). Elige una posición del 0 al 8: "))

    if jugada < 0 or jugada > 8 or tablero[jugada] != " ":
        print("Movimiento inválido. Pierdes el turno.")
    else:
        tablero[jugada] = "O"

    cliente.send(str(tablero).encode())

    ganador = verificar_ganador(tablero)
    if ganador:
        imprimir_tablero(tablero)
        print("Resultado:", ganador)
        break

cliente.close()