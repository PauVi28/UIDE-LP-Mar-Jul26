def determinar_ganador(jugador1, jugador2):
    if jugador1 == jugador2:
        return "Empate"

    elif jugador1 == "piedra" and jugador2 == "tijera":
        return "Gana Jugador 1"

    elif jugador1 == "papel" and jugador2 == "piedra":
        return "Gana Jugador 1"

    elif jugador1 == "tijera" and jugador2 == "papel":
        return "Gana Jugador 1"

    else:
        return "Gana Jugador 2"