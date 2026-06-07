#LÓGICA BASE DE JUEGO DE PENALES [Balseca, Choez y Estévez]#

#Variables de Lógica
penales_pateados = 0
penales_restantes = 10
contador_j1 = 0
contador_j2 = 0

#Elección de Equipo de Cada Jugador
EQUIPO_1 = input("JUGADOR 1, INGRESA TU SELECCIÓN: ")
EQUIPO_2 = input("JUGADOR 2, INGRESA TU SELECCIÓN: ")

#Penales regulares

tanda = True

while tanda:

    #Input de Decisión Jugador 1
    decision_j1 = int(input(f"TURNO DE {EQUIPO_1} [PATEA]: "))
    decision_j2 = int(input(f"TURNO DEL {EQUIPO_2} [TAPA]: "))

    if decision_j1 != decision_j2:
        contador_j1 += 1
        print(f"{EQUIPO_1} HA MARCADO GOL!")
    else:
        print(f"{EQUIPO_2} HA PARADO EL PENAL!")

    print(f"{EQUIPO_1} [{contador_j1}] vs [{contador_j2}] {EQUIPO_2}")

    penales_pateados += 1
    penales_restantes -= 1

    diferencia = abs(contador_j1 - contador_j2)

    #Comprobación de Ganador Antes de Tiempo
    penales_por_equipo = penales_restantes // 2

    if diferencia > penales_por_equipo + 1:
        if contador_j1 > contador_j2:
            ganador = EQUIPO_1
        else:
            ganador = EQUIPO_2

        print(f"EL CAMPEÓN DEL MUNDO ES {ganador}!!!")

        tanda = False
        continue

    #Input de Decisión Jugador 2
    decision_j2 = int(input(f"TURNO DE {EQUIPO_2} [PATEA]: "))
    decision_j1 = int(input(f"TURNO DEL {EQUIPO_1} [TAPA]: "))

    if decision_j2 != decision_j1:
        contador_j2 += 1
        print(f"{EQUIPO_2} HA MARCADO GOL!")
    else:
        print(f"{EQUIPO_1} HA PARADO EL PENAL!")

    print(f"{EQUIPO_1} [{contador_j1}] vs [{contador_j2}] {EQUIPO_2}")

    penales_pateados += 1
    penales_restantes -= 1

    diferencia = abs(contador_j1 - contador_j2)

    #Comprobación de Ganador Después de Cada Penal
    penales_por_equipo = penales_restantes // 2

    if diferencia > penales_por_equipo or (penales_pateados == 10 and diferencia != 0):
        if contador_j1 > contador_j2:
            ganador = EQUIPO_1
        else:
            ganador = EQUIPO_2

        print(f"EL CAMPEÓN DEL MUNDO ES {ganador}!!!")
        
        tanda = False

#TANDA EXTRA DE PENALES

    elif penales_pateados == 10 and diferencia == 0:
        print ("VAMOS A TANDA EXTRA!!")

        while True:
            penales_pateados = 0
            penales_restantes = 2

            while diferencia == 0:

                #Input de Decisión Jugador 1
                decision_j1 = int(input(f"TURNO DE {EQUIPO_1} [PATEA]: "))
                decision_j2 = int(input(f"TURNO DEL {EQUIPO_2} [TAPA]: "))

                if decision_j1 != decision_j2:
                    contador_j1 += 1
                    print(f"{EQUIPO_1} HA MARCADO GOL!")
                else:
                    print(f"{EQUIPO_2} HA PARADO EL PENAL!")

                print(f"{EQUIPO_1} [{contador_j1}] vs [{contador_j2}] {EQUIPO_2}")

                penales_pateados += 1
                penales_restantes -= 1

                #Input de Decisión Jugador 2
                decision_j2 = int(input(f"TURNO DE {EQUIPO_2} [PATEA]: "))
                decision_j1 = int(input(f"TURNO DEL {EQUIPO_1} [TAPA]: "))

                #Comprobación de Ganador Después de Cada Penal Extra
                if decision_j2 != decision_j1:
                    contador_j2 += 1
                    print(f"{EQUIPO_2} HA MARCADO GOL!")
                else:
                    print(f"{EQUIPO_1} HA PARADO EL PENAL!")

                print(f"{EQUIPO_1} [{contador_j1}] vs [{contador_j2}] {EQUIPO_2}")

                penales_pateados += 1
                penales_restantes -= 1
                diferencia = abs(contador_j1 - contador_j2)

                if contador_j1 > contador_j2:
                    ganador = EQUIPO_1
                elif contador_j2 > contador_j1:
                    ganador = EQUIPO_2
            

            #Mostrar el Resultado
            print (f"EL CAMPEÓN DEL MUNDO ES {ganador}!!!")

            break
        tanda = False
