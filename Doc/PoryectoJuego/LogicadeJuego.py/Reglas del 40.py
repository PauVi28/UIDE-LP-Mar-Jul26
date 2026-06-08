def calcular_ganador(carta_jugador, carta_cpu):

    valores = {
        "A": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13
    }

    valor_jugador = carta_jugador[:-1]
    valor_cpu = carta_cpu[:-1]

    if valores[valor_jugador] > valores[valor_cpu]:
        return "jugador"

    elif valores[valor_cpu] > valores[valor_jugador]:
        return "cpu"

    else:
        return "empate"
