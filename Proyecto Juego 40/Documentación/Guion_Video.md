[GUION_VIDEO.md](https://github.com/user-attachments/files/28980427/GUION_VIDEO.md)
# Guion del Video Demostrativo (máximo 10 minutos)

El video final debe llamarse **`Video_Demostrativo.mp4`** y colocarse en la raíz
del proyecto (junto a las carpetas `Codigo_Fuente/`, `Documentacion/` y
`Evidencias/`).

> Nota: el video lo deben grabar ustedes con sus dos máquinas virtuales reales,
> porque es la evidencia de que la comunicación funciona en su red. Abajo está
> el guion exacto, segmento por segmento, para que la grabación sea rápida y
> cubra todos los puntos del enunciado. Tiempos sugeridos para no pasar de 10
> minutos.

Sugerencia de grabación: usa OBS Studio (gratis) capturando ambas ventanas, o
graba la pantalla del host y, dentro, ten visible la del cliente (escritorio
remoto / ventana lado a lado). Narra brevemente cada paso.

---

## Minuto 0:00 – 0:40 · Presentación
- Decir el nombre del grupo, integrantes y el tema: "Juego del 40 en red local
  con Python, Pygame y sockets TCP".
- Mostrar rápidamente la estructura de carpetas del proyecto.

## Minuto 0:40 – 2:00 · Configuración de las máquinas virtuales
- Mostrar las dos VMs encendidas (por ejemplo en VirtualBox/VMware).
- Mostrar la configuración de red de cada una (adaptador en modo
  "Red interna" o "Bridge", según corresponda).
- Mostrar la IP de cada máquina:
  - Windows: `ipconfig`
  - Linux: `ip addr` o `ifconfig`

## Minuto 2:00 – 3:00 · Verificación de conectividad (ping)
- Desde el cliente hacer ping al host y viceversa:
  - `ping 192.168.x.x`
- Mostrar que responden (0% de pérdida de paquetes).

## Minuto 3:00 – 4:00 · Inicio del servidor
- En el host, abrir la terminal en `Codigo_Fuente/` y ejecutar:
  - `python server.py`
- Mostrar el mensaje de consola: "Escuchando en 0.0.0.0:5050" y la ventana
  "SERVIDOR ACTIVO / Esperando a que se conecte un jugador...".

## Minuto 4:00 – 5:00 · Conexión del cliente
- En la otra VM ejecutar:
  - `python client.py <IP_DEL_HOST>`
- Mostrar en consola "Conectando a ..." y "Conectado al servidor".
- Mostrar que en el host aparece "Cliente conectado. Iniciando partida." y que
  ambas ventanas pasan al tablero del juego.

## Minuto 5:00 – 8:30 · Comunicación por sockets e intercambio de jugadas
- Jugar varios turnos mostrando AMBAS pantallas.
- Señalar que cuando uno lanza una carta, la otra pantalla se actualiza al
  instante (es el estado viajando por el socket TCP).
- Mostrar al menos una **captura**, y si se da, una **caída** o una **limpia**.
- Comentar que el servidor es quien resuelve toda la lógica y reparte de nuevo
  cuando ambos se quedan sin cartas.

## Minuto 8:30 – 9:30 · Determinación del ganador
- Continuar hasta que un jugador llegue a 40 puntos.
- Mostrar el cartel "GANASTE" / "GANO EL RIVAL" en las dos pantallas.

## Minuto 9:30 – 10:00 · Cierre
- Confirmar que el modo multijugador funcionó de extremo a extremo.
- Despedida breve.

---

### Lista de verificación (todo debe aparecer en el video)
- [ ] Configuración de las máquinas virtuales
- [ ] Comunicación entre las máquinas (ping correcto)
- [ ] Inicio del servidor
- [ ] Conexión del cliente
- [ ] Comunicación mediante sockets TCP (las pantallas se sincronizan)
- [ ] Intercambio de jugadas
- [ ] Determinación del ganador
- [ ] Funcionamiento correcto del modo multijugador
