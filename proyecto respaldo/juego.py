import random
from game_logic import determinar_ganador

def mostrar_menu():
    print("\n=== BIENVENIDO A PIEDRA, PAPEL O TIJERA ===")
    print("1. Modo Local (Contra la IA)")
    print("2. Modo Multijugador (Conectarse a Servidor)")
    print("3. Salir")
    return input("Selecciona una opción: ")

def jugar_local():
    opciones = ['piedra', 'papel', 'tijera']
    print("\n--- MODO LOCAL ---")

    jugada_usuario = input("Elige (piedra, papel, tijera): ").lower().strip()
    if jugada_usuario not in opciones:
        print("Opción no válida. Intenta de nuevo.")
        return

    jugada_ia = random.choice(opciones)
    print(f"La IA eligió: {jugada_ia}")

    resultado = determinar_ganador(jugada_usuario, jugada_ia)

    if resultado == "empate":
        print("¡Es un empate!")
    elif resultado == "ganas":
        print("¡Felicidades, ganaste!")
    else:
        print("Perdiste... Inténtalo de nuevo.")

if __name__ == "__main__":
    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            jugar_local()
        elif opcion == "2":
            print("\n[INFO] Para jugar multijugador, corre 'server.py' primero y luego 'client.py'.")
        elif opcion == "3":
            print("¡Gracias por jugar!")
            break
        else:
            print("Opción inválida.")
