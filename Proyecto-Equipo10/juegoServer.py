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
fuente_1 = pygame.font.Font("RecursosSI/PressStart2P.ttf", 15)
fuente_2 = pygame.font.Font("RecursosSI/PressStart2P.ttf", 18)
fuente_3 = pygame.font.Font("RecursosSI/PressStart2P.ttf", 25)
fuente_4 = pygame.font.Font("RecursosSI/PressStart2P.ttf", 28)
fuente_5 = pygame.font.Font("RecursosSI/PressStart2P.ttf", 40)


    #Fondos e Imágenes
    #Fondo Escenas

def cargar_fondo(ruta):
    imagen = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(imagen, (1080, 630))

fondo_menu = cargar_fondo("RecursosSI/Fondos/fondo_menu_servidor.jpg")
fondo_seleccion_local = cargar_fondo("RecursosSI/Fondos/fondo_seleccion_local.jpg")
fondo_seleccion_online = cargar_fondo("RecursosSI/Fondos/fondo_seleccion_online.jpg")
fondo_volver = cargar_fondo("RecursosSI/Fondos/fondo_volver.png")

fondo_buscando_cliente = cargar_fondo("RecursosSI/Fondos/fondo_buscando_cliente.jpg")

fondo_sorteo = cargar_fondo("RecursosSI/Fondos/fondo_sorteo.jpg")

fondo_vs = cargar_fondo("RecursosSI/Fondos/fondo_vs.jpg")

fondo_arco = cargar_fondo("RecursosSI/Fondos/fondo_arco.jpg")
fondo_penal = cargar_fondo("RecursosSI/Fondos/fondo_penal.jpg")
fondo_flechas = cargar_fondo("RecursosSI/Fondos/fondo_flechas.png")

fondo_gol = cargar_fondo("RecursosSI/Fondos/fondo_gol.jpg")
fondo_atajado = cargar_fondo("RecursosSI/Fondos/fondo_atajada.jpg")
fondo_atajado_feliz = cargar_fondo("RecursosSI/Fondos/fondo_atajada_feliz.jpg")
fondo_atajado_triste = cargar_fondo("RecursosSI/Fondos/fondo_atajada_triste.jpg")
fondo_notapado = cargar_fondo("RecursosSI/Fondos/fondo_no_tapado.jpg")

fondo_tanda_extra = cargar_fondo("RecursosSI/Fondos/fondo_tanda_extra.jpg")

fondo_ganador = cargar_fondo("RecursosSI/Fondos/fondo_ganador.jpg")

    #Mensajes
def cargar_mensaje(ruta, x, y):
    imagen = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(imagen, (x, y))

mensaje_sorteo = cargar_mensaje("RecursosSI/Mensajes/mensaje_patea_primero.png", 408, 114)
mensaje_buscando_cliente = cargar_mensaje("RecursosSI/Mensajes/mensaje_buscando_cliente.png", 792, 197)
mensaje_conectado_desde = cargar_mensaje("RecursosSI/Mensajes/mensaje_conectado_desde.png", 930, 283)

mensaje_default = cargar_mensaje("RecursosSI/Mensajes/mensaje_default_server.png", 868, 493)
mensaje_conexion_perdida = cargar_mensaje("RecursosSI/Mensajes/mensaje_conexión_perdida.png", 773, 471)

    #Banderas y Nombres

def cargar_bandera(ruta):
    imagen = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(imagen, (479, 276))

def cargar_bandera_vs(ruta):
    imagen = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(imagen, (343, 199))

def cargar_seleccion(ruta):
    imagen = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(imagen, (254, 265))

def cargar_bandera_izq(ruta):
    imagen = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(imagen, (399, 95))

def cargar_bandera_der(ruta):
    imagen = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(imagen, (402, 95))


seleccion_ecuador = cargar_seleccion("RecursosSI/Selecciones/Elecciones/jugadores_ecuador.png")
seleccion_argentina = cargar_seleccion("RecursosSI/Selecciones/Elecciones/jugadores_argentina.png")
seleccion_portugal = cargar_seleccion("RecursosSI/Selecciones/Elecciones/jugadores_portugal.png")
seleccion_españa = cargar_seleccion("RecursosSI/Selecciones/Elecciones/jugadores_españa.png")
seleccion_francia = cargar_seleccion("RecursosSI/Selecciones/Elecciones/jugadores_francia.png")
seleccion_brasil = cargar_seleccion("RecursosSI/Selecciones/Elecciones/jugadores_brasil.png")

band_ecuador_izq = cargar_bandera_izq("RecursosSI/Selecciones/Marcador/ecuador_izq.png")
band_ecuador_der = cargar_bandera_der("RecursosSI/Selecciones/Marcador/ecuador_der.png")
band_argentina_izq = cargar_bandera_izq("RecursosSI/Selecciones/Marcador/argentina_izq.png")
band_argentina_der = cargar_bandera_der("RecursosSI/Selecciones/Marcador/argentina_der.png")
band_portugal_izq = cargar_bandera_izq("RecursosSI/Selecciones/Marcador/portugal_izq.png")
band_portugal_der = cargar_bandera_der("RecursosSI/Selecciones/Marcador/portugal_der.png")
band_españa_izq = cargar_bandera_izq("RecursosSI/Selecciones/Marcador/españa_izq.png")
band_españa_der = cargar_bandera_der("RecursosSI/Selecciones/Marcador/españa_der.png")
band_francia_izq = cargar_bandera_izq("RecursosSI/Selecciones/Marcador/francia_izq.png")
band_francia_der = cargar_bandera_der("RecursosSI/Selecciones/Marcador/francia_der.png")
band_brasil_izq = cargar_bandera_izq("RecursosSI/Selecciones/Marcador/brasil_izq.png")
band_brasil_der = cargar_bandera_der("RecursosSI/Selecciones/Marcador/brasil_der.png")

band_ecuador = cargar_bandera("RecursosSI/Selecciones/Banderas/bandera_ecuador.png")
band_argentina = cargar_bandera("RecursosSI/Selecciones/Banderas/bandera_argentina.png")
band_portugal = cargar_bandera("RecursosSI/Selecciones/Banderas/bandera_portugal.png")
band_españa = cargar_bandera("RecursosSI/Selecciones/Banderas/bandera_españa.png")
band_francia = cargar_bandera("RecursosSI/Selecciones/Banderas/bandera_francia.png")
band_brasil = cargar_bandera("RecursosSI/Selecciones/Banderas/bandera_brasil.png")

band_ecuador_vs = cargar_bandera_vs("RecursosSI/Selecciones/Banderas/bandera_ecuador_vs.png")
band_argentina_vs = cargar_bandera_vs("RecursosSI/Selecciones/Banderas/bandera_argentina_vs.png")
band_portugal_vs = cargar_bandera_vs("RecursosSI/Selecciones/Banderas/bandera_portugal_vs.png")
band_españa_vs = cargar_bandera_vs("RecursosSI/Selecciones/Banderas/bandera_españa_vs.png")
band_francia_vs = cargar_bandera_vs("RecursosSI/Selecciones/Banderas/bandera_francia_vs.png")
band_brasil_vs = cargar_bandera_vs("RecursosSI/Selecciones/Banderas/bandera_brasil_vs.png")


        #Fotogramas Animación
def dibujar_fotograma(pantalla, imagen, tiempo_inicio, desde, hasta, x, y):
    tiempo_actual = pygame.time.get_ticks() - tiempo_inicio

    if desde <= tiempo_actual < hasta:
        pantalla.blit(imagen, (x, y))

def dibujar_secuencia(
    pantalla,
    fotogramas,
    tiempo_inicio,
    tiempos,
    posiciones
):
    for i in range(len(fotogramas)):
        desde, hasta = tiempos[i]
        x, y = posiciones[i]

        dibujar_fotograma(
            pantalla,
            fotogramas[i],
            tiempo_inicio,
            desde,
            hasta,
            x,
            y
        )

def cargar_fotograma(ruta, x, y):
    imagen = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(imagen, (x, y))
            

tamaños_jugador = [
    (88, 207),
    (88, 207),
    (77, 205),
    (74, 173),
    (121, 176),
    (115, 174),
    (124, 152),
    (124, 128),
    (134, 123),
    (136, 125),
    (128, 123),
    (105, 126),
    (92, 126),
    (91, 142),
    (84, 142),
    (114, 148)
]


tamaños_arquero_izq = [
    (63, 106),
    (61, 73),
    (76, 73),
    (86, 67),
    (85, 61),
    (121, 59),
    (140, 69),
    (123, 62),
    (113, 45),
    (102, 62),
    (53, 29),
    (71, 50)
]


tamaños_arquero_der = [
    (63, 106),
    (61, 73),
    (76, 73),
    (86, 67),
    (85, 61),
    (121, 59),
    (140, 69),
    (123, 62),
    (113, 45),
    (102, 62),
    (53, 29),
    (71, 50)
]


tamaños_arquero_med = [
    (63, 106),
    (61, 73),
    (76, 73),
    (78, 82),
    (124, 90),
    (116, 85),
    (111, 80),
    (107, 56),
    (98, 45)
]

tiempos_jugador = [
    (0, 100),
    (100, 200),
    (200, 300),
    (300, 400),
    (400, 500),
    (500, 600),
    (600, 700),
    (700, 800),
    (800, 900),
    (900, 1000),
    (1000, 1100),
    (1100, 1200),
    (1200, 1300),
    (1300, 1400),
    (1400, 1500),
    (1500, 1600)
]


posiciones_jugador = [
    (642, 352),
    (634, 343),
    (616, 340),
    (595, 326),
    (565, 316),
    (556, 307),
    (547, 307),
    (555, 314),
    (555, 312),
    (552, 314),
    (537, 315),
    (543, 312),
    (552, 311),
    (540, 296),
    (543, 297),
    (543, 297)
]

tiempos_arquero_izq_der = [
    (0, 300),
    (300, 600),
    (600, 900),
    (900, 970),
    (970, 1041),
    (1041, 1111),
    (1111, 1182),
    (1182, 1252),
    (1252, 1323),
    (1323, 1393),
    (1393, 1463),
    (1463, 99999999)
]


posiciones_arquero_izq = [
    (505, 180),
    (505, 214),
    (493, 215),
    (478, 218),
    (466, 224),
    (418, 227),
    (386, 214),
    (366, 203),
    (364, 227),
    (355, 223),
    (353, 256),
    (329, 246)
]


posiciones_arquero_der = [
    (503, 180),
    (505, 214),
    (502, 215),
    (507, 218),
    (520, 224),
    (532, 227),
    (545, 214),
    (582, 203),
    (594, 227),
    (614, 223),
    (665, 256),
    (671, 246)
]


tiempos_arquero_med = [
    (0, 300),
    (300, 600),
    (600, 900),
    (900, 1005),
    (1005, 1110),
    (1110, 1214),
    (1214, 1319),
    (1319, 1424),
    (1424, 99999999)
]


posiciones_arquero_med = [
    (505, 180),
    (505, 214),
    (493, 215),
    (500, 208),
    (475, 199),
    (472, 205),
    (470, 210),
    (467, 230),
    (477, 244)
]

def cargar_secuencia(carpeta, tamaños):
    fotogramas = []

    for numero, tamaño in enumerate(tamaños, start=1):
        ruta = f"{carpeta}/{numero}.png"

        imagen = cargar_fotograma(
            ruta,
            tamaño[0],
            tamaño[1]
        )

        fotogramas.append(imagen)

    return fotogramas


def cargar_skin_equipo(pais):
    carpeta = f"RecursosSI/Animaciones/Países/{pais}"

    return {
        "jugador": cargar_secuencia(
            f"{carpeta}/Jugadores",
            tamaños_jugador
        ),

        "feliz": cargar_fotograma(
            f"{carpeta}/Jugadores/17_feliz.png",
            114,
            148
        ),

        "triste": cargar_fotograma(
            f"{carpeta}/Jugadores/17_triste.png",
            114,
            148
        ),

        "arquero": {
            1: cargar_secuencia(
                f"{carpeta}/Arquero/Izquierda",
                tamaños_arquero_izq
            ),

            2: cargar_secuencia(
                f"{carpeta}/Arquero/Medio",
                tamaños_arquero_med
            ),

            3: cargar_secuencia(
                f"{carpeta}/Arquero/Derecha",
                tamaños_arquero_der
            )
        }
    }

skins = {
    "Ecuador": cargar_skin_equipo("Ecuador"),
    "Argentina": cargar_skin_equipo("Argentina"),
    "Portugal": cargar_skin_equipo("Portugal"),
    "España": cargar_skin_equipo("España"),
    "Francia": cargar_skin_equipo("Francia"),
    "Brasil": cargar_skin_equipo("Brasil")
}

moneda1 = cargar_fotograma("RecursosSI/Animaciones/Moneda/moneda1.png", 122, 80)
moneda2 = cargar_fotograma("RecursosSI/Animaciones/Moneda/moneda2.png", 119, 92)
moneda3 = cargar_fotograma("RecursosSI/Animaciones/Moneda/moneda3.png", 108, 101)
moneda4 = cargar_fotograma("RecursosSI/Animaciones/Moneda/moneda4.png", 116, 124)
moneda5 = cargar_fotograma("RecursosSI/Animaciones/Moneda/moneda5.png", 128, 129)
moneda6 = cargar_fotograma("RecursosSI/Animaciones/Moneda/moneda6.png", 117, 121)
moneda7 = cargar_fotograma("RecursosSI/Animaciones/Moneda/moneda7.png", 114, 88)
moneda8 = cargar_fotograma("RecursosSI/Animaciones/Moneda/moneda8.png", 121, 67)
moneda9 = cargar_fotograma("RecursosSI/Animaciones/Moneda/moneda9.png", 121, 48)
moneda10 = cargar_fotograma("RecursosSI/Animaciones/Moneda/moneda10.png", 121, 66)
moneda11 = cargar_fotograma("RecursosSI/Animaciones/Moneda/moneda11.png", 115, 87)
moneda12 = cargar_fotograma("RecursosSI/Animaciones/Moneda/moneda12.png", 123, 114)
moneda13 = cargar_fotograma("RecursosSI/Animaciones/Moneda/moneda13.png", 133, 127)
moneda14 = cargar_fotograma("RecursosSI/Animaciones/Moneda/moneda14.png", 122, 93)
moneda15 = cargar_fotograma("RecursosSI/Animaciones/Moneda/moneda15.png", 113, 46)

            

            #Balón
def cargar_balon(ruta):
    imagen = pygame.image.load(ruta).convert_alpha()
    return pygame.transform.scale(imagen, (30, 30))

balon1 = cargar_balon("RecursosSI/Animaciones/Balón/1.png")
balon2 = cargar_balon("RecursosSI/Animaciones/Balón/2.png")
balon3 = cargar_balon("RecursosSI/Animaciones/Balón/3.png")
balon4 = cargar_balon("RecursosSI/Animaciones/Balón/4.png")
balon5 = cargar_balon("RecursosSI/Animaciones/Balón/5.png")
balon6 = cargar_balon("RecursosSI/Animaciones/Balón/6.png")
balon7 = cargar_balon("RecursosSI/Animaciones/Balón/7.png")
balon8 = cargar_balon("RecursosSI/Animaciones/Balón/8.png")

        #Bolitas de Resultado
bolita_verde = pygame.image.load("RecursosSI/Botones/bolita_verde.png").convert_alpha()
pygame.transform.scale(bolita_verde, (52, 50))

bolita_roja = pygame.image.load("RecursosSI/Botones/bolita_roja.png").convert_alpha()
pygame.transform.scale(bolita_roja, (52, 50))



    #Escena Inicial
escena = "menu_principal"
modo_local = False

    #Conexión
conectado = False
buscando_conexión = False
dirección = None
conexión = None

tiempo_conexion_perdida = 0

        #Confirmación en Conexión
confirmado_continuar = False
rival_confirma_continuar = False
contador_confirmado = 0

mensaje_volver = False

j1_vuelve = False
j2_vuelve = False

    #Diccionarios Equipos

paises = ["Ecuador", "Argentina", "Portugal", "España", "Francia", "Brasil"]
banderas_paises = {"Ecuador" : band_ecuador,
                   "Argentina" : band_argentina,
                   "Portugal" : band_portugal,
                   "España" : band_españa,
                   "Francia" : band_francia,
                   "Brasil" : band_brasil}

banderas_paises_marcador_izq = {"Ecuador" : band_ecuador_izq,
                   "Argentina" : band_argentina_izq,
                   "Portugal" : band_portugal_izq,
                   "España" : band_españa_izq,
                   "Francia" : band_francia_izq,
                   "Brasil" : band_brasil_izq}

banderas_paises_marcador_der = {"Ecuador" : band_ecuador_der,
                   "Argentina" : band_argentina_der,
                   "Portugal" : band_portugal_der,
                   "España" : band_españa_der,
                   "Francia" : band_francia_der,
                   "Brasil" : band_brasil_der}

banderas_paises_vs = {"Ecuador" : band_ecuador_vs,
                   "Argentina" : band_argentina_vs,
                   "Portugal" : band_portugal_vs,
                   "España" : band_españa_vs,
                   "Francia" : band_francia_vs,
                   "Brasil" : band_brasil_vs}

equipos_bandera = {"Ecuador" : seleccion_ecuador,
                   "Argentina" : seleccion_argentina,
                   "Portugal" : seleccion_portugal,
                   "España" : seleccion_españa,
                   "Francia" : seleccion_francia,
                   "Brasil" : seleccion_brasil}

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
    x_izq = 60
    x_der = 969
    y = 143
    espacio = 65

    if primer_turno == 1:
        lista_izq = resultado_penales_j1
        lista_der = resultado_penales_j2
    else:
        lista_izq = resultado_penales_j2
        lista_der = resultado_penales_j1

    for i in range(5):
        if i < len(lista_izq):
            if lista_izq[i]:
                pantalla.blit(
                    bolita_verde,
                    (x_izq + i * espacio, y)
                )
            else:
                pantalla.blit(
                    bolita_roja,
                    (x_izq + i * espacio, y)
                )

        if i < len(lista_der):
            if lista_der[i]:
                pantalla.blit(
                    bolita_verde,
                    (x_der - i * espacio, y)
                )
            else:
                pantalla.blit(
                    bolita_roja,
                    (x_der - i * espacio, y)
                )

    #Botones
        #Carga de botones
def cargar_boton_img(ruta_normal, ruta_hover, x, y):
    imagen_normal = pygame.image.load(ruta_normal).convert_alpha()
    imagen_hover = pygame.image.load(ruta_hover).convert_alpha()
    rect = imagen_normal.get_rect(topleft=(x, y))

    return {
        "normal": imagen_normal,
        "hover": imagen_hover,
        "rect": rect
    }

boton_local_menu = cargar_boton_img("RecursosSI/Botones/boton_local.png","RecursosSI/Botones/boton_local_hover.png", 146, 412)
boton_online_menu = cargar_boton_img("RecursosSI/Botones/boton_online.png","RecursosSI/Botones/boton_online_hover.png", 626, 412)

boton_volver_menu = cargar_boton_img("RecursosSI/Botones/boton_confirmar_volver.png","RecursosSI/Botones/boton_confirmar_volver_hover.png", 625, 471)
boton_cancelar_volver = cargar_boton_img("RecursosSI/Botones/boton_cancelar_volver.png","RecursosSI/Botones/boton_cancelar_volver_hover.png", 259, 471)

boton_volver_selección = cargar_boton_img("RecursosSI/Botones/boton_volver_seleccion.png","RecursosSI/Botones/boton_volver_seleccion_hover.png", 29, 559)
boton_continuar_selección = cargar_boton_img("RecursosSI/Botones/boton_continuar_general.png","RecursosSI/Botones/boton_continuar_general_hover.png", 840, 559)

boton_volver_conexion = cargar_boton_img("RecursosSI/Botones/boton_volver_online.png","RecursosSI/Botones/boton_volver_online_hover.png", 54, 457)
boton_continuar_conexión = cargar_boton_img("RecursosSI/Botones/boton_continuar_online.png","RecursosSI/Botones/boton_continuar_online_hover.png", 718, 457)
boton_continuar_conexión_si = cargar_boton_img("RecursosSI/Botones/boton_continuar_online_si.png","RecursosSI/Botones/boton_continuar_online_si_hover.png", 718, 457)

boton_confirmar_seleccion1 = cargar_boton_img("RecursosSI/Botones/boton_confirmar_seleccion.png","RecursosSI/Botones/boton_confirmar_seleccion_hover.png", 153, 207)
boton_confirmar_seleccion2 = cargar_boton_img("RecursosSI/Botones/boton_confirmar_seleccion.png","RecursosSI/Botones/boton_confirmar_seleccion_hover.png", 679, 207)

boton_confirmado_seleccion1 = cargar_boton_img("RecursosSI/Botones/boton_confirmado_seleccion.png","RecursosSI/Botones/boton_confirmado_seleccion_hover.png", 138, 207)
boton_confirmado_seleccion2 = cargar_boton_img("RecursosSI/Botones/boton_confirmado_seleccion.png","RecursosSI/Botones/boton_confirmado_seleccion_hover.png", 663, 207)

boton_continuar_sorteo = cargar_boton_img("RecursosSI/Botones/boton_continuar_general.png","RecursosSI/Botones/boton_continuar_general_hover.png", 840, 559)


boton_izq_arco = cargar_boton_img("RecursosSI/Botones/boton_decision.png","RecursosSI/Botones/boton_decision_hover.png", 198, 159)
boton_med_arco = cargar_boton_img("RecursosSI/Botones/boton_decision.png","RecursosSI/Botones/boton_decision_hover.png", 433, 159)
boton_der_arco = cargar_boton_img("RecursosSI/Botones/boton_decision.png","RecursosSI/Botones/boton_decision_hover.png", 667, 159)

def dibujar_boton_img(pantalla, boton, posicion_mouse):
    if boton["rect"].collidepoint(posicion_mouse):
        pantalla.blit(boton["hover"], boton["rect"])
    else:
        pantalla.blit(boton["normal"], boton["rect"])

def cerrar_conexion_online():
    global conectado, buscando_conexión, conexión
    global confirmado_continuar, rival_confirma_continuar, contador_confirmado

    conectado = False
    buscando_conexión = False
    confirmado_continuar = False
    rival_confirma_continuar = False
    contador_confirmado = 0

    try:
        if conexión:
            conexión.close()
    except:
        pass

    conexión = None

def cerrar_socket_actual_server():
    global conectado, conexión
    global confirmado_continuar, rival_confirma_continuar, contador_confirmado

    conectado = False
    confirmado_continuar = False
    rival_confirma_continuar = False
    contador_confirmado = 0

    try:
        if conexión:
            conexión.close()
    except:
        pass

    conexión = None

#---------------------------------------------------------CONEXIÓN SOCKETS TCP-------------------------------------------------------
def esperando_cliente():
    global conectado, conexión, dirección, buscando_conexión, rival_confirma_continuar, indice_j2
    global confirmacion_j1, confirmacion_j2, pais_j1, pais_j2, escena, tiempo_animacion_moneda, tiempo_vs
    global confirmacion_online_j2, confirmacion_online_j1, decision_j1, decision_j2, tiempo_animacion_penal, j2_vuelve
    global j1_vuelve, tiempo_conexion_perdida

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

            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, OSError):
                cerrar_socket_actual_server()
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

                            #Manejo Desconexiones
                        elif mensaje == "J2_CONFIRMA_DESCONEXION_PROPOSITO":
                            cerrar_conexion_online()
                            escena = "ganaste_default"

                                #Rival quiere volver
                        elif mensaje == "J2_VOLVER_MENU":
                            j2_vuelve = True

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
                if escena == "conectando":
                    cerrar_socket_actual_server()
                else:
                    cerrar_conexion_online()
                    escena = "conexion_perdida"
                    tiempo_conexion_perdida = pygame.time.get_ticks()


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

        mensaje_volver = False
        j1_vuelve = False
        j2_vuelve = False
        tiempo_conexion_perdida = 0

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
                if boton_volver_selección["rect"].collidepoint(evento.pos):

                    if escena == "ganador":
                        escena = "menu_principal"

                    elif escena == "ganaste_default":
                        escena = "menu_principal"

                    elif modo_local and escena == "seleccion_equipos":
                        escena = "menu_principal"

                    else:
                        mensaje_volver = True

                if mensaje_volver:
                    if boton_volver_menu["rect"].collidepoint(evento.pos):
                        if not modo_local and conectado:
                            conexión.sendall(b"J1_CONFIRMA_DESCONEXION_PROPOSITO|")
                            cerrar_conexion_online()

                        escena = "menu_principal"

                    elif boton_cancelar_volver["rect"].collidepoint(evento.pos):
                        mensaje_volver = False
                    

            #MENU
            if escena == "menu_principal":
                if boton_local_menu["rect"].collidepoint(evento.pos) and not mensaje_volver:
                    escena = "seleccion_equipos"
                    modo_local = True

                elif boton_online_menu["rect"].collidepoint(evento.pos) and not mensaje_volver:
                    cerrar_conexion_online()
                    escena = "conectando"

                    if not conectado and not buscando_conexión:
                        buscando_conexión = True
                        hilo_red = threading.Thread(target=esperando_cliente, daemon=True)
                        hilo_red.start()
            
            #SELECCIÓN EQUIPOS
            elif escena == "seleccion_equipos":
                if modo_local:
                    if boton_confirmar_seleccion1["rect"].collidepoint(evento.pos):
                        if not confirmacion_j1:
                            pais_j1 = paises[indice_j1]
                            confirmacion_j1 = True
                        else:
                            pais_j1 = None
                            confirmacion_j1 = False
                    elif boton_confirmar_seleccion2["rect"].collidepoint(evento.pos):
                        if not confirmacion_j2:
                            pais_j2 = paises[indice_j2]
                            confirmacion_j2 = True
                        else:
                            pais_j2 = None
                            confirmacion_j2 = False

                    if selecciones_confirmadas:
                        if boton_continuar_selección["rect"].collidepoint(evento.pos):
                            escena = "sorteo"
                            tiempo_animacion_moneda = pygame.time.get_ticks()

                else:
                    if boton_confirmar_seleccion1["rect"].collidepoint(evento.pos):
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
                        if boton_continuar_selección["rect"].collidepoint(evento.pos):
                            escena = "sorteo"
                            if conectado:
                                conexión.sendall(b"IR_A_SORTEO|")
                                tiempo_animacion_moneda = pygame.time.get_ticks()
                                
            #SORTEO
            elif escena == "sorteo":
                if sorteo_hecho and boton_continuar_sorteo["rect"].collidepoint(evento.pos):
                    escena = "versus"
                    tiempo_vs = pygame.time.get_ticks()
                        
                    if not modo_local and conectado:
                        conexión.sendall(b"INICIAR_PARTIDO|")

            #J1 PATEA
            elif escena == "j1_PATEA":
                
                if decision_j1 is None:
                    if boton_izq_arco["rect"].collidepoint(evento.pos) and not mensaje_volver: decision_j1 = 1
                    elif boton_med_arco["rect"].collidepoint(evento.pos) and not mensaje_volver: decision_j1 = 2
                    elif boton_der_arco["rect"].collidepoint(evento.pos) and not mensaje_volver: decision_j1 = 3

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
                    if boton_izq_arco["rect"].collidepoint(evento.pos) and not mensaje_volver: decision_j2 = 1
                    elif boton_med_arco["rect"].collidepoint(evento.pos) and not mensaje_volver: decision_j2 = 2
                    elif boton_der_arco["rect"].collidepoint(evento.pos) and not mensaje_volver: decision_j2 = 3

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
                    if boton_izq_arco["rect"].collidepoint(evento.pos) and not mensaje_volver:decision_j2 = 1
                    elif boton_med_arco["rect"].collidepoint(evento.pos) and not mensaje_volver: decision_j2 = 2
                    elif boton_der_arco["rect"].collidepoint(evento.pos) and not mensaje_volver:decision_j2 = 3

                if modo_local and decision_j2 is not None:
                    escena = "j1_TAPA"
                    tiempo_animacion_penal = pygame.time.get_ticks()

            #J1 TAPA
            elif escena == "j1_TAPA":
                
                
                if decision_j1 is None:
                    if boton_izq_arco["rect"].collidepoint(evento.pos) and not mensaje_volver: decision_j1 = 1
                    elif boton_med_arco["rect"].collidepoint(evento.pos) and not mensaje_volver: decision_j1 = 2
                    elif boton_der_arco["rect"].collidepoint(evento.pos) and not mensaje_volver: decision_j1 = 3

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
                if boton_volver_conexion["rect"].collidepoint(evento.pos):
                    escena = "menu_principal"
                    buscando_conexión = False
                    

                    if conectado and conexión:
                        conexión.close()
                    conectado = False
            
                elif boton_continuar_conexión["rect"].collidepoint(evento.pos):
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
        pantalla.blit(fondo_menu, (0,0))

        dibujar_boton_img(pantalla, boton_local_menu, posicion_mouse)
        dibujar_boton_img(pantalla, boton_online_menu, posicion_mouse)


#BUSCANDO CONEXIÓN
    elif escena == "conectando":
        pantalla.blit(fondo_buscando_cliente, (0,0))

        dibujar_boton_img(pantalla, boton_volver_conexion, posicion_mouse)

        if not conectado:
            pantalla.blit(mensaje_buscando_cliente, (144, 192))
        else:
            pantalla.blit(mensaje_conectado_desde, (70, 150))
            texto = fuente_5.render(f"{dirección[0]}", True, (255, 255, 255))
            pantalla.blit(texto, (183, 365))

            if confirmado_continuar:
                dibujar_boton_img(pantalla, boton_continuar_conexión_si, posicion_mouse)
            else:
                dibujar_boton_img(pantalla, boton_continuar_conexión, posicion_mouse)

            texto = fuente_2.render((f"{contador_confirmado}/2"), True, (255, 255, 255))
            pantalla.blit(texto, (845, 547))



#SELECCIÓN DE EQUIPOS
    elif escena == "seleccion_equipos":
        
        if modo_local:
            pantalla.blit(fondo_seleccion_local, (0,0))
        else:
            pantalla.blit(fondo_seleccion_online, (0,0))

        pantalla.blit(equipos_bandera[paises[indice_j1]], (146, 276))
        pantalla.blit(equipos_bandera[paises[indice_j2]], (681, 275))
        

        if not confirmacion_j1:
            dibujar_boton_img(pantalla, boton_confirmar_seleccion1, posicion_mouse)
        else:
            dibujar_boton_img(pantalla, boton_confirmado_seleccion1, posicion_mouse)

        if not confirmacion_j2:
            dibujar_boton_img(pantalla, boton_confirmar_seleccion2, posicion_mouse)
        else:
            dibujar_boton_img(pantalla, boton_confirmado_seleccion2, posicion_mouse)

        if selecciones_confirmadas:

            dibujar_boton_img(pantalla, boton_continuar_selección, posicion_mouse)

        if error_paises_iguales:
            
            texto = fuente_2.render("NO PUEDEN ESCOGER EL MISMO PAIS", True, (255, 0, 0))
            pantalla.blit(texto, (250, 570))


#SORTEO
    elif escena == "sorteo":
        pantalla.blit(fondo_sorteo, (0,0))

        dibujar_fotograma(pantalla, moneda1, tiempo_animacion_moneda, 0, 80, 266, 296)
        dibujar_fotograma(pantalla, moneda2, tiempo_animacion_moneda, 80, 160, 304, 238)
        dibujar_fotograma(pantalla, moneda3, tiempo_animacion_moneda, 160, 240, 347, 183)
        dibujar_fotograma(pantalla, moneda4, tiempo_animacion_moneda, 240, 320, 392, 142)
        dibujar_fotograma(pantalla, moneda5, tiempo_animacion_moneda, 320, 400, 469, 128)
        dibujar_fotograma(pantalla, moneda6, tiempo_animacion_moneda, 400, 450, 526, 168)
        dibujar_fotograma(pantalla, moneda7, tiempo_animacion_moneda, 480, 500, 548, 227)
        dibujar_fotograma(pantalla, moneda8, tiempo_animacion_moneda, 500, 550, 560, 281)
        dibujar_fotograma(pantalla, moneda9, tiempo_animacion_moneda, 550, 600, 563, 329)
        dibujar_fotograma(pantalla, moneda10, tiempo_animacion_moneda, 600, 650, 560, 353)
        dibujar_fotograma(pantalla, moneda11, tiempo_animacion_moneda, 650, 700, 564, 392)
        dibujar_fotograma(pantalla, moneda12, tiempo_animacion_moneda, 700, 750, 559, 441)
        dibujar_fotograma(pantalla, moneda13, tiempo_animacion_moneda, 750, 800, 555, 492)
        dibujar_fotograma(pantalla, moneda14, tiempo_animacion_moneda, 800, 850, 559, 537)
        dibujar_fotograma(pantalla, moneda15, tiempo_animacion_moneda, 850, 999999999, 556, 584)


        if pygame.time.get_ticks() - tiempo_animacion_moneda > 1000:
            if not sorteo_hecho:
                primer_turno = random.choice((1, 2))
                sorteo_hecho = True

                if not modo_local and conectado:
                    conexión.sendall(f"RESULTADO_SORTEO:{primer_turno}|".encode("utf-8"))
            
            if primer_turno == 1:
                bandera = banderas_paises[paises[indice_j1]]
            else:
                bandera = banderas_paises[paises[indice_j2]]

            pantalla.blit(bandera, (519, 137))
            pantalla.blit(mensaje_sorteo, (571,427))
            dibujar_boton_img(pantalla, boton_continuar_sorteo, posicion_mouse)


#ESCENA VS

    elif escena == "versus":
        pantalla.blit(fondo_vs, (0,0))

        if primer_turno == 1:
            pantalla.blit(banderas_paises_vs[paises[indice_j1]], (131, 66))
            pantalla.blit(banderas_paises_vs[paises[indice_j2]], (131, 344))
        else:
            pantalla.blit(banderas_paises_vs[paises[indice_j2]], (131, 66))
            pantalla.blit(banderas_paises_vs[paises[indice_j1]], (131, 344))

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

        texto = fuente_4.render(f"{pais_j1} PATEA", True, (255,255,255))
        pantalla.blit(texto, (350, 50))

        if modo_local:
            texto = fuente_3.render(f"{pais_j2} CIERRA LOS OJOS!", True, (255,255,255))
            pantalla.blit(texto, (200, 500))
        else:
            if decision_j1 is not None and not confirmacion_online_j2:
                texto = fuente_3.render(f"ESPERANDO LA DECISIÓN DE {pais_j2}", True, (255,255,255))
                pantalla.blit(texto, (120, 500))


        if not decision_j1:
            dibujar_boton_img(pantalla, boton_izq_arco, posicion_mouse)
            dibujar_boton_img(pantalla, boton_med_arco, posicion_mouse)
            dibujar_boton_img(pantalla, boton_der_arco, posicion_mouse)

            pantalla.blit(fondo_flechas, (0, 0))

#J2_PATEA
    elif escena == "j2_PATEA":
        pantalla.blit(fondo_arco, (0, 0))

        texto = fuente_4.render(f"{pais_j2} PATEA", True, (255,255,255))
        pantalla.blit(texto, (350, 50))

        if modo_local:
            texto = fuente_4.render(f"{pais_j1} CIERRA LOS OJOS!", True, (255,255,255))
            pantalla.blit(texto, (200, 500))

        if not decision_j2:

            dibujar_boton_img(pantalla, boton_izq_arco, posicion_mouse)
            dibujar_boton_img(pantalla, boton_med_arco, posicion_mouse)
            dibujar_boton_img(pantalla, boton_der_arco, posicion_mouse)

            pantalla.blit(fondo_flechas, (0, 0))

#J1_TAPA
    elif escena == "j1_TAPA":
        pantalla.blit(fondo_arco, (0, 0))

        texto = fuente_4.render(f"{pais_j1} TAPA", True, (255,255,255))
        pantalla.blit(texto, (350, 50))

        if modo_local:
            texto = fuente_4.render(f"{pais_j2} CIERRA LOS OJOS!", True, (255,255,255))
            pantalla.blit(texto, (200, 500))
        else:
            if decision_j1 is not None and not confirmacion_online_j2:
                texto = fuente_3.render(f"ESPERANDO LA DECISIÓN DE {pais_j2}", True, (255,255,255))
                pantalla.blit(texto, (120, 500))

        if not decision_j1:
            dibujar_boton_img(pantalla, boton_izq_arco, posicion_mouse)
            dibujar_boton_img(pantalla, boton_med_arco, posicion_mouse)
            dibujar_boton_img(pantalla, boton_der_arco, posicion_mouse)

            pantalla.blit(fondo_flechas, (0, 0))

#J2_TAPA
    elif escena == "j2_TAPA":
        pantalla.blit(fondo_arco, (0, 0))

        texto = fuente_4.render(f"{pais_j2} TAPA", True, (255,255,255))
        pantalla.blit(texto, (350, 50))

        if modo_local:
            texto = fuente_4.render(f"{pais_j1} CIERRA LOS OJOS!", True, (255,255,255))
            pantalla.blit(texto, (200, 500))

        if not decision_j2:
            dibujar_boton_img(pantalla, boton_izq_arco, posicion_mouse)
            dibujar_boton_img(pantalla, boton_med_arco, posicion_mouse)
            dibujar_boton_img(pantalla, boton_der_arco, posicion_mouse)

            pantalla.blit(fondo_flechas, (0, 0))


#ANIMACIÓN PENAL
    elif escena == "animacion_penal":
        pantalla.blit(fondo_penal, (0, 0))

        if pateador_actual == 1:
            pais_pateador = pais_j1
            pais_arquero = pais_j2

            decision_pateador = decision_j1
            decision_arquero = decision_j2

        else:
            pais_pateador = pais_j2
            pais_arquero = pais_j1

            decision_pateador = decision_j2
            decision_arquero = decision_j1

        skin_pateador = skins[pais_pateador]
        skin_arquero = skins[pais_arquero]

        fotogramas_jugador = skin_pateador["jugador"]
        fotogramas_arquero = skin_arquero["arquero"][decision_arquero]

        dibujar_secuencia(
            pantalla,
            fotogramas_jugador,
            tiempo_animacion_penal,
            tiempos_jugador,
            posiciones_jugador
        )

        if decision_arquero == 1:
            dibujar_secuencia(
                pantalla,
                fotogramas_arquero,
                tiempo_animacion_penal,
                tiempos_arquero_izq_der,
                posiciones_arquero_izq
            )

        elif decision_arquero == 2:
            dibujar_secuencia(
                pantalla,
                fotogramas_arquero,
                tiempo_animacion_penal,
                tiempos_arquero_med,
                posiciones_arquero_med
            )

        elif decision_arquero == 3:
            dibujar_secuencia(
                pantalla,
                fotogramas_arquero,
                tiempo_animacion_penal,
                tiempos_arquero_izq_der,
                posiciones_arquero_der
            )

        dibujar_fotograma(
            pantalla,
            balon1,
            tiempo_animacion_penal,
            0,
            1100,
            525,
            406
        )

        if decision_pateador == 1:
            dibujar_fotograma(pantalla, balon2, tiempo_animacion_penal, 1100, 1114, 505, 371)
            dibujar_fotograma(pantalla, balon3, tiempo_animacion_penal, 1114, 1128, 501, 336)
            dibujar_fotograma(pantalla, balon4, tiempo_animacion_penal, 1128, 1142, 466, 307)
            dibujar_fotograma(pantalla, balon5, tiempo_animacion_penal, 1142, 1156, 444, 279)
            dibujar_fotograma(pantalla, balon6, tiempo_animacion_penal, 1156, 1169, 420, 262)
            dibujar_fotograma(pantalla, balon7, tiempo_animacion_penal, 1169, 1182, 395, 222)
            dibujar_fotograma(pantalla, balon8, tiempo_animacion_penal, 1182, 1252, 369, 200)

            if decision_pateador == decision_arquero:
                dibujar_fotograma(pantalla, balon1, tiempo_animacion_penal, 1252, 1320, 343, 210)
                dibujar_fotograma(pantalla, balon2, tiempo_animacion_penal, 1320, 1388, 324, 225)
                dibujar_fotograma(pantalla, balon3, tiempo_animacion_penal, 1388, 1456, 304, 246)
                dibujar_fotograma(pantalla, balon4, tiempo_animacion_penal, 1456, 99999999, 286, 267)

            else:
                dibujar_fotograma(pantalla, balon1, tiempo_animacion_penal, 1252, 1320, 353, 164)
                dibujar_fotograma(pantalla, balon2, tiempo_animacion_penal, 1320, 1388, 357, 156)
                dibujar_fotograma(pantalla, balon3, tiempo_animacion_penal, 1388, 1456, 372, 161)
                dibujar_fotograma(pantalla, balon4, tiempo_animacion_penal, 1456, 99999999, 384, 168)

        elif decision_pateador == 2:
            dibujar_fotograma(pantalla, balon2, tiempo_animacion_penal, 1100, 1114, 517, 384)
            dibujar_fotograma(pantalla, balon3, tiempo_animacion_penal, 1114, 1128, 515, 356)
            dibujar_fotograma(pantalla, balon4, tiempo_animacion_penal, 1128, 1142, 513, 329)
            dibujar_fotograma(pantalla, balon5, tiempo_animacion_penal, 1142, 1156, 510, 300)
            dibujar_fotograma(pantalla, balon6, tiempo_animacion_penal, 1156, 1169, 510, 270)
            dibujar_fotograma(pantalla, balon7, tiempo_animacion_penal, 1169, 1182, 513, 245)
            dibujar_fotograma(pantalla, balon8, tiempo_animacion_penal, 1182, 1252, 517, 221)

            if decision_pateador == decision_arquero:
                dibujar_fotograma(pantalla, balon1, tiempo_animacion_penal, 1252, 1320, 555, 235)
                dibujar_fotograma(pantalla, balon2, tiempo_animacion_penal, 1320, 1388, 553, 239)
                dibujar_fotograma(pantalla, balon3, tiempo_animacion_penal, 1388, 99999999, 564, 265)

            else:
                dibujar_fotograma(pantalla, balon1, tiempo_animacion_penal, 1252, 1320, 525, 196)
                dibujar_fotograma(pantalla, balon2, tiempo_animacion_penal, 1320, 1388, 537, 179)
                dibujar_fotograma(pantalla, balon3, tiempo_animacion_penal, 1388, 99999999, 554, 163)

        elif decision_pateador == 3:
            dibujar_fotograma(pantalla, balon2, tiempo_animacion_penal, 1100, 1114, 537, 371)
            dibujar_fotograma(pantalla, balon3, tiempo_animacion_penal, 1114, 1128, 556, 336)
            dibujar_fotograma(pantalla, balon4, tiempo_animacion_penal, 1128, 1142, 576, 307)
            dibujar_fotograma(pantalla, balon5, tiempo_animacion_penal, 1142, 1156, 598, 279)
            dibujar_fotograma(pantalla, balon6, tiempo_animacion_penal, 1156, 1169, 637, 262)
            dibujar_fotograma(pantalla, balon7, tiempo_animacion_penal, 1169, 1182, 647, 222)
            dibujar_fotograma(pantalla, balon8, tiempo_animacion_penal, 1182, 1252, 674, 200)

            if decision_pateador == decision_arquero:
                dibujar_fotograma(pantalla, balon1, tiempo_animacion_penal, 1252, 1320, 705, 189)
                dibujar_fotograma(pantalla, balon2, tiempo_animacion_penal, 1320, 1388, 731, 209)
                dibujar_fotograma(pantalla, balon3, tiempo_animacion_penal, 1388, 1456, 750, 238)
                dibujar_fotograma(pantalla, balon4, tiempo_animacion_penal, 1456, 99999999, 763, 267)

            else:
                dibujar_fotograma(pantalla, balon1, tiempo_animacion_penal, 1252, 1320, 689, 164)
                dibujar_fotograma(pantalla, balon2, tiempo_animacion_penal, 1320, 1388, 685, 156)
                dibujar_fotograma(pantalla, balon3, tiempo_animacion_penal, 1388, 1456, 670, 161)
                dibujar_fotograma(pantalla, balon4, tiempo_animacion_penal, 1456, 99999999, 658, 168)


        tiempo_transcurrido = pygame.time.get_ticks() - tiempo_animacion_penal

        if 1600 < tiempo_transcurrido < 2900:
            if decision_pateador != decision_arquero:
                pantalla.blit(
                    skin_pateador["feliz"],
                    (543, 291)
                )
            else:
                pantalla.blit(
                    skin_pateador["triste"],
                    (543, 291)
                )

        if tiempo_transcurrido > 2900:
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
                    pantalla.blit(fondo_atajado_triste, (0,0))
            else:
                if decision_j1 != decision_j2:
                    pantalla.blit(fondo_notapado, (0,0))
                else:
                    pantalla.blit(fondo_atajado_feliz, (0,0))
     
        if primer_turno == 1:
            pantalla.blit(banderas_paises_marcador_izq[paises[indice_j1]], (52, 40))
            texto= fuente_5.render(f"{contador_j1}", True, (255, 255, 255))
            pantalla.blit(texto, (474, 63))

            pantalla.blit(banderas_paises_marcador_der[paises[indice_j2]], (629, 40))
            texto= fuente_5.render(f"{contador_j2}", True, (255, 255, 255))
            pantalla.blit(texto, (564, 63))
        else:
            pantalla.blit(banderas_paises_marcador_izq[paises[indice_j2]], (52, 40))
            texto= fuente_5.render(f"{contador_j2}", True, (255, 255, 255))
            pantalla.blit(texto, (474, 63))

            pantalla.blit(banderas_paises_marcador_der[paises[indice_j1]], (629, 40))
            texto= fuente_5.render(f"{contador_j1}", True, (255, 255, 255))
            pantalla.blit(texto, (564, 63))

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
            pantalla.blit(banderas_paises_vs[paises[indice_j1]], (693, 162))
            
        elif ganador == 2:
            pantalla.blit(banderas_paises_vs[paises[indice_j2]], (693, 162))

#MENSAJE TANDA EXTRA

    elif escena == "mensaje_tanda_extra":
        pantalla.blit(fondo_tanda_extra, (0,0))

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

#GANADOR DEFAULT
    elif escena == "ganaste_default":
        pantalla.blit(fondo_buscando_cliente, (0,0))
        pantalla.blit(mensaje_default, (106, 48))

#CONEXIÓN PERDIDA
    elif escena == "conexion_perdida":
        pantalla.blit(fondo_buscando_cliente, (0,0))
        pantalla.blit(mensaje_conexion_perdida, (154,53))

        if pygame.time.get_ticks() - tiempo_conexion_perdida > 3000:
            tiempo_conexion_perdida = 0
            escena = "menu_principal"
#------------------------------------------------------------------FIN------------------------------------------------------------
    if escena != "menu_principal" and escena != "conectando" and escena != "conexion_perdida":
        dibujar_boton_img(pantalla, boton_volver_selección, posicion_mouse)
        
        if mensaje_volver:
            pantalla.blit(fondo_volver, (0,0))
            dibujar_boton_img(pantalla, boton_cancelar_volver, posicion_mouse)
            dibujar_boton_img(pantalla, boton_volver_menu, posicion_mouse)

    pygame.display.update()
pygame.quit()
