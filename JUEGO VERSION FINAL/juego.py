import random
from game_logic import determinar_ganador
opciones = ["piedra", "papel", "tijera"]
print("=== PIEDRA, PAPEL O TIJERA ===")
print("1. Jugar contra la computadora")
jugador = input("Elige piedra, papel o tijera: ").lower()
if jugador not in opciones:
    print("Opción inválida.")
else:
    computadora = random.choice(opciones)
    print("Tú elegiste:", jugador)
    print("Computadora eligió:", computadora)
    resultado = determinar_ganador(jugador, computadora)
    if resultado == "Gana Jugador 1":
        print("Ganaste.")
    elif resultado == "Gana Jugador 2":
        print("Perdiste.")
    else:
        print("Empate.")