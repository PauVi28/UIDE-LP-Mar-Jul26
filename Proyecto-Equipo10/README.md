# Mundialinho De Penales 2026 😎

Proyecto integrador desarrollado para fin de semestre de la carrera Ingeniería en Sistemas de Información | Primer Nivel — UIDE, periodo Marzo–Julio 2026.

El proyecto consiste en un videojuego de tanda de penales inspirado en una final mundialista de fútbol desarrollado en Python con la librería Pygame, especializada en el desarrollo de videojuegos mediante la manipulación de elementos como sonido, audio e interacción. El juego cuenta con un modo local por turnos y una arquitectura multijugador cliente-servidor mediante sockets TCP para partidas LAN.

-----------------------------

# Integrantes

- Paco Choez
- José Estévez

-----------------------------

# Características del Proyecto

## Modo Local
- Sistema de tanda de penales por turnos alternados
- Selección de dirección de disparo y atajada
- Marcador dinámico
- Detección automática de ganador
- Tanda extra en caso de empate

##  Modo Multijugador LAN
- Arquitectura cliente-servidor
- Comunicación mediante sockets TCP
- Sincronización de jugadas entre jugadores
- Sistema de turnos sincronizada
- Procesamiento centralizado de resultados
- Conexión entre computadoras en red local
- Compatibilidad con máquinas virtuales

-----------------------------

# Estructura del Proyecto

```text
Proyecto_Grupo10/
├── Código Fuente/
│   ├── juegoServer.py
│   ├── juegoCliente.py
│   └── RecursosSI/
│       ├── Animaciones/
│       ├── Botones/
│       ├── Fondos/
│       ├── Mensajes/
│       ├── Selecciones/
│       ├── Sonidos/
│       └── PressStart2P.ttf
├── Documentación/
│   ├── Informe_Técnico.pdf
│   ├── README.md
│   ├── LICENSE
│   └── Evidencias/
└── Video_Demostrativo.mp4
```

El proyecto final se ejecuta mediante dos archivos principales: `juegoServer.py`, correspondiente al Jugador 1 en rol de servidor, y `juegoCliente.py`, correspondiente al Jugador 2 en rol de cliente. La carpeta `RecursosSI` contiene los elementos gráficos, sonoros y tipográficos necesarios para el funcionamiento visual e interactivo del videojuego.
```

-----------------------------

# Tecnologías Utilizadas

- Python
- Pygame CE
- Sockets TCP
- Threading
- GitHub
- Arquitectura Cliente-Servidor
- Máquinas Virtuales en Oracle Virtual Box

-----------------------------

# ▶Ejecución del Proyecto

## Instalar Pygame

```bash
pip install pygame-ce
```

## Ejecutar Servidor

```bash
python3 juegoServer.py
```

## Ejecutar Cliente

```bash
python3 juegoCliente.py
```

-----------------------------

## Lógica Base del Juego

El sistema recrea una tanda de penales tradicional.  
Cada jugador selecciona una dirección:

- 1 → Izquierda
- 2 → Centro
- 3 → Derecha

Si la dirección del disparo es distinta a la dirección de atajada, se registra un gol. En caso contrario, el penal es detenido.

El sistema controla:
- cantidad de penales restantes
- diferencia matemática de goles
- finalización anticipada
- tanda extra en caso de empate

-----------------------------

Todo el código final del proyecto fue revisado, comprendido, adaptado y desarrollado por los integrantes del equipo como parte del proceso académico del Proyecto Integrador de Primer Nivel.

Durante el desarrollo del videojuego se utilizaron herramientas de inteligencia artificial como ChatGPT, Gemini y Claude únicamente como instrumentos de apoyo educativo para:
- comprensión de errores de programación
- depuración de bugs
- explicación de lógica de sockets TCP
- organización modular del código
- apoyo en documentación técnica
- orientación en arquitectura cliente-servidor
- asistencia en la estructuración de lógica del juego

La inteligencia artificial fue utilizada exclusivamente con fines académicos y de aprendizaje, manteniendo siempre la revisión y comprensión del código por parte de los integrantes del equipo.

## Recursos externos, autoría y uso académico

El proyecto utiliza recursos visuales, sonoros y tipográficos para mejorar la experiencia del usuario durante la partida. Con el fin de mantener transparencia sobre la autoría y el uso de estos elementos, se detalla el origen general de los recursos incorporados al videojuego.

Recursos visuales propios

Los archivos correspondientes a animaciones, botones, indicadores visuales, selecciones, banderas, mensajes y elementos del marcador fueron elaborados por el equipo como parte del desarrollo del proyecto.

Estos recursos se encuentran principalmente en las siguientes carpetas:

RecursosSI/Animaciones/
RecursosSI/Botones/
RecursosSI/Selecciones/
RecursosSI/Mensajes/

Dentro del videojuego, estos elementos se utilizan para representar el sorteo, los jugadores, los arqueros, el balón, las decisiones de penal, los botones de navegación, las confirmaciones, los mensajes de conexión y el marcador visual de la tanda de penales.

-----------------------------

Fondos generados con apoyo de inteligencia artificial

Los fondos del juego, ubicados en RecursosSI/Fondos/, fueron generados con apoyo de herramientas de inteligencia artificial a partir de ideas, indicaciones y referencias visuales planteadas por el equipo.

Estos fondos se utilizaron para ambientar las diferentes escenas del videojuego, como el menú principal, la selección de equipos, la búsqueda de conexión, el sorteo, la escena de penal, los resultados, la tanda extra y la pantalla de ganador.

-----------------------------

Recursos sonoros externos

Los efectos de sonido y la música de fondo fueron obtenidos desde videos de YouTube y utilizados únicamente con fines académicos y demostrativos dentro del Proyecto Integrador.

Estos recursos se encuentran en:

RecursosSI/Sonidos/Clicks/
RecursosSI/Sonidos/Efectos/
RecursosSI/Sonidos/Fondo/

Entre los sonidos utilizados se incluyen efectos de click, selección de decisión, error, pateo, red, atajada, silbato, hinchada, moneda y música de fondo estilo 8-bit. Su finalidad es mejorar la retroalimentación del usuario y reforzar la ambientación futbolística del videojuego.

-----------------------------

Fuente tipográfica

El proyecto utiliza la fuente PressStart2P.ttf, ubicada en RecursosSI/PressStart2P.ttf, para mantener una estética retro y pixel art en los textos del juego.

Consideración sobre derechos de uso

Todos los recursos fueron incorporados con fines académicos, educativos y demostrativos. Los elementos visuales propios fueron desarrollados por el equipo, mientras que los fondos fueron generados con apoyo de inteligencia artificial y los recursos sonoros fueron obtenidos desde videos de YouTube.

En caso de publicación, distribución externa o uso comercial del proyecto, se recomienda reemplazar los recursos sonoros obtenidos desde YouTube por archivos con licencia libre, recursos Creative Commons o sonidos con permiso explícito de uso, debido a que citar una fuente no reemplaza necesariamente la autorización legal del recurso.


## Librerías utilizadas
- Python Standard Library
- socket
- threading
- pygame

-----------------------------

# Licencia

Este proyecto utiliza la licencia MIT para el código fuente desarrollado por el equipo. Esta licencia permite usar, copiar, modificar y distribuir el software, siempre que se mantenga el aviso de copyright y los términos de la licencia.

El texto completo de la licencia se encuentra en el archivo LICENSE del repositorio.

Es importante aclarar que la licencia MIT aplica al código fuente desarrollado por los integrantes del equipo. Los recursos externos utilizados, como sonidos obtenidos desde videos de YouTube y fondos generados con apoyo de inteligencia artificial, se documentan por separado en la sección de recursos externos y fueron incorporados únicamente con fines académicos y demostrativos.

-----------------------------

#  Estado del Proyecto

FINALIZADO EN ESPERA DE PRESENTAR 😎 | FASE 6
