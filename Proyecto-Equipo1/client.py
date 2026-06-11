import socket

HOST = input("Ingrese la IP del servidor: ")
PORT = 5555
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))
    print(client.recv(1024).decode())
    while True:
        try:
            num = input("Ingresa número: ")
            client.send(num.encode())
            respuesta = client.recv(1024).decode()
            if not respuesta:
                print("Servidor desconectado")
                break
            print(respuesta)
            
            if respuesta == "Ganaste!":
                break
        except:
            print("Servidor desconectado")
            break
except:
    print("No se pudo conectar al servidor")

client.close()
