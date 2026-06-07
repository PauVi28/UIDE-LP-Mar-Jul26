#CÓDIGO DEL JUEGO SERVER

import pygame
import socket
import threading
import random

#---------------------------------------------------SERVER INICIADO--------------------------------------------------------
HOST = "127.0.0.1"
PORT = 6767

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

pygame.init() #Inicia Pygame

from pygame.locals import( #Importar Controles
    K_LEFT,
    K_RIGHT,
    K_a,
    K_d,
    K_RETURN,
    KEYDOWN,
    QUIT
)

#---------------------------------------------------VARIABLES-----------------------------------------------------

RESOLUCION = (1080, 630) #Resolución de la Ventana en Pixeles


    #Pantalla en Ventana
pantalla = pygame.display.set_mode(RESOLUCION)
pygame.display.set_caption("Mundialinho De Penales 2026 😎 (SERVER)")

pantalla.fill((2, 37, 69))

fuente_temporal = pygame.font.SysFont(None, 60)
texto_carga = fuente_temporal.render("CARGANDO...", True, (255, 255, 255))
pantalla.blit(texto_carga, (380, 290))
pygame.display.update()

    #Fuentes
fuente_1 = pygame.font.Font("RECURSOS/PressStart2P.ttf", 15)
fuente_2 = pygame.font.Font("RECURSOS/PressStart2P.ttf", 18)
fuente_3 = pygame.font.Font("RECURSOS/PressStart2P.ttf", 25)
fuente_4 = pygame.font.Font("RECURSOS/PressStart2P.ttf", 28)
fuente_5 = pygame.font.Font("RECURSOS/PressStart2P.ttf", 40)


    #Fondos e Imágenes
logo_juego = pygame.image.load("RECURSOS/LOGO_JUEGO.png").convert_alpha()
logo_juego = pygame.transform.scale(logo_juego, (700, 350))

    #Fondo Escenas

def cargar_fondo(ruta):
    imagen = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(imagen, (1080, 630))

fondo_arco = cargar_fondo("RECURSOS/ARCO.jpg")
fondo_penal = cargar_fondo("RECURSOS/FONDO_PENAL.jpg")

fondo_gol = cargar_fondo("RECURSOS/fondo_gol.jpg")
fondo_atajado = cargar_fondo("RECURSOS/fondo_atajado.jpg")
fondo_notapado = cargar_fondo("RECURSOS/fondo_notapado.jpg")
fondo_atajado_feliz = cargar_fondo("RECURSOS/fondo_atajado_feliz.jpg")

fondo_ganador = cargar_fondo("RECURSOS/fondo_ganador.jpg")

fondo_mensaje = cargar_fondo("RECURSOS/fondo_mensaje.jpg")

    #Banderas y Nombres

def cargar_bandera(ruta):
    imagen = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(imagen, (150, 90))

band_ecuador = cargar_bandera("RECURSOS/banderaECU.png")
band_argentina = cargar_bandera("RECURSOS/banderaARG.png")
band_portugal = cargar_bandera("RECURSOS/banderaPOR.png")
band_españa = cargar_bandera("RECURSOS/banderaESP.png")
band_francia = cargar_bandera("RECURSOS/banderaFRA.png")
band_brasil = cargar_bandera("RECURSOS/banderaBRA.png")

        #Monedas
def cargar_monedas(ruta):
    imagen = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(imagen, (100, 100))

moneda1 = cargar_monedas("RECURSOS/moneda1.png")
moneda2 = cargar_monedas("RECURSOS/moneda2.png")
moneda3 = cargar_monedas("RECURSOS/moneda3.png")

        #Fotogramas Animación
def cargar_personaje(ruta):
    imagen = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(imagen, (150, 180))
            
            #Fotogramas Jugador
jugador_f1 = cargar_personaje("RECURSOS/ANIMACION/jugador_f1.png")
jugador_f2 = cargar_personaje("RECURSOS/ANIMACION/jugador_f2.png")
jugador_f3 = cargar_personaje("RECURSOS/ANIMACION/jugador_f3.png")
jugador_f4 = cargar_personaje("RECURSOS/ANIMACION/jugador_f4.png")
jugador_f5 = cargar_personaje("RECURSOS/ANIMACION/jugador_f5.png")
jugador_f6 = cargar_personaje("RECURSOS/ANIMACION/jugador_f6.png")
jugador_f7_FELIZ = cargar_personaje("RECURSOS/ANIMACION/jugador_f7_FELIZ.png")
jugador_f7_TRISTE = cargar_personaje("RECURSOS/ANIMACION/jugador_f7_TRISTE.png")

            #Fotogramas Arquero
arquero_f1 = cargar_personaje("RECURSOS/ANIMACION/arq_1.png")
arquero_f2_izq = cargar_personaje("RECURSOS/ANIMACION/arq_izq.png")
arquero_f2_med = cargar_personaje("RECURSOS/ANIMACION/arq_med.png")
arquero_f2_der = cargar_personaje("RECURSOS/ANIMACION/arq_der.png")

            #Balón
balón = pygame.image.load("RECURSOS/ANIMACION/balon.png").convert_alpha()
pygame.transform.scale(balón, (5, 5))

        #Bolitas de Resultado
bolita_verde = pygame.image.load("RECURSOS/bolita_verde.png").convert_alpha()
pygame.transform.scale(bolita_verde, (62, 62))

bolita_roja = pygame.image.load("RECURSOS/bolita_roja.png").convert_alpha()
pygame.transform.scale(bolita_roja, (62, 62))



    #Escena Inicial
escena = "menu_principal"
modo_local = False

    #Conexión
conectado = False
buscando_conexión = False
dirección = None
conexión = None

        #Confirmación en Conexión
confirmado_continuar = False
rival_confirma_continuar = False
contador_confirmado = 0

    #Escena Selección Equipos

paises = ["Ecuador", "Argentina", "Portugal", "España", "Francia", "Brasil"]
banderas_paises = {"Ecuador" : band_ecuador,
                   "Argentina" : band_argentina,
                   "Portugal" : band_portugal,
                   "España" : band_españa,
                   "Francia" : band_francia,
                   "Brasil" : band_brasil}

indice_j1 = 0
indice_j2 = 0

confirmacion_j1 = False
confirmacion_j2 = False

pais_j1 = None
pais_j2 = None

error_paises_iguales = False
selecciones_confirmadas = False

    #Sorteo
primer_turno = 0
sorteo_hecho = False


    #Lógica Penales

decision_j1 = None
decision_j2 = None

penales_pateados = 0
penales_restantes = 10

contador_j1 = 0
contador_j2 = 0

resultado_penales_j1 = []
resultado_penales_j2 = []

pateador_actual = 0
penal_online_resuelto = False

confirmacion_online_j1 = False
confirmacion_online_j2 = False

modo_tanda_extra = False

ganador = None

        #Tanda extra
gol_extra_j1 = None
gol_extra_j2 = None
tiempo_mensaje_tanda_extra = 0


def resolver_penal_online():
    global contador_j1, contador_j2, penal_online_resuelto, escena, tiempo_animacion_penal
    global penales_pateados, penales_restantes, ganador
    global gol_extra_j1, gol_extra_j2, resultado_penales_j1, resultado_penales_j2

    if penal_online_resuelto:
        return

    if decision_j1 is None or decision_j2 is None:
        return

    gol = decision_j1 != decision_j2
    if not modo_tanda_extra:
        if pateador_actual == 1:
            resultado_penales_j1.append(gol)
        elif pateador_actual == 2:
            resultado_penales_j2.append(gol)

    if gol:
        if pateador_actual == 1:
            contador_j1 += 1
        elif pateador_actual == 2:
            contador_j2 += 1

    if modo_tanda_extra:
        if pateador_actual == 1:
            gol_extra_j1 = gol
        elif pateador_actual == 2:
            gol_extra_j2 = gol

        verificar_ganador_extra()

    else:
        penales_pateados += 1
        penales_restantes -= 1
        verificar_ganador()

    penal_online_resuelto = True

    if conectado:
        lista_j1 = "".join(["1" if x else "0" for x in resultado_penales_j1])
        lista_j2 = "".join(["1" if x else "0" for x in resultado_penales_j2])

        mensaje = f"RESULTADO_PENAL:{contador_j1},{contador_j2},{decision_j1},{decision_j2},{pateador_actual},{penales_pateados},{penales_restantes},{ganador},{int(modo_tanda_extra)},{lista_j1},{lista_j2}|"
        
        conexión.sendall(mensaje.encode("utf-8"))

    escena = "animacion_penal"
    tiempo_animacion_penal = pygame.time.get_ticks()

def verificar_ganador():
    global ganador

    if primer_turno == 1:
        tiros_j1 = (penales_pateados + 1) // 2
        tiros_j2 = penales_pateados // 2
    else:
        tiros_j2 = (penales_pateados + 1) // 2
        tiros_j1 = penales_pateados // 2

    restantes_j1 = 5 - tiros_j1
    restantes_j2 = 5 - tiros_j2

    if penales_pateados >= 10:
        if contador_j1 > contador_j2:
            ganador = 1
        elif contador_j2 > contador_j1:
            ganador = 2
        else:
            ganador = 0
        return

    if contador_j1 > contador_j2 + restantes_j2:
        ganador = 1

    elif contador_j2 > contador_j1 + restantes_j1:
        ganador = 2

def verificar_ganador_extra():
    global ganador, gol_extra_j1, gol_extra_j2

    if gol_extra_j1 is None or gol_extra_j2 is None:
        return

    if gol_extra_j1 and not gol_extra_j2:
        ganador = 1

    elif gol_extra_j2 and not gol_extra_j1:
        ganador = 2

    else:
        gol_extra_j1 = None
        gol_extra_j2 = None
     
def dibujar_bolitas_resultado():
    x_izq = 83
    x_der = 638
    y = 471
    espacio = 74
    if primer_turno == 1:
        lista_izq = resultado_penales_j1
        lista_der = resultado_penales_j2
    else:
        lista_izq = resultado_penales_j2
        lista_der = resultado_penales_j1

    for i in range(5):
        if i < len(lista_izq):
            if lista_izq[i]:
                pantalla.blit(bolita_verde, (x_izq + i * espacio, y))
            else:
                pantalla.blit(bolita_roja, (x_izq + i * espacio, y))

        if i < len(lista_der):
            if lista_der[i]:
                pantalla.blit(bolita_verde, (x_der + i * espacio, y))
            else:
                pantalla.blit(bolita_roja, (x_der + i * espacio, y))

    #Botones
boton_local_menu = pygame.Rect(354, 330, 320, 120)
boton_online_menu = pygame.Rect(354, 470, 320, 120)

boton_volver_selección = pygame.Rect(40, 550, 130, 50)
boton_continuar_selección = pygame.Rect(850, 550, 190, 50)

boton_volver_conexion = pygame.Rect(50, 500, 220, 80)
boton_continuar_conexión = pygame.Rect(812, 500, 220, 80)

boton_confirmar_seleccion1 = pygame.Rect(190, 400, 220, 80)
boton_confirmar_seleccion2 = pygame.Rect(650, 400, 220, 80)

boton_continuar_sorteo = pygame.Rect(850, 550, 190, 50)


boton_izq_arco = pygame.Rect(280, 200, 150, 250)
boton_med_arco = pygame.Rect(450, 200, 150, 250)
boton_der_arco = pygame.Rect(620, 200, 150, 250)

color_transparente = (235, 155, 0, 170)
color_transparente_encima = (173, 102, 16, 170)

def botones_transparentes(superficie_destino, color, rect):
    superficie_boton = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    superficie_boton.fill(color)
    superficie_destino.blit(superficie_boton, (rect.x, rect.y))

#---------------------------------------------------------CONEXIÓN SOCKETS TCP-------------------------------------------------------
def esperando_cliente():
    global conectado, conexión, dirección, buscando_conexión, rival_confirma_continuar, indice_j2, confirmacion_j1, confirmacion_j2, pais_j1, pais_j2, escena, tiempo_animacion_moneda, tiempo_vs, confirmacion_online_j2, confirmacion_online_j1, decision_j1, decision_j2, tiempo_animacion_penal

    servidor.settimeout(1.0)
    while buscando_conexión:
        if not conectado:
            try:
                conexión, dirección = servidor.accept()
                conexión.settimeout(1.0)
                conexión.sendall(b"CONECTADO|")
                conectado = True

            except socket.timeout:
                pass
        else:
            try:
                datos = conexión.recv(1024)
                if not datos:
                    raise ConnectionResetError("El cliente cerró su ventana")
                else:
                    mensajes = datos.decode("utf-8").split("|")

                    for mensaje in mensajes:
                        if mensaje == "":
                            continue

                            #Escena Continuar en Conexión
                        if mensaje == "CONTINUAR CONFIRMADO":
                            rival_confirma_continuar = True
                        elif mensaje == "CONTINUAR DESCONFIRMADO":
                            rival_confirma_continuar = False

                            #Elección Países
                        elif mensaje.startswith("J2_SEL:"):
                            indice_j2 = int(mensaje.split(":")[1])
                        
                        elif mensaje == "J2_CONFIRMA":
                            confirmacion_j2 = True
                            pais_j2 = paises[indice_j2]
                        elif mensaje == "J2_DESCONFIRMA":
                            confirmacion_j2 = False
                            pais_j2 = None
                        elif mensaje == "IR_A_SORTEO":
                            escena = "sorteo"
                            tiempo_animacion_moneda = pygame.time.get_ticks()

                            #Sorteo
                        elif mensaje == "INICIAR_PARTIDO":
                            escena = "versus"
                            tiempo_vs = pygame.time.get_ticks()

                            #Penales
                        elif mensaje == "J2_TAPA_IZQUIERDA" or mensaje == "J2_PATEA_IZQUIERDA":
                            decision_j2 = 1
                            confirmacion_online_j2 = True
                        elif mensaje == "J2_TAPA_MEDIO" or mensaje == "J2_PATEA_MEDIO":
                            decision_j2 = 2
                            confirmacion_online_j2 = True
                        elif mensaje == "J2_TAPA_DERECHA" or mensaje == "J2_PATEA_DERECHA":
                            decision_j2 = 3
                            confirmacion_online_j2 = True

                        elif mensaje == "IR_A_ANIMACION":
                            resolver_penal_online()
                                

                        
            
            except socket.timeout:
                pass
            except (ConnectionResetError, ConnectionAbortedError, OSError):
                if conexión:
                    conexión.close()
                conectado = False
                rival_confirma_continuar = False


#--------------------------------------------------------JUEGOS, EVENTOS Y LÓGICA----------------------------------------------------
juego_abierto = True
while juego_abierto:
    posicion_mouse = pygame.mouse.get_pos()

    contador_confirmado = (1 if confirmado_continuar else 0) + (1 if rival_confirma_continuar else 0)

            
    if escena == "menu_principal":
        modo_local = False
        sorteo_hecho = False
        primer_turno = 0

        indice_j1 = 0
        indice_j2 = 0
        confirmacion_j1 = False
        confirmacion_j2 = False
        pais_j1 = None
        pais_j2 = None

        contador_j1 = 0
        contador_j2 = 0
        decision_j1 = None
        decision_j2 = None

        penales_pateados = 0
        penales_restantes = 10
        pateador_actual = 0

        ganador = None
        modo_tanda_extra = False
        gol_extra_j1 = None
        gol_extra_j2 = None
        tiempo_mensaje_tanda_extra = 0

        penal_online_resuelto = False
        confirmacion_online_j1 = False
        confirmacion_online_j2 = False

        resultado_penales_j1 = []
        resultado_penales_j2 = []

    elif escena == "conectando" and contador_confirmado == 2:
        escena = "seleccion_equipos"
        confirmado_continuar = False
        rival_confirma_continuar = False

    elif escena == "seleccion_equipos":
        if confirmacion_j1 and confirmacion_j2:
            if pais_j1 == pais_j2:
                error_paises_iguales = True
                selecciones_confirmadas = False

                confirmacion_j1 = False
                confirmacion_j2 = False
                pais_j1 = None
                pais_j2 = None

                if not modo_local and conectado:
                    conexión.sendall(b"J1_DESCONFIRMA|")
            else:
                error_paises_iguales = False
                selecciones_confirmadas = True
        else:
            selecciones_confirmadas = False

    if not modo_local and (escena == "j1_PATEA" or escena == "j1_TAPA"):
        resolver_penal_online()

    


    for evento in pygame.event.get():

            #Cerrar el juego
        if evento.type == pygame.QUIT:
            juego_abierto = False

            #Eventos Tecla
        if evento.type == KEYDOWN:
            if escena == "seleccion_equipos":
                if modo_local:
                    if not confirmacion_j1:
                        if evento.key == K_a:
                            indice_j1 = (indice_j1 - 1) % len(paises)
                        if evento.key == K_d:
                            indice_j1 = (indice_j1 + 1) % len(paises)
                        if evento.key == K_a or evento.key == K_d:
                            if paises[indice_j1] != paises[indice_j2]:
                                error_paises_iguales = False

                    if not confirmacion_j2:
                        if evento.key == K_LEFT:
                            indice_j2 = (indice_j2 - 1) % len(paises)
                        if evento.key == K_RIGHT:
                            indice_j2 = (indice_j2 + 1) % len(paises)
                        if evento.key == K_LEFT or evento.key == K_RIGHT:
                            if paises[indice_j1] != paises[indice_j2]:
                                error_paises_iguales = False
                else:
                    if not confirmacion_j1:
                        if evento.key == K_a or evento.key == K_LEFT:
                            indice_j1 = (indice_j1 - 1) % len(paises)
                            if conectado:
                                conexión.sendall(f"J1_SEL:{indice_j1}".encode("utf-8"))
                        if evento.key == K_d or evento.key == K_RIGHT:
                            indice_j1 = (indice_j1 + 1) % len(paises)
                            if conectado: 
                                conexión.sendall(f"J1_SEL:{indice_j1}|".encode("utf-8"))
                        if evento.key == K_a or evento.key == K_d or evento.key == K_LEFT or evento.key == K_RIGHT:
                            if paises[indice_j1] != paises[indice_j2]:
                                error_paises_iguales = False

        

            #Eventos Click
        if evento.type == pygame.MOUSEBUTTONDOWN:
                #Botón Volver
            if escena != "menu_principal" and escena != "conectando":
                if boton_volver_selección.collidepoint(evento.pos):
                    escena = "menu_principal"

            #MENU
            if escena == "menu_principal":
                if boton_local_menu.collidepoint(evento.pos):
                    escena = "seleccion_equipos"
                    modo_local = True

                elif boton_online_menu.collidepoint(evento.pos):
                    escena = "conectando"

                    if not conectado and not buscando_conexión:
                        buscando_conexión = True
                        hilo_red = threading.Thread(target=esperando_cliente, daemon=True)
                        hilo_red.start()
            
            #SELECCIÓN EQUIPOS
            elif escena == "seleccion_equipos":
                if modo_local:
                    if boton_confirmar_seleccion1.collidepoint(evento.pos):
                        if not confirmacion_j1:
                            pais_j1 = paises[indice_j1]
                            confirmacion_j1 = True
                        else:
                            pais_j1 = None
                            confirmacion_j1 = False
                    elif boton_confirmar_seleccion2.collidepoint(evento.pos):
                        if not confirmacion_j2:
                            pais_j2 = paises[indice_j2]
                            confirmacion_j2 = True
                        else:
                            pais_j2 = None
                            confirmacion_j2 = False

                    if selecciones_confirmadas:
                        if boton_continuar_selección.collidepoint(evento.pos):
                            escena = "sorteo"
                            tiempo_animacion_moneda = pygame.time.get_ticks()

                else:
                    if boton_confirmar_seleccion1.collidepoint(evento.pos):
                        if not confirmacion_j1:
                            pais_j1 = paises[indice_j1]
                            confirmacion_j1 = True
                            if conectado:
                                conexión.sendall(b"J1_CONFIRMA|")
                        else:
                            pais_j1 = None
                            confirmacion_j1 = False
                            if conectado:
                                conexión.sendall(b"J1_DESCONFIRMA|")

                    if selecciones_confirmadas:
                        if boton_continuar_selección.collidepoint(evento.pos):
                            escena = "sorteo"
                            if conectado:
                                conexión.sendall(b"IR_A_SORTEO|")
                                tiempo_animacion_moneda = pygame.time.get_ticks()
                                
            #SORTEO
            elif escena == "sorteo":
                if sorteo_hecho and boton_continuar_sorteo.collidepoint(evento.pos):
                    escena = "versus"
                    tiempo_vs = pygame.time.get_ticks()
                        
                    if not modo_local and conectado:
                        conexión.sendall(b"INICIAR_PARTIDO|")

            #J1 PATEA
            elif escena == "j1_PATEA":
                
                if decision_j1 is None:
                    if boton_izq_arco.collidepoint(evento.pos): decision_j1 = 1
                    elif boton_med_arco.collidepoint(evento.pos): decision_j1 = 2
                    elif boton_der_arco.collidepoint(evento.pos): decision_j1 = 3

                if modo_local and decision_j1 is not None:
                    escena = "j2_TAPA"
                    tiempo_animacion_penal = pygame.time.get_ticks()

                elif not modo_local and decision_j1 is not None and not penal_online_resuelto:
                    if decision_j1 == 1: conexión.sendall(b"J1_PATEA_IZQUIERDA|")
                    elif decision_j1 == 2: conexión.sendall(b"J1_PATEA_MEDIO|")
                    elif decision_j1 == 3: conexión.sendall(b"J1_PATEA_DERECHA|")
                    resolver_penal_online()
                    

            #J2 TAPA
            elif escena == "j2_TAPA":
                pateador_actual = 1
                
                if decision_j2 is None:
                    if boton_izq_arco.collidepoint(evento.pos): decision_j2 = 1
                    elif boton_med_arco.collidepoint(evento.pos): decision_j2 = 2
                    elif boton_der_arco.collidepoint(evento.pos): decision_j2 = 3

                if modo_local  and decision_j2 is not None:
                    escena = "animacion_penal"
                    tiempo_animacion_penal = pygame.time.get_ticks()

                    gol = decision_j1 != decision_j2
                    if not modo_tanda_extra:
                        resultado_penales_j1.append(gol)

                    if gol:
                        contador_j1 += 1

                    if modo_tanda_extra:
                        gol_extra_j1 = gol
                        verificar_ganador_extra()
                    else:
                        penales_restantes -= 1
                        penales_pateados += 1
                        verificar_ganador()
                
            #J2 PATEA
            elif escena == "j2_PATEA":
                pateador_actual = 2
                
                if decision_j2 is None:
                    if boton_izq_arco.collidepoint(evento.pos):decision_j2 = 1
                    elif boton_med_arco.collidepoint(evento.pos): decision_j2 = 2
                    elif boton_der_arco.collidepoint(evento.pos):decision_j2 = 3

                if modo_local and decision_j2 is not None:
                    escena = "j1_TAPA"
                    tiempo_animacion_penal = pygame.time.get_ticks()

            #J1 TAPA
            elif escena == "j1_TAPA":
                
                
                if decision_j1 is None:
                    if boton_izq_arco.collidepoint(evento.pos): decision_j1 = 1
                    elif boton_med_arco.collidepoint(evento.pos): decision_j1 = 2
                    elif boton_der_arco.collidepoint(evento.pos): decision_j1 = 3

                if modo_local and decision_j1 is not None:
                    escena = "animacion_penal"
                    tiempo_animacion_penal = pygame.time.get_ticks()

                    gol = decision_j1 != decision_j2
                    if not modo_tanda_extra:
                        resultado_penales_j2.append(gol)

                    if gol:
                        contador_j2 += 1

                    if modo_tanda_extra:
                        gol_extra_j2 = gol
                        verificar_ganador_extra()
                    else:
                        penales_restantes -= 1
                        penales_pateados += 1
                        verificar_ganador()


                elif not modo_local and decision_j1 is not None and not penal_online_resuelto:
                    if decision_j1 == 1: conexión.sendall(b"J1_TAPA_IZQUIERDA|")
                    elif decision_j1 == 2: conexión.sendall(b"J1_TAPA_MEDIO|")
                    elif decision_j1 == 3: conexión.sendall(b"J1_TAPA_DERECHA|")
                    resolver_penal_online()
                    

            #BUSCANDO CONEXIÓN
            elif escena == "conectando":
                if boton_volver_conexion.collidepoint(evento.pos):
                    escena = "menu_principal"
                    buscando_conexión = False
                    

                    if conectado and conexión:
                        conexión.close()
                    conectado = False
            
                elif boton_continuar_conexión.collidepoint(evento.pos):
                    if conectado:
                        if not confirmado_continuar:
                            confirmado_continuar = True
                            conexión.sendall(b"CONTINUAR CONFIRMADO")
                        else:
                            confirmado_continuar = False
                            conexión.sendall(b"CONTINUAR DESCONFIRMADO")
                            

#--------------------------------------------------------------ESCENAS RENDER-------------------------------------------------------------
    
#MENÚ
    if escena == "menu_principal":
        pantalla.fill((2, 37, 69))
        
        color1 = (252, 70, 33)
        color2 = (252, 70, 33)

        if boton_local_menu.collidepoint(posicion_mouse):
            color1 = (255, 108, 82)
        elif boton_online_menu.collidepoint(posicion_mouse):
            color2 = (255, 108, 82)

        pygame.draw.rect(pantalla, color1, boton_local_menu)
        texto = fuente_4.render("PLAY LOCAL", True, (255, 255, 255))
        pantalla.blit(texto, (380, 375))

        pygame.draw.rect(pantalla, color2, boton_online_menu)
        texto = fuente_4.render("PLAY ONLINE", True, (255, 255, 255))
        pantalla.blit(texto, (362, 515))

        texto = fuente_2.render("MODO SERVIDOR", True, (255, 255, 255))
        pantalla.blit(texto, (20, 600))
        

        pantalla.blit(logo_juego, (180,-20))


#BUSCANDO CONEXIÓN
    elif escena == "conectando":
        pantalla.fill((2, 37, 69))


        color1 = (252, 70, 33)
        color2 = (252, 70, 33)
        if boton_volver_conexion.collidepoint(posicion_mouse):
            color1 = (255, 108, 82)
        elif boton_continuar_conexión.collidepoint(posicion_mouse):
            color2 = (255, 108, 82)

        pygame.draw.rect(pantalla, color1, boton_volver_conexion)
        texto = fuente_3.render("VOLVER", True, (255, 255, 255))
        pantalla.blit(texto, (85, 530))


        if not conectado:
            texto = fuente_5.render("BUSCANDO CLIENTE...", True, (255, 255, 255))
            pantalla.blit(texto, (206, 230))
        else:
            texto = fuente_4.render("CONTECTADO CON EL JUGADOR 2", True, (255, 255, 255))
            pantalla.blit(texto, (180, 230))
            texto = fuente_5.render(f"DESDE {dirección[0]}", True, (255, 255, 255))
            pantalla.blit(texto, (206, 300))

            if confirmado_continuar:
                if boton_continuar_conexión.collidepoint(posicion_mouse):
                    color2 = (105, 255, 106)
                else:
                    color2 = (46, 255, 48)

            pygame.draw.rect(pantalla, color2, boton_continuar_conexión)
            texto = fuente_2.render("CONTINUAR", True, (255, 255, 255))
            pantalla.blit(texto, (840, 530))

            texto = fuente_2.render((f"{contador_confirmado}/2"), True, (255, 255, 255))
            pantalla.blit(texto, (890, 480))



#SELECCIÓN DE EQUIPOS
    elif escena == "seleccion_equipos":
        
        pantalla.fill((2, 37, 69))

        pantalla.blit(banderas_paises[paises[indice_j1]], (220, 200))
        pantalla.blit(banderas_paises[paises[indice_j2]], (680, 200))

        texto = fuente_3.render("JUGADOR 1", True , (255, 255, 255))
        pantalla.blit(texto, (185, 150))
        texto = fuente_3.render("JUGADOR 2", True , (255, 255, 255))
        pantalla.blit(texto, (650, 150))

        texto = fuente_5.render("SELECCION DE EQUIPOS", True, (225, 139, 49))
        pantalla.blit(texto, (147, 50))

        

        if not confirmacion_j1:
            color1 = (204, 125, 55)
            
            if boton_confirmar_seleccion1.collidepoint(posicion_mouse):
                color1 = (250, 201, 127)
            
            pygame.draw.rect(pantalla, color1, boton_confirmar_seleccion1)
            texto = fuente_2.render("CONFIRMAR", True, (6, 9, 26))
            pantalla.blit(texto, (220, 430))

        else:
            color1 = (46, 255, 48)
            
            if boton_confirmar_seleccion1.collidepoint(posicion_mouse):
                color1 = (105, 255, 106)
            
            pygame.draw.rect(pantalla, color1, boton_confirmar_seleccion1)
            texto = fuente_2.render("CONFIRMADO", True, (6, 9, 26))
            pantalla.blit(texto, (210, 430))

            

        if not confirmacion_j2:
            color2 = (204, 125, 55)

            if boton_confirmar_seleccion2.collidepoint(posicion_mouse):
                color2 = (250, 201, 127)
            
            pygame.draw.rect(pantalla, color2, boton_confirmar_seleccion2)
            texto = fuente_2.render("CONFIRMAR", True, (6, 9, 26))
            pantalla.blit(texto, (680, 430))

        else:
            color2 = (46, 255, 48)
            
            if boton_confirmar_seleccion2.collidepoint(posicion_mouse):
                color2 = (105, 255, 106)
            
            pygame.draw.rect(pantalla, color2, boton_confirmar_seleccion2)
            texto = fuente_2.render("CONFIRMADO", True, (6, 9, 26))
            pantalla.blit(texto, (670, 430))

        if selecciones_confirmadas:

            color = (252, 70, 33)
            if boton_continuar_selección.collidepoint(posicion_mouse):
                color = (255, 108, 82)

            pygame.draw.rect(pantalla, color, boton_continuar_selección)
            texto = fuente_2.render("CONTINUAR", True, (255, 255, 255))
            pantalla.blit(texto, (865, 566))

        if error_paises_iguales:
            
            texto = fuente_2.render("NO PUEDEN ESCOGER EL MISMO PAIS", True, (255, 26, 26))
            pantalla.blit(texto, (250, 550))


#SORTEO
    elif escena == "sorteo":
        pantalla.fill((116, 208, 227))

        texto = fuente_4.render("SORTEO DE PRIMER PATEADOR", True, (7, 29, 31))
        pantalla.blit(texto, (170, 40))

        if 500 > pygame.time.get_ticks() - tiempo_animacion_moneda > 0:
            pantalla.blit(moneda1, (450, 150))
        
        if 1000 > pygame.time.get_ticks() - tiempo_animacion_moneda > 500:
            pantalla.blit(moneda2, (450, 150))

        if 1500 > pygame.time.get_ticks() - tiempo_animacion_moneda > 1000:
            pantalla.blit(moneda3, (450, 150))

        if pygame.time.get_ticks() - tiempo_animacion_moneda > 1500:
            pantalla.blit(moneda3, (450, 150))
            
            if not sorteo_hecho:
                primer_turno = random.choice((1, 2))
                sorteo_hecho = True

                if not modo_local and conectado:
                    conexión.sendall(f"RESULTADO_SORTEO:{primer_turno}|".encode("utf-8"))
            
            if primer_turno == 1:
                bandera = banderas_paises[paises[indice_j1]]
            else:
                bandera = banderas_paises[paises[indice_j2]]

            pantalla.blit(bandera, (430, 300))
            texto = fuente_5.render("PATEA PRIMERO!!", True, (15, 7, 31))
            pantalla.blit(texto, (250,430))

            color = (252, 70, 33)
            if boton_continuar_selección.collidepoint(posicion_mouse):
                color = (255, 108, 82)

            pygame.draw.rect(pantalla, color, boton_continuar_sorteo)
            texto = fuente_2.render("CONTINUAR", True, (255, 255, 255))
            pantalla.blit(texto, (865, 566))


#ESCENA VS

    elif escena == "versus":
        pantalla.fill((138, 219, 222))

        texto = fuente_5.render("VS", True, (0, 0, 0))
        pantalla.blit(texto, (500, 240))

        if primer_turno == 1:
            pantalla.blit(banderas_paises[paises[indice_j1]], (300, 240))
            pantalla.blit(banderas_paises[paises[indice_j2]], (600, 240))

        else:
            pantalla.blit(banderas_paises[paises[indice_j2]], (300, 240))
            pantalla.blit(banderas_paises[paises[indice_j1]], (600, 240))

        if pygame.time.get_ticks() -  tiempo_vs > 3000:
            if modo_local:
                if primer_turno == 1:
                    escena = "j1_PATEA"
                    decision_j2 = None
                    decision_j1 = None
                else:
                    escena = "j2_PATEA"
                    decision_j2 = None
                    decision_j1 = None
            
            else:
                if primer_turno == 1:
                    escena = "j1_PATEA"
                    pateador_actual = 1
                    decision_j2 = None
                    decision_j1 = None
                    penal_online_resuelto = False
                    confirmacion_online_j1 = False
                    confirmacion_online_j2 = False
                else:
                    escena = "j1_TAPA"
                    pateador_actual = 2
                    decision_j2 = None
                    decision_j1 = None
                    penal_online_resuelto = False
                    confirmacion_online_j1 = False
                    confirmacion_online_j2 = False



#J1_PATEA
    elif escena == "j1_PATEA":
        pantalla.blit(fondo_arco, (0, 0))

        texto = fuente_4.render(f"{pais_j1} PATEA", True, (0, 0, 0))
        pantalla.blit(texto, (350, 50))

        if modo_local:
            texto = fuente_3.render(f"{pais_j2} CIERRA LOS OJOS!", True, (0, 0, 0))
            pantalla.blit(texto, (200, 500))
        else:
            if decision_j1 is not None and not confirmacion_online_j2:
                texto = fuente_3.render(f"ESPERANDO LA DECISIÓN DE {pais_j2}", True, (0, 0, 0))
                pantalla.blit(texto, (120, 500))


        color1 = color_transparente
        color2 = color_transparente
        color3 = color_transparente


        if not decision_j1:
            if boton_izq_arco.collidepoint(posicion_mouse):
                color1 = color_transparente_encima
            elif boton_med_arco.collidepoint(posicion_mouse):
                color2 = color_transparente_encima
            elif boton_der_arco.collidepoint(posicion_mouse):
                color3 = color_transparente_encima

            botones_transparentes(pantalla, color1, boton_izq_arco)
            botones_transparentes(pantalla, color2, boton_med_arco)
            botones_transparentes(pantalla, color3, boton_der_arco)


#J2_PATEA
    elif escena == "j2_PATEA":
        pantalla.blit(fondo_arco, (0, 0))

        texto = fuente_4.render(f"{pais_j2} PATEA", True, (0, 0, 0))
        pantalla.blit(texto, (350, 50))

        if modo_local:
            texto = fuente_4.render(f"{pais_j1} CIERRA LOS OJOS!", True, (0, 0, 0))
            pantalla.blit(texto, (200, 500))

        color1 = color_transparente
        color2 = color_transparente
        color3 = color_transparente

        if not decision_j2:
            if boton_izq_arco.collidepoint(posicion_mouse):
                color1 = color_transparente_encima
            elif boton_med_arco.collidepoint(posicion_mouse):
                color2 = color_transparente_encima
            elif boton_der_arco.collidepoint(posicion_mouse):
                color3 = color_transparente_encima

            botones_transparentes(pantalla, color1, boton_izq_arco)
            botones_transparentes(pantalla, color2, boton_med_arco)
            botones_transparentes(pantalla, color3, boton_der_arco)



#J1_TAPA
    elif escena == "j1_TAPA":
        pantalla.blit(fondo_arco, (0, 0))

        texto = fuente_4.render(f"{pais_j1} TAPA", True, (0, 0, 0))
        pantalla.blit(texto, (350, 50))

        if modo_local:
            texto = fuente_4.render(f"{pais_j2} CIERRA LOS OJOS!", True, (0, 0, 0))
            pantalla.blit(texto, (200, 500))
        else:
            if decision_j1 is not None and not confirmacion_online_j2:
                texto = fuente_3.render(f"ESPERANDO LA DECISIÓN DE {pais_j2}", True, (0, 0, 0))
                pantalla.blit(texto, (120, 500))

        color1 = color_transparente
        color2 = color_transparente
        color3 = color_transparente

        if not decision_j1:
            if boton_izq_arco.collidepoint(posicion_mouse):
                color1 = color_transparente_encima
            elif boton_med_arco.collidepoint(posicion_mouse):
                color2 = color_transparente_encima
            elif boton_der_arco.collidepoint(posicion_mouse):
                color3 = color_transparente_encima

            botones_transparentes(pantalla, color1, boton_izq_arco)
            botones_transparentes(pantalla, color2, boton_med_arco)
            botones_transparentes(pantalla, color3, boton_der_arco)


#J2_TAPA
    elif escena == "j2_TAPA":
        pantalla.blit(fondo_arco, (0, 0))

        texto = fuente_4.render(f"{pais_j2} TAPA", True, (0, 0, 0))
        pantalla.blit(texto, (350, 50))

        if modo_local:
            texto = fuente_4.render(f"{pais_j1} CIERRA LOS OJOS!", True, (0, 0, 0))
            pantalla.blit(texto, (200, 500))

        color1 = color_transparente
        color2 = color_transparente
        color3 = color_transparente

        if not decision_j2:
            if boton_izq_arco.collidepoint(posicion_mouse):
                color1 = color_transparente_encima
            elif boton_med_arco.collidepoint(posicion_mouse):
                color2 = color_transparente_encima
            elif boton_der_arco.collidepoint(posicion_mouse):
                color3 = color_transparente_encima

            botones_transparentes(pantalla, color1, boton_izq_arco)
            botones_transparentes(pantalla, color2, boton_med_arco)
            botones_transparentes(pantalla, color3, boton_der_arco)



#ANIMACIÓN PENAL
    elif escena == "animacion_penal":
        pantalla.blit(fondo_penal, (0,0))

        if 250 > pygame.time.get_ticks() - tiempo_animacion_penal > 0:
            pantalla.blit(arquero_f1, (465, 143))
            pantalla.blit(balón, (522, 433))
            pantalla.blit(jugador_f1, (314, 329))

        if 500 > pygame.time.get_ticks() - tiempo_animacion_penal > 250:
            pantalla.blit(arquero_f1, (465, 143))
            pantalla.blit(balón, (522, 433))
            pantalla.blit(jugador_f2, (387, 315))

        if 750 > pygame.time.get_ticks() - tiempo_animacion_penal > 500:
            pantalla.blit(arquero_f1, (465, 143))
            pantalla.blit(balón, (522, 433))
            pantalla.blit(jugador_f3, (420, 291))
        
        if 1000 > pygame.time.get_ticks() - tiempo_animacion_penal > 750:
            pantalla.blit(arquero_f1, (465, 143))
            pantalla.blit(balón, (522, 433))
            pantalla.blit(jugador_f4, (418, 294))

        if 1250 > pygame.time.get_ticks() - tiempo_animacion_penal > 1000:
            pantalla.blit(arquero_f1, (465, 143))
            pantalla.blit(balón, (522, 433))
            pantalla.blit(jugador_f5, (439, 297))

        if 1500 > pygame.time.get_ticks() - tiempo_animacion_penal > 1250:
            pantalla.blit(arquero_f1, (465, 143))
            pantalla.blit(balón, (522, 326))
            pantalla.blit(jugador_f6, (450, 284))

        if 2900 > pygame.time.get_ticks() - tiempo_animacion_penal > 1500:
            if decision_j1 != decision_j2:
                pantalla.blit(jugador_f7_FELIZ, (511, 290))
            
            else:
                pantalla.blit(jugador_f7_TRISTE, (490, 290))

            if pateador_actual == 1:
                if decision_j2 == 1:
                    pantalla.blit(arquero_f2_izq, (357, 100))
                if decision_j1 == 1:
                    pantalla.blit(balón, (360, 101))
                
                if decision_j2 == 2:
                    pantalla.blit(arquero_f2_med, (465, 133))
                if decision_j1 == 2:
                    pantalla.blit(balón, (522, 201))

                if decision_j2 == 3:
                    pantalla.blit(arquero_f2_der, (540, 108))
                if decision_j1 == 3:
                    pantalla.blit(balón, (683, 118))

            else:
                if decision_j1 == 1:
                    pantalla.blit(arquero_f2_izq, (357, 100))
                if decision_j2 == 1:
                    pantalla.blit(balón, (360, 101))
                
                if decision_j1 == 2:
                    pantalla.blit(arquero_f2_med, (465, 133))
                if decision_j2 == 2:
                    pantalla.blit(balón, (522, 201))

                if decision_j1 == 3:
                    pantalla.blit(arquero_f2_der, (540, 108))
                if decision_j2 == 3:
                    pantalla.blit(balón, (683, 118))

        if pygame.time.get_ticks() - tiempo_animacion_penal > 2900:
            escena = "resultado"
            tiempo_resultado = pygame.time.get_ticks()

#RESULTADO
    elif escena == "resultado":
        if modo_local:
            if decision_j1 != decision_j2:
                pantalla.blit(fondo_gol, (0,0))                                
            else:
                pantalla.blit(fondo_atajado, (0,0))

        else:
            if pateador_actual == 1:
                if decision_j1 != decision_j2:
                    pantalla.blit(fondo_gol, (0,0))
                else:
                    pantalla.blit(fondo_atajado, (0,0))
            else:
                if decision_j1 != decision_j2:
                    pantalla.blit(fondo_notapado, (0,0))
                else:
                    pantalla.blit(fondo_atajado_feliz, (0,0))
     
        if primer_turno == 1:
            pantalla.blit(banderas_paises[paises[indice_j1]], (75, 350))
            texto= fuente_5.render(f"{contador_j1}", True, (255, 255, 255))
            pantalla.blit(texto, (470, 480))

            pantalla.blit(banderas_paises[paises[indice_j2]], (850, 350))
            texto= fuente_5.render(f"{contador_j2}", True, (255, 255, 255))
            pantalla.blit(texto, (570, 480))
        else:
            pantalla.blit(banderas_paises[paises[indice_j2]], (75, 350))
            texto= fuente_5.render(f"{contador_j2}", True, (255, 255, 255))
            pantalla.blit(texto, (470, 480))

            pantalla.blit(banderas_paises[paises[indice_j1]], (850, 350))
            texto= fuente_5.render(f"{contador_j1}", True, (255, 255, 255))
            pantalla.blit(texto, (570, 480))

        dibujar_bolitas_resultado()
            

        if pygame.time.get_ticks() - tiempo_resultado > 3000:

            if ganador == 1 or ganador == 2:
                escena = "ganador"

            elif ganador == 0:
                escena = "mensaje_tanda_extra"
                tiempo_mensaje_tanda_extra = pygame.time.get_ticks()
            else:
                if modo_local:
                    if pateador_actual == 1:
                        escena = "j2_PATEA"
                        decision_j2 = None
                        decision_j1 = None
                    else:
                        escena = "j1_PATEA"
                        decision_j2 = None
                        decision_j1 = None
                else:
                    if pateador_actual == 1:
                        escena = "j1_TAPA"
                        pateador_actual = 2
                        decision_j2 = None
                        decision_j1 = None
                        penal_online_resuelto = False
                    else:
                        escena = "j1_PATEA"
                        pateador_actual = 1
                        decision_j2 = None
                        decision_j1 = None
                        penal_online_resuelto = False

                decision_j2 = None
                decision_j1 = None
                penal_online_resuelto = False
                confirmacion_online_j1 = False
                confirmacion_online_j2 = False
                confirmacion_j1 = False
                confirmacion_j2 = False
            

        
#GANADOR
    elif escena == "ganador":
        pantalla.blit(fondo_ganador, (0,0))

        if ganador == 1:
            pantalla.blit(banderas_paises[paises[indice_j1]], (500, 500))
            
        elif ganador == 2:
            pantalla.blit(banderas_paises[paises[indice_j2]], (500, 500))

#MENSAJE TANDA EXTRA

    elif escena == "mensaje_tanda_extra":
        pantalla.blit(fondo_mensaje, (0,0))

        if pygame.time.get_ticks() - tiempo_mensaje_tanda_extra > 3000:
            modo_tanda_extra = True
            ganador = None
            gol_extra_j1 = None
            gol_extra_j2 = None
            decision_j1 = None
            decision_j2 = None
            penal_online_resuelto = False
            confirmacion_online_j1 = False
            confirmacion_online_j2 = False

            if primer_turno == 1:
                pateador_actual = 1
                escena = "j1_PATEA"

            else:
                pateador_actual = 2
                if modo_local:
                    escena = "j2_PATEA"
                else:
                    escena = "j1_TAPA"

#------------------------------------------------------------------FIN------------------------------------------------------------
    if escena != "menu_principal" and escena != "conectando":
        color = (252, 70, 33)
        if boton_volver_selección.collidepoint(posicion_mouse):
            color = (255, 108, 82)

        pygame.draw.rect(pantalla, color, boton_volver_selección)
        texto = fuente_2.render("VOLVER", True, (255, 255, 255))
        pantalla.blit(texto, (52, 566))


    pygame.display.update()
pygame.quit()