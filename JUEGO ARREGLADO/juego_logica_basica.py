import random
opciones = ["piedra", "papel", "tijera"]
print("=== JUEGO: PIEDRA, PAPEL O TIJERA ===")
print("Opciones disponibles: piedra, papel, tijera")
jugador = input("Elige una opción: ").lower()
computadora = random.choice(opciones)
print("Tú elegiste:", jugador)
print("La computadora eligió:", computadora)
if jugador not in opciones:
    print("Opción inválida. Debes escribir piedra, papel o tijera.")
elif jugador == computadora:
    print("Empate.")
elif jugador == "piedra" and computadora == "tijera":
    print("Ganaste.")
elif jugador == "papel" and computadora == "piedra":
    print("Ganaste.")
elif jugador == "tijera" and computadora == "papel":
    print("Ganaste.")
else:
    print("Perdiste.")