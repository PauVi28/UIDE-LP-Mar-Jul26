import socket

HOST = input("IP del servidor: ")
PORT = 5000

def iniciar_cliente():

    cliente = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:

        cliente.connect((HOST, PORT))

        mensaje = cliente.recv(1024).decode()

        print(mensaje)

        while True:

            datos = input("Ingrese mensaje: ")

            cliente.send(datos.encode())

            respuesta = cliente.recv(1024).decode()

            print(f"Servidor: {respuesta}")

    except:

        print("No se pudo conectar.")

    finally:

        cliente.close()

Nota: Este es el inico del trabajo y puede ser modificado dependiendo el requerimiento del trabajado.
