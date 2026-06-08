from logica.mazo import crear_mazo

class Game40:

    def _init_(self):

        self.mazo = crear_mazo()

        self.mano_jugador = [
            self.mazo.pop(),
            self.mazo.pop(),
            self.mazo.pop(),
            self.mazo.pop(),
            self.mazo.pop()
        ]

        self.mano_cpu = [
            self.mazo.pop(),
            self.mazo.pop(),
            self.mazo.pop(),
            self.mazo.pop(),
            self.mazo.pop()
        ]

        self.mesa = [
            self.mazo.pop(),
            self.mazo.pop(),
            self.mazo.pop(),
            self.mazo.pop()
        ]

        self.puntaje_jugador = 0
        self.puntaje_cpu = 0


        self.carta_seleccionada = None


    def jugar_turno(self,indice):
        if indice >= len(self.mano_jugador):
            return

        carta = self.mano_jugador.pop(indice)

        self.mesa.append(carta)

        self.carta_seleccionada = None
