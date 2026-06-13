import socket

HOST = "0.0.0.0"
PORT = 5000

def iniciar_servidor():

    servidor = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    servidor.bind((HOST, PORT))
    servidor.listen(1)

    print("Esperando conexión del cliente...")

    conexion, direccion = servidor.accept()

    print("Cliente conectado:", direccion)

    mensaje = conexion.recv(1024).decode()

    print("Cliente dice:", mensaje)

    conexion.send(
        "Conexión establecida correctamente".encode()
    )

    conexion.close()
    servidor.close()