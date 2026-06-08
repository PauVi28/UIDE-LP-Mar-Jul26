import random

def crear_mazo():

    palos = ["♠️", "♥️", "♦️", "♣️"]

    valores = [
        "A", "2", "3", "4", "5",
        "6", "7", "8", "9", "10",
        "J", "Q", "K"
    ]

    mazo = []

    for palo in palos:
        for valor in valores:
            mazo.append(valor + palo)

    random.shuffle(mazo)

    return mazo
