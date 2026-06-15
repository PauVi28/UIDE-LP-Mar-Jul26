def estado_a_dict(juego):
 
    return {
        "mesa": juego.mesa,
        "mano_jugador": juego.mano_jugador,
        "mano_jugador2": juego.mano_jugador2,
        "puntaje_jugador": juego.puntaje_jugador,
        "puntaje_jugador2": juego.puntaje_jugador2,
        "carton_jugador": len(juego.carton_jugador),
        "carton_jugador2": len(juego.carton_jugador2),
        "turno": juego.turno,
        "ultima_carta": juego.ultima_carta,
        "ultimo_jugador": juego.ultimo_jugador,
        "ganador": juego.ganador,
        "evento": juego.evento,
    }


def estado_vacio():
 
    return {
        "mesa": [],
        "mano_jugador": [],
        "mano_jugador2": [],
        "puntaje_jugador": 0,
        "puntaje_jugador2": 0,
        "carton_jugador": 0,
        "carton_jugador2": 0,
        "turno": 1,
        "ultima_carta": None,
        "ultimo_jugador": None,
        "ganador": None,
        "evento": "",
    }
