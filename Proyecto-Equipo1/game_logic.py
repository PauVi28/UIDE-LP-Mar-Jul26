import random

def seleccionar_limite(nivel):

    if nivel == 1:
        return 50

    elif nivel == 2:
        return 100

    elif nivel == 3:
        return 1000

    else:
        return 100


def generar_numero(limite):
    return random.randint(1, limite)


def verificar_numero(intento, numero_secreto):

    if intento == numero_secreto:
        return "correcto"

    elif intento < numero_secreto:
        return "mayor"

    else:
        return "menor"