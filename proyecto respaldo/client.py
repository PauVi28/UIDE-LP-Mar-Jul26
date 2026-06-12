import socket

def conectar_al_juego():
    # Cambia esta IP por la IP de la máquina donde corre server.py
    SERVER_IP = '127.0.0.1'
    PORT = 65432

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((SERVER_IP, PORT))

        msg = client_socket.recv(1024).decode()
        print(f"\n[SERVIDOR]: {msg}")

        if "Esperando" in msg:
            msg_espera = client_socket.recv(1024).decode()
            print(f"[SERVIDOR]: {msg_espera}")

        opciones = ['piedra', 'papel', 'tijera']
        jugada = ""
        while jugada not in opciones:
            jugada = input("Elige tu jugada (piedra, papel, tijera): ").lower().strip()

        client_socket.sendall(jugada.encode())
        print("Jugada enviada. Esperando resultado...")

        resultado = client_socket.recv(1024).decode()
        print(f"\n=======================")
        print(f" RESULTADO: {resultado} ")
        print(f"=======================")

    except ConnectionRefusedError:
        print("[ERROR] No se pudo conectar. ¿Está corriendo server.py?")
    finally:
        client_socket.close()

if __name__ == "__main__":
    conectar_al_juego()
