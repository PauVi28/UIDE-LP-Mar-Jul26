print("=== JUEGO DE ADIVINAR EL NÚMERO ===")

print("1. Iniciar Servidor")
print("2. Iniciar Cliente")

opcion = input("Seleccione una opción: ")

if opcion == "1":

    import server

elif opcion == "2":

    import client

else:

    print("Opción inválida")S