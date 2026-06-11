import socket
from game_logic import determinar_ganador
HOST = "0.0.0.0"
PUERTO = 5000
opciones = ["piedra", "papel", "tijera", "salir"]
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PUERTO))
servidor.listen(1)
print("Servidor iniciado.")
print("Esperando conexión del cliente...")
cliente, direccion = servidor.accept()
print("Cliente conectado desde:", direccion)
while True:
    print("\n--- NUEVA RONDA ---")
    jugada_servidor = input("Jugador 1, elige piedra, papel, tijera o salir: ").lower()
    while jugada_servidor not in opciones:
        print("Opción inválida.")
        jugada_servidor = input("Jugador 1, elige piedra, papel, tijera o salir: ").lower()
    cliente.send(jugada_servidor.encode())
    if jugada_servidor == "salir":
        print("Servidor cerró el juego.")
        break
    jugada_cliente = cliente.recv(1024).decode()
    if jugada_cliente == "salir":
        print("El cliente salió del juego.")
        break
    print("Jugador 2 eligió:", jugada_cliente)
    resultado = determinar_ganador(jugada_servidor, jugada_cliente)
    if resultado == "Gana Jugador 1":
        mensaje_resultado = "Ganó el servidor"
    elif resultado == "Gana Jugador 2":
        mensaje_resultado = "Ganó el cliente"
    else:
        mensaje_resultado = "Empate"
    print("Resultado:", mensaje_resultado)
    cliente.send(mensaje_resultado.encode())
cliente.close()
servidor.close()
print("Servidor cerrado.")