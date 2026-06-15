PUNTOS_CAIDA = 2
PUNTOS_LIMPIA = 2
PUNTOS_CARTON = 6
META = 40          


def buscar_captura(mesa, carta):

    capturadas = []
    for c in mesa:
        if c["valor"] == carta["valor"]:
            capturadas.append(c)
    return capturadas


def es_caida(capturadas, ultima_carta, ultimo_jugador, jugador):
 
    if ultima_carta is None:
        return False
    if ultimo_jugador == jugador:
        return False
    return ultima_carta in capturadas


def es_limpia(mesa):

    return len(mesa) == 0


def mayor_carton(carton1, carton2):
 
    if len(carton1) > len(carton2):
        return 1
    if len(carton2) > len(carton1):
        return 2
    return 0
