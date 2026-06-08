import socket
from game_logic import determinar_ganador

def iniciar_servidor():
    HOST = '0.0.0.0'
    PORT = 65432

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)

    print(f"[SERVIDOR] Esperando conexiones en el puerto {PORT}...")

    conn1, addr1 = server_socket.accept()
    print(f"[SERVIDOR] Jugador 1 conectado desde {addr1}")
    conn1.sendall(b"Conectado como Jugador 1. Esperando al rival...")

    conn2, addr2 = server_socket.accept()
    print(f"[SERVIDOR] Jugador 2 conectado desde {addr2}")
    conn2.sendall(b"Conectado como Jugador 2. El juego comienza ya.")
    conn1.sendall(b"Rival listo. Envia tu jugada.")

    try:
        jugada1 = conn1.recv(1024).decode().strip()
        print(f"[SERVIDOR] Jugador 1 eligió: {jugada1}")

        jugada2 = conn2.recv(1024).decode().strip()
        print(f"[SERVIDOR] Jugador 2 eligió: {jugada2}")

        res_j1 = determinar_ganador(jugada1, jugada2)

        if res_j1 == "empate":
            conn1.sendall(b"Empate")
            conn2.sendall(b"Empate")
        elif res_j1 == "ganas":
            conn1.sendall(b"Ganaste")
            conn2.sendall(b"Perdiste")
        else:
            conn1.sendall(b"Perdiste")
            conn2.sendall(b"Ganaste")

    except Exception as e:
        print(f"[ERROR] Ocurrió un problema: {e}")
    finally:
        conn1.close()
        conn2.close()
        server_socket.close()
        print("[SERVIDOR] Partida terminada y sockets cerrados.")

if __name__ == "__main__":
    iniciar_servidor()
