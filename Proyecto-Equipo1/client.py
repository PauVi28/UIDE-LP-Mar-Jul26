import socket

HOST = input("Ingresa la IP del servidor: ")
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

mensaje = client.recv(1024).decode()

print(mensaje)

while True:

    intento = input("Ingresa tu número: ")

    client.send(intento.encode())

    respuesta = client.recv(1024).decode()

    print(respuesta)

    if "ganado" in respuesta.lower():
        break

client.close()