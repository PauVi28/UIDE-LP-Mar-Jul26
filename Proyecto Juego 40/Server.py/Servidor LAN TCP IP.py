import socket

HOST = "0.0.0.0"
PORT = 5000

def iniciar_servidor():

    servidor = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    servidor.bind((HOST, PORT))

    servidor.listen()

    print("Servidor iniciado...")
    print("Esperando jugador...")

    conexion, direccion = servidor.accept()

    print(f"Jugador conectado desde {direccion}")

    conexion.send(
        "Conexión establecida".encode()
    )

    while True:

        datos = conexion.recv(1024).decode()

        if not datos:
            break

        print(f"Cliente: {datos}")

        conexion.send(
            "Datos recibidos".encode()
        )

    conexion.close()
    servidor.close()

Nota: Este es el inico del trabajo y puede ser modificado dependiendo el requerimiento del trabajado.
