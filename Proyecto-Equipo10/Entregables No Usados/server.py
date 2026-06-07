import socket
 
HOST = '127.0.0.1'
PORT = 65432
 
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()
 
print("Esperando conexion del Jugador 2...")
 
conexion, direccion = servidor.accept()
print(f"Jugador 2 conectado desde {direccion}\n")
 
while True:
    mensaje = input("Jugador 1: ").strip()
    conexion.sendall(mensaje.encode('utf-8'))
 
    respuesta = conexion.recv(1024).decode('utf-8')
    print(f"Jugador 2: {respuesta}")
 
conexion.close()
servidor.close()
