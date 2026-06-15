import socket
import json
from network import config


class Cliente:
    def __init__(self, ip, puerto=config.PUERTO):
        self.ip = ip
        self.puerto = puerto
        self.sock = None
        self.buffer = ""

    def conectar(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.puerto))

    def enviar(self, datos):
        if self.sock is None:
            return
        texto = json.dumps(datos) + "\n"
        self.sock.sendall(texto.encode("utf-8"))

    def recibir(self):
        if self.sock is None:
            return None
        while "\n" not in self.buffer:
            parte = self.sock.recv(config.TAMANO_BUFFER)
            if not parte:
                return None
            self.buffer += parte.decode("utf-8")
        linea, self.buffer = self.buffer.split("\n", 1)
        if not linea.strip():
            return None
        return json.loads(linea)

    def cerrar(self):
        if self.sock:
            self.sock.close()
