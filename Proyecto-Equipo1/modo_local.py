import random

print("BIENVENIDO AL JUEGO DE ADIVINAR EL NÚMERO")

quiere_jugar = input("¿Quieres jugar a adivinar el número? (si/no): ").lower()

while quiere_jugar == "si" or quiere_jugar == "sí":
    
    print("\n--- SELECCIÓN DE NIVEL ---")
    print("1. Fácil (Número del 1 al 50)")
    print("2. Medio (Número del 1 al 100)")
    print("3. Difícil (Número del 1 al 1000)")
    
    entrada_nivel = input("Elige un nivel (1, 2 o 3): ").lower()
    
    if entrada_nivel == "1" or entrada_nivel == "uno":
        limite_superior = 50
        print("Has elegido nivel Fácil.")
    elif entrada_nivel == "2" or entrada_nivel == "dos":
        limite_superior = 100
        print("Has elegido nivel Medio.")
    elif entrada_nivel == "3" or entrada_nivel == "tres":
        limite_superior = 1000
        print("Has elegido nivel Difícil.")
    else:
        print("Opción no válida. Seleccionando dificultad por defecto (Medio).")
        limite_superior = 100
        
    numero_secreto = random.randint(1, limite_superior)
    intentos = 0
    adivinado = False
    
    print("¡Listo! He pensado un número entre 1 y " + str(limite_superior))
    print("Recuerda: debes ingresar solo números enteros, no se permiten letras.")
    
    while adivinado == False:
        entrada_usuario = input("Introduce tu número: ")
        
        try:
            intento_usuario = int(entrada_usuario)
        except ValueError:
            print("¡Error! Eso no es un número válido. Por favor, ingresa solo números, no letras.")
            continue  
            
        intentos = intentos + 1
        
        if intento_usuario == numero_secreto:
            print("¡Felicidades! Has acertado el número en " + str(intentos) + " intentos.")
            adivinado = True
        elif intento_usuario < numero_secreto:
            print("El número secreto es mayor. ¡Prueba otra vez!")
        else:
            print("El número secreto es menor. ¡Prueba otra vez!")
            
    print("\n--- Partida terminada ---")
    quiere_jugar = input("¿Quieres volver a jugar? (si/no): ").lower()

print("Gracias por usar el programa. ¡Hasta luego!")