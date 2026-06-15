import socket
import json
from network import config


class Servidor:
    def __init__(self, puerto=config.PUERTO):
        self.puerto = puerto
        self.sock = None
        self.conexion = None
        self.buffer = ""

    def esperar_cliente(self):
     
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((config.ESCUCHAR_EN, self.puerto))
        self.sock.listen(1)
        self.conexion, direccion = self.sock.accept()
        return direccion

    def enviar(self, datos):
       
        if self.conexion is None:
            return
        texto = json.dumps(datos) + "\n"
        self.conexion.sendall(texto.encode("utf-8"))

    def recibir(self):
        
        if self.conexion is None:
            return None
        while "\n" not in self.buffer:
            parte = self.conexion.recv(config.TAMANO_BUFFER)
            if not parte:
                return None
            self.buffer += parte.decode("utf-8")
        linea, self.buffer = self.buffer.split("\n", 1)
        if not linea.strip():
            return None
        return json.loads(linea)

    def cerrar(self):
        if self.conexion:
            self.conexion.close()
        if self.sock:
            self.sock.close()
