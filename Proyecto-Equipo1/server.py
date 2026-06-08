import socket
from game_logic import seleccionar_limite, generar_numero

HOST = "127.0.0.1"
PORT = 5555

print("=== CONFIGURACIÓN DEL JUEGO ===")
print("1. Fácil")
print("2. Medio")
print("3. Difícil")

nivel = int(input("Seleccione nivel: "))

limite = seleccionar_limite(nivel)
numero_secreto = generar_numero(limite)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Servidor iniciado...")
print(f"Número generado entre 1 y {limite}")

conn, addr = server.accept()
print("Cliente conectado:", addr)

conn.send(f"Adivina el número del 1 al {limite}".encode())

while True:
    data = conn.recv(1024).decode()

    if not data:
        break

    intento = int(data)

    if intento == numero_secreto:
        conn.send("Ganaste!".encode())
        break
    elif intento < numero_secreto:
        conn.send("El número es mayor".encode())
    else:
        conn.send("El número es menor".encode())

conn.close()
server.close()
