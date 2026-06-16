import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logica.game40 import Game40
from logica.mazo import crear_mazo, texto_valor, nombre_carta, PALOS, VALORES
from logica.reglas40 import (
    buscar_captura, es_caida, es_limpia, mayor_carton,
    PUNTOS_CAIDA, PUNTOS_LIMPIA, PUNTOS_CARTON, META,
)

__all__ = [
    "Game40",
    "crear_mazo", "texto_valor", "nombre_carta", "PALOS", "VALORES",
    "buscar_captura", "es_caida", "es_limpia", "mayor_carton",
    "PUNTOS_CAIDA", "PUNTOS_LIMPIA", "PUNTOS_CARTON", "META",
]
