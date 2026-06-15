from logica import mazo as mazo_modulo
from logica import reglas40
from logica import cpu


class Game40:
    def __init__(self, modo="cpu"):
        self.modo = modo           
        self.mazo = []
        self.mesa = []             

        self.mano_jugador = []
        self.mano_cpu = []          
        self.mano_jugador2 = []     

        self.carton_jugador = []    
        self.carton_jugador2 = []  

        self.puntaje_jugador = 0
        self.puntaje_jugador2 = 0

        self.turno = 1             
        self.ultima_carta = None    
        self.ultimo_jugador = None 
        self.ganador = None         
        self.evento = ""            

        self.iniciar()

    def _mano_rival(self):
        """La mano del jugador 2 segun el modo."""
        if self.modo == "cpu":
            return self.mano_cpu
        return self.mano_jugador2

    def _mano(self, jugador):
        if jugador == 1:
            return self.mano_jugador
        return self._mano_rival()

    def _carton(self, jugador):
        if jugador == 1:
            return self.carton_jugador
        return self.carton_jugador2

    def _sumar_puntos(self, jugador, puntos):
        if jugador == 1:
            self.puntaje_jugador += puntos
        else:
            self.puntaje_jugador2 += puntos

    def iniciar(self):
        self.mazo = mazo_modulo.crear_mazo()
        self.mesa = []
        self.repartir()
        self.turno = 1

    def repartir(self):
        """Reparte 5 cartas a cada jugador, una por vez, desde el mazo."""
        for _ in range(5):
            if self.mazo:
                self.mano_jugador.append(self.mazo.pop())
            if self.mazo:
                self._mano_rival().append(self.mazo.pop())

    def jugar_carta(self, jugador, indice):
        """Procesa la jugada de un jugador. Solo lo llama el host (o el modo cpu).
        Aqui se resuelven capturas, caidas, limpias y el cambio de turno."""
        if self.ganador is not None:
            return
        if jugador != self.turno:
            return                      

        mano = self._mano(jugador)
        if indice < 0 or indice >= len(mano):
            return                    

        carta = mano.pop(indice)
        capturadas = reglas40.buscar_captura(self.mesa, carta)
        self.evento = ""

        if capturadas:
            
            for c in capturadas:
                self.mesa.remove(c)
            carton = self._carton(jugador)
            carton.extend(capturadas)
            carton.append(carta)
            self.evento = "captura"

            if reglas40.es_caida(capturadas, self.ultima_carta,
                                 self.ultimo_jugador, jugador):
                self._sumar_puntos(jugador, reglas40.PUNTOS_CAIDA)
                self.evento = "caida"

            if reglas40.es_limpia(self.mesa):
                self._sumar_puntos(jugador, reglas40.PUNTOS_LIMPIA)
                self.evento = "limpia"

            self.ultima_carta = None
            self.ultimo_jugador = None
        else:
         
            self.mesa.append(carta)
            self.ultima_carta = carta
            self.ultimo_jugador = jugador
            self.evento = "carta"

        self.turno = 2 if jugador == 1 else 1

        self.verificar_reparto()
        self.fin_ronda()

    def turno_cpu(self):
        """En modo cpu hace jugar a la maquina cuando le toca."""
        if self.modo != "cpu":
            return
        if self.turno != 2 or self.ganador is not None:
            return
        indice = cpu.jugar_cpu(self)
        self.jugar_carta(2, indice)

    def verificar_reparto(self):
        """Si los dos se quedaron sin cartas pero aun hay mazo, reparte otra vez.
        No reinicia puntos ni carton."""
        sin_cartas = len(self.mano_jugador) == 0 and len(self._mano_rival()) == 0
        if sin_cartas and len(self.mazo) > 0:
            self.repartir()

    def fin_ronda(self):
        """Cuando ya no hay mazo ni cartas en las manos, se cierra la ronda:
        se cuenta el carton, se suman los 6 puntos y se revisa el ganador."""
        mazo_vacio = len(self.mazo) == 0
        manos_vacias = len(self.mano_jugador) == 0 and len(self._mano_rival()) == 0
        if not (mazo_vacio and manos_vacias):
            return

        quien = reglas40.mayor_carton(self.carton_jugador, self.carton_jugador2)
        if quien != 0:
            self._sumar_puntos(quien, reglas40.PUNTOS_CARTON)

        self.comprobar_ganador()
        if self.ganador is None:
            self.nueva_ronda()

    def comprobar_ganador(self):
        if self.puntaje_jugador >= reglas40.META:
            self.ganador = 1
        elif self.puntaje_jugador2 >= reglas40.META:
            self.ganador = 2

    def nueva_ronda(self):
        """Arranca otra ronda. Se reinician mazo, mesa y carton, pero NO los puntos."""
        self.mazo = mazo_modulo.crear_mazo()
        self.mesa = []
        self.carton_jugador = []
        self.carton_jugador2 = []
        self.ultima_carta = None
        self.ultimo_jugador = None
        self.repartir()
        self.turno = 1
