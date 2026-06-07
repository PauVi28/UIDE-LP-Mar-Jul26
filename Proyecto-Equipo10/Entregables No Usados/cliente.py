import socket
 
HOST = '127.0.0.1'
PORT = 65432
 
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))
print("Conectado al Jugador 1\n")
 
while True:
    mensaje = cliente.recv(1024).decode('utf-8')
    print(f"Jugador 1: {mensaje}")
 
    respuesta = input("Jugador 2: ").strip()
    cliente.sendall(respuesta.encode('utf-8'))

cliente.close()
