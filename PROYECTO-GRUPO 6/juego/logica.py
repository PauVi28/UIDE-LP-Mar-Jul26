def ganador(jugador1, jugador2):

    if jugador1 == jugador2:
        return "🤝 Empate"

    elif (
        (jugador1 == "piedra" and jugador2 == "tijera") or
        (jugador1 == "papel" and jugador2 == "piedra") or
        (jugador1 == "tijera" and jugador2 == "papel")
    ):
        return "🎉 ¡Ganaste!"

    else:
        return "💻 La computadora ganó"