import threading

from logica.game40 import Game40
from network.servidor import Servidor
from multiplayer import estados


class Host:
    def __init__(self, puerto=None):
        self.juego = Game40(modo="lan")
        self.servidor = Servidor(puerto) if puerto else Servidor()
        self.jugadas_cliente = []     
        self.lock = threading.Lock() 
        self.conectado = False
        self.error = ""
        self.activo = True

    def iniciar(self):
     
        hilo = threading.Thread(target=self._aceptar_y_escuchar, daemon=True)
        hilo.start()

    def _aceptar_y_escuchar(self):
        try:
            self.servidor.esperar_cliente()
        except OSError as e:
            self.error = "No se pudo abrir el puerto: " + str(e)
            return
        self.conectado = True
        self.enviar_estado()      
        while self.activo:
            mensaje = self.servidor.recibir()
            if mensaje is None:
                break              
            if mensaje.get("tipo") == "jugar":
                with self.lock:
                    self.jugadas_cliente.append(mensaje.get("indice", 0))

    def procesar(self):

        with self.lock:
            pendientes = self.jugadas_cliente
            self.jugadas_cliente = []
        hubo_cambio = False
        for indice in pendientes:
            self.juego.jugar_carta(2, indice) 
            hubo_cambio = True
        if hubo_cambio:
            self.enviar_estado()

    def jugar_host(self, indice):
        """El host (jugador 1) juega una de sus cartas."""
        self.juego.jugar_carta(1, indice)
        self.enviar_estado()

    def enviar_estado(self):
        if self.conectado:
            try:
                self.servidor.enviar(estados.estado_a_dict(self.juego))
            except OSError:
                self.conectado = False

    def cerrar(self):
        self.activo = False
        self.servidor.cerrar()
