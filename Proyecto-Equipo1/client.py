import socket

HOST = "0.0.0.0"
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print(client.recv(1024).decode())

while True:
    num = input("Ingresa número: ")

    client.send(num.encode())

    respuesta = client.recv(1024).decode()
    print(respuesta)

    if respuesta == "Ganaste!":
        break

client.close()
