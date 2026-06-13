import socket

def iniciar_cliente():

    HOST = input(
        "Ingrese la IP del servidor: "
    )

    PORT = 5000

    cliente = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    cliente.connect((HOST, PORT))

    cliente.send(
        "Hola servidor".encode()
    )

    respuesta = cliente.recv(1024).decode()

    print("Servidor:", respuesta)

    cliente.close()