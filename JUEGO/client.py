import socket
HOST = "192.168.10.1"
PUERTO = 5000
opciones = ["piedra", "papel", "tijera", "salir"]
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PUERTO))
print("Conectado al servidor.")
while True:
    jugada_servidor = cliente.recv(1024).decode()
    if jugada_servidor == "salir":
        print("El servidor cerró el juego.")
        break
    print("\n--- NUEVA RONDA ---")
    jugada_cliente = input("Jugador 2, elige piedra, papel, tijera o salir: ").lower()
    while jugada_cliente not in opciones:
        print("Opción inválida.")
        jugada_cliente = input("Jugador 2, elige piedra, papel, tijera o salir: ").lower()
    cliente.send(jugada_cliente.encode())
    if jugada_cliente == "salir":
        print("Cliente cerró el juego.")
        break
    resultado = cliente.recv(1024).decode()
    print("Jugador 1 eligió:", jugada_servidor)
    print("Resultado:", resultado)
cliente.close()
print("Cliente cerrado.")