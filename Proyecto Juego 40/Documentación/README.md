Este proyecto es un juego del 40 ecuatoriano hecho en Python. Se puede jugar contra la computadora o con otra persona en la misma red local (LAN). El servidor es el que controla todo: las cartas, las reglas y los puntos. El cliente solo muestra la partida y envía las jugadas.

Requisitos
Tener instalado Python 3.12 o más nuevo.

Instalar Pygame.

Una computadora con pantalla.

Para jugar en LAN: dos PCs conectadas a la misma red.

Instalación
Descarga Python desde la página oficial.

Instala Pygame con el comando:

Código
pip install pygame
Los sonidos ya están listos, pero si quieres recrearlos puedes correr:

Código
python generar_sonidos.py
Cómo jugar
Dentro de la carpeta Codigo_Fuente/ tienes dos formas de jugar:

Modo LAN (dos PCs):

En el host:

Código
python server.py
En el cliente:

Código
python client.py IP_DEL_HOST
(Cambias “IP_DEL_HOST” por la dirección de la otra PC).

Menú completo (una sola ventana):

Código
python juego.py
Aquí puedes elegir: jugar contra la CPU, jugar en LAN (ser host o unirse) o salir.

Reglas básicas
Cada jugador recibe 5 cartas.

La mesa empieza vacía.

En tu turno eliges una carta para jugar.

Si coincide con cartas de la mesa, las capturas.

Capturar la última carta del rival = caída (+2).

Dejar la mesa vacía = limpia (+2).

Al final de la ronda, quien tenga más cartas suma +6.

Gana quien llega primero a 40 puntos.
