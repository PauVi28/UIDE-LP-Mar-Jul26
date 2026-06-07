# Mundialinho De Penales 2026 😎

Proyecto integrador desarrollado para fin de semestre de la carrera Ingeniería en Sistemas de la Información | Primer Nivel — UIDE, periodo Marzo–Julio 2026.

El proyecto consiste en un videojuego de tanda de penales inspirado en una final mundialista de fútbol desarrollado en Python con la librería Pygame, especializada en el desarrollo de videojuegos mediante la manipulación de elementos como sonido, audio e interacción. El juego cuenta con un modo local por turnos y una arquitectura multijugador cliente-servidor mediante sockets TCP para partidas LAN.

-----------------------------

# Integrantes

- Paco Choez
- José Estévez
- Kevin Balseca

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
Proyecto-Equipo10/
│
├── juegoServer.py
├── juegoCliente.py
├── LICENSE
└── README.md
```

-----------------------------

# Tecnologías Utilizadas

- Python
- Pygame CE
- Sockets TCP
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

# Lógica Base del Juego

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

## Recursos de Audio y Multimedia

El proyecto utilizará distintos efectos de sonido y recursos musicales con temática futbolística y estética retro pixelart para mejorar la experiencia del jugador.

Entre los recursos de audio se incluyen:
- efectos de sonido del balón
- sonido de impacto en la red al marcar gol
- sonido de impacto en guantes al atajar gol
- efectos de transición entre escenas
- sonidos ambientales de afición y estadio
- efectos de interacción de interfaz

Además, el videojuego contará con música de fondo estilo 8-bit inspirada en temas futbolísticos y ambientaciones mundialistas, utilizadas con fines educativos y demostrativos dentro del proyecto académico.

Todos los recursos externos utilizados serán referenciados y acreditados adecuadamente dentro de la documentación del proyecto.

## Librerías utilizadas
- Python Standard Library
- socket
- threading
- pygame

-----------------------------

# Licencia

Este proyecto utiliza la licencia MIT.

-----------------------------

#  Estado del Proyecto

🧱🧱🛠️🛠️ 😎En desarrollo😎 🧱🧱🛠️🛠️
Fase Actual: Programación del modo Local y Online LAN | Semana 4
Próxima Fase: Diseño de interfaz de usuario intuitiva | Semana 5
