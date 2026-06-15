import random

PALOS = ["oros", "copas", "espadas", "bastos"]
VALORES = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]  


def crear_mazo():
    mazo = []
    for palo in PALOS:
        for valor in VALORES:
            carta = {"valor": valor, "palo": palo}
            mazo.append(carta)
    random.shuffle(mazo)
    return mazo


def texto_valor(valor):
    especiales = {1: "A", 10: "S", 11: "C", 12: "R"}
    return especiales.get(valor, str(valor))


def nombre_carta(carta):
    return texto_valor(carta["valor"]) + " de " + carta["palo"]
