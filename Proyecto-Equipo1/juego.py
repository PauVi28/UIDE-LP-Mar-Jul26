print("=== JUEGO DE ADIVINAR EL NÚMERO ===")

print("1. Modo Local")
print("2. Iniciar Servidor")
print("3. Iniciar Cliente")
opcion = input("Seleccione una opción: ")

if opcion == "1":
    import modo_local
elif opcion == "2":
    import server
elif opcion == "3":
    import client
else:
    print("Opción inválida")
