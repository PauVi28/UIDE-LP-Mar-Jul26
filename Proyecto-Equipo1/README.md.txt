Proyecto: Juego de Adivinar el Número en Red

 Descripción

Este proyecto consiste en un juego multijugador desarrollado en Python utilizando sockets. El objetivo es que varios jugadores intenten adivinar un número aleatorio generado por el servidor.

El primer jugador que logre acertar el número gana la partida.

---

 Características

* Juego cliente-servidor
* Uso de sockets
* Diferentes niveles de dificultad
* Validación de datos
* Comunicación en red
* Soporte para múltiples jugadores

---

 Tecnologías utilizadas

* Python
* Socket
* Threading
* Random

---

 Estructura del proyecto

* `juego.py` → Menú principal
* `server.py` → Servidor del juego
* `client.py` → Cliente jugador
* `game_logic.py` → Lógica del juego
* `README.md` → Documentación
* `LICENSE` → Licencia

---

 Funcionamiento

1. El servidor inicia la partida.
2. Los clientes se conectan mediante IP.
3. El servidor genera un número aleatorio.
4. Los jugadores envían intentos.
5. El servidor responde:

   * Mayor
   * Menor
   * Correcto
6. El primer jugador en acertar gana.

---

 Objetivos

* Aplicar programación en Python.
* Comprender comunicación cliente-servidor.
* Implementar sockets.
* Practicar trabajo modular.
* Simular comunicación en red entre dispositivos.

---

 Posibles mejoras

* Ranking
* Chat entre jugadores
* Temporizador
* Interfaz gráfica
* Base de datos
* Puntajes

---

 Licencia Open Source

Este proyecto está distribuido bajo la licencia MIT License.
Esto permite usar, modificar y distribuir el software libremente con fines educativos y de aprendizaje.

---

 Declaración de Autoría

Este proyecto fue desarrollado por:

* Diego Cisneros
* Cristhoper Pilataxi

El código fue desarrollado con fines académicos para la materia correspondiente de programación y redes.

---

 Recursos Utilizados

Durante el desarrollo del proyecto se utilizaron los siguientes recursos de apoyo:

* Documentación oficial de Python
* Biblioteca estándar `socket`
* Biblioteca estándar `threading`
* Biblioteca estándar `random`
* Apoyo de herramientas de inteligencia artificial para orientación y explicación de conceptos

