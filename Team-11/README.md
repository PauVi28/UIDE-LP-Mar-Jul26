# ForgottenTale

**ForgottenTale** es un prototipo de videojuego de combate multijugador asíncrono estilo RPG (2D) escrito completamente en Python utilizando el motor gráfico **Pygame**. El proyecto demuestra mecánicas de juego en red a través de sockets TCP, máquinas de estado de animación y diseño centrado en el jugador.

---

## 📚 Integridad Académica y Propiedad Intelectual

Este proyecto fue desarrollado con fines estrictamente educativos y académicos para demostrar habilidades de ingeniería de software, arquitectura de redes (Cliente-Servidor) y programación orientada a objetos en Python.

*   **Asistencia de Inteligencia Artificial:** Partes de la reestructuración del código, optimización del rendimiento y refactorización fueron realizadas mediante colaboración (Pair Programming) con asistentes de IA avanzada, utilizados como herramienta de apoyo metodológico y técnico para cumplir con los estándares de diseño y limpieza de código.
*   **Librerías Externas:** Todo el renderizado gráfico, control de FPS y manejo de eventos es gestionado por la librería Open Source **Pygame**.
*   **Recursos Audiovisuales (Fair Use):** La música, los efectos de sonido, las imágenes de fondo y los sprites de los personajes involucrados (*Mario, Luigi, Bowser*) pertenecen exclusivamente a **Nintendo Co., Ltd.** No reclamamos ninguna autoría sobre estos activos. Son utilizados bajo la doctrina de uso justo (*Fair Use*) con el único fin de crear un prototipo educativo, no comercial y sin fines de lucro.

## 📄 Licenciamiento (Open Source)

El código fuente original que da vida a este prototipo (incluyendo la lógica de servidor, la máquina de estados, el manejo de sockets y la interfaz gráfica) se distribuye de manera ética bajo el modelo de código abierto con la **Licencia MIT**. 

Cualquier desarrollador, estudiante o investigador es libre de clonar, estudiar, modificar y distribuir el **código**, siempre que se mantenga el aviso de copyright original. *(Nota: Esta licencia aplica únicamente al código; los archivos multimedia están sujetos a los derechos de sus autores originales, mencionados en la sección anterior).*

Para leer los detalles completos de uso, por favor consulta el archivo `LICENSE` incluido en este repositorio.

## 🔒 Privacidad y Seguridad

Este software fue diseñado poniendo la privacidad, la seguridad y el control del usuario en primer lugar:

1.  **Transparencia de Conexión LAN:** La función multijugador utiliza exclusivamente conexiones directas entre pares (TCP Sockets) dentro de redes de área local (LAN). **No existen servidores intermediarios ocultos, telemetría, ni recolección de datos en la nube.** El juego únicamente transmitirá información hacia la dirección IP que el propio usuario introduzca voluntariamente mediante el código de sala o PIN numérico en pantalla.
2.  **Manejo de Datos de Red:** Los datos transferidos entre jugadores constan estrictamente de estados de juego empaquetados en formato JSON (coordenadas `X/Y`, nivel de `hp`, pulsaciones de la tecla `Enter`, e identificadores de animación). No se transfiere, lee, ni expone ninguna información personal, hardware, contraseñas o archivos del sistema del usuario.
3.  **Código Seguro y Abierto:** El código fuente completo es auditable y libre de ofuscación. Garantizamos que la arquitectura ha sido revisada para asegurar que no contiene puertas traseras (backdoors), vulnerabilidades intencionales ni ningún tipo de software malicioso. Las conexiones de red finalizan y los puertos se liberan inmediatamente al cerrar la ventana del juego o al detectar una desconexión.
