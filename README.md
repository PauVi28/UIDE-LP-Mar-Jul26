# FuriosCar2D - Juego de Carreras Multijugador LAN / Local

**FuriosCar2D** es un videojuego de carreras desarrollado en Python con Pygame y comunicación por sockets TCP.  
Permite jugar en **modo local** (un jugador) o en **modo multijugador** en red local (LAN) con dos jugadores.

## 🎮 Características

- Menú de selección de modo (Local / Multijugador) con imagen personalizada.
- Modo local: un solo coche esquivando obstáculos durante 60 segundos.
- Modo multijugador: dos jugadores compiten en carriles separados, usando sockets TCP.
- HUD (interfaz superior) con fuente retro pixelada, puntuación y temporizador.
- Obstáculos con el mismo diseño de coches enemigos.
- Portadas personalizadas para cada jugador.
- Código modular sin clases, utilizando diccionarios y funciones.

## 📁 Estructura del proyecto
FuriosCar2D/
├── server.py # Servidor para modo multijugador
├── client.py # Cliente unificado (local + multijugador)
├── game_logic.py # Lógica compartida (coches, obstáculos, partículas)
├── PressStart2P-Regular.ttf # Fuente pixelada (SIL Open Font License)
├── assets/ # Imágenes de portada (opcional)
│-- Portadamenu.png
│-- portadaJ1.png
│-- portadaJ2.png
│-- portada_local.png
├── README.md
├── LICENCIA.txt

## 🧰 Requisitos

- Python 3.8 o superior
- Pygame 2.5.0 o superior

Instala Pygame con:

```bash
pip install pygame

Como jugar
Modo local (un jugador)
Abre una terminal en la carpeta del proyecto.

Ejecuta:
python client.py
En el menú de selección, presiona 1 (Modo Local).

En la pantalla de portada, presiona la tecla O para iniciar.

Controles: A / D para moverte.

Modo multijugador (LAN)
Servidor (Jugador 1):

Abre una terminal y ejecuta:
python server.py
En otra terminal, ejecuta:
python client.py
Elige opción 2 (Multijugador) y presiona enter en la terminal del client.py para jugar como localhost

Cliente (Jugador 2)
En la otra pc que debe estar conectada a la misma red LAN 
Ejecuta:
python client.py
Elige la opcion 2 para jugar en multijugador
En la terminal ingresa la IPv4 de la maquina que este actuando como servidor y dar enter
Para iniciar el juego el servidor debe presionar la tecla espacio
Controles multijugador
Jugador	Movimiento
Jugador 1	A / D
Jugador 2	← / →

Privacidad y Seguridad
Este juego no recopila, almacena ni transmite información personal. La comunicación en modo multijugador se realiza mediante sockets TCP en red local y solo se intercambian comandos de teclas y el estado del juego (posiciones, puntuaciones).
El código no contiene vulnerabilidades intencionales ni software malicioso.

🧑‍🤝‍🧑 Desarrolladores
[Cristian Vilca] – Lógica del servidor, comunicación TCP, game_logic

[Ricardo Carrion] – Interfaz gráfica, menús, HUD

[Juan Esteban] – Diseño visual, assets, pruebas

ASISTENCIA DE IA
Durante el desarrollo se utilizaron herramientas de inteligencia artificial (Claude de Anthropic y DeepSeek) como asistentes en la depuración, refactorización y mejora de la interfaz gráfica. Todas las sugerencias fueron revisadas e integradas manualmente por el equipo de desarrollo

LICENCIA
Este proyecto se distribuye bajo la Licencia MIT. Consulta el archivo LICENSE.txt para más detalles.

Fuente tipográfica: Press Start 2P por CodeMan38 (SIL Open Font License).
Motor gráfico: Pygame (LGPL).