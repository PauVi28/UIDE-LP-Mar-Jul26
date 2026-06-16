[README.md](https://github.com/user-attachments/files/28980481/README.md)
# Juego del "40" ecuatoriano — Multijugador LAN (Python + Pygame + Sockets TCP)

Proyecto del juego de cartas del **40** (Cuarenta) desarrollado en Python con
Pygame. Permite jugar **contra la CPU** o **entre dos máquinas en red local
(LAN)** usando **sockets TCP**.

El **servidor (host)** controla toda la lógica del juego (mazo, capturas,
caídas, limpias, puntos y ganador). El **cliente** solo muestra el estado que
recibe y envía sus jugadas. Es decir, nunca hay dos mazos ni dos lógicas: una
sola fuente de verdad en el servidor.

La interfaz está inspirada visualmente en Balatro (fondo oscuro con humo rojo y
turquesa, botones biselados y un logo "40" con un As de espadas), pero las
reglas son las del 40 tradicional.

---

## 1. Requisitos

- **Python 3.12** o superior
- **Pygame 2.x**
- Sistema con entorno gráfico (la interfaz usa una ventana)
- Para el modo LAN: dos máquinas en la misma red (cable Ethernet o misma red
  local) que puedan hacerse **ping** entre sí.

---

## 2. Instrucciones de instalación

1. Instalar Python 3.12+ desde https://www.python.org (en Windows, marcar
   "Add Python to PATH" durante la instalación).
2. Instalar Pygame:

   ```
   pip install pygame
   ```

3. (Opcional) Regenerar los sonidos: ya vienen incluidos en
   `assets/sonidos/`, pero se pueden volver a crear con:

   ```
   python generar_sonidos.py
   ```

---

## 3. Instrucciones de ejecución

Todos los comandos se ejecutan dentro de la carpeta `Codigo_Fuente/`.

### Opción A — Modo LAN con archivos separados (recomendado para la demostración)

En la máquina **servidor (host)**:

```
python server.py
```

Aparece "SERVIDOR ACTIVO / Esperando a que se conecte un jugador..." y en la
consola se imprime el puerto en el que escucha (5050 por defecto).

En la máquina **cliente**:

```
python client.py 192.168.1.10
```

Reemplazar `192.168.1.10` por la **IP del host**. Si se ejecuta
`python client.py` sin la IP, el programa la pedirá por teclado. Apenas se
conecta, empieza la partida en ambas pantallas.

### Opción B — Menú completo (todo en una ventana)

```
python juego.py
```

Abre el menú principal con tres opciones:

- **JUGAR**: partida contra la CPU.
- **MULTIJUGADOR LOCAL**: elegir *SER HOST* o *UNIRSE A PARTIDA* (escribiendo la
  IP del host) desde la misma interfaz.
- **SALIR**.

### Cómo se juega

- Cada jugador recibe 5 cartas; la mesa **inicia vacía**.
- En tu turno, haz clic en una carta de tu mano para lanzarla.
- Si su valor coincide con cartas de la mesa, las **capturas** (van a tu cartón).
- Capturar la última carta que dejó el rival = **caída** (+2).
- Dejar la mesa vacía tras capturar = **limpia** (+2).
- Al terminar la ronda, quien tenga más cartas en el cartón suma **+6**.
- Gana quien llega primero a **40 puntos**.

El puerto TCP se configura en `network/config.py` (por defecto **5050**).

---

## 4. Estructura del código

```
Codigo_Fuente/
  server.py            inicia el SERVIDOR (host) en modo LAN
  client.py            inicia el CLIENTE en modo LAN
  game_logic.py        acceso unico a la logica del juego (reune el paquete logica/)
  juego.py             menu completo (CPU + multijugador en una ventana)
  generar_sonidos.py   genera los efectos de sonido .wav

  logica/
    mazo.py            baraja espanola de 40 cartas
    reglas40.py        capturas, caidas, limpias y conteo del carton
    cpu.py             decision de la maquina (modo vs CPU)
    game40.py          clase Game40 con TODA la logica del juego

  network/
    config.py          puerto y opciones de red
    servidor.py        socket TCP del lado del host
    cliente.py         socket TCP del lado del cliente

  multiplayer/
    estados.py         arma el estado en JSON que viaja por la red
    host.py            une Game40 con el servidor (hilo de escucha)

  ui/
    recursos.py        colores, fuentes, sonidos, fondo, botones y tablero
    menu.py            pantalla principal
    partida.py         pantalla del modo vs CPU
    multijugador.py    elegir ser host o unirse (entrada de IP)
    partida_lan.py     pantalla del juego en red (host y cliente)

  assets/
    sonidos/           efectos .wav (clic, carta, captura, caida, limpia, repartir, ganar)
    cartas/, fondos/   opcionales (las cartas y el fondo se dibujan por codigo)
```

---

## 5. Comunicación por red (resumen técnico)

- Protocolo: **TCP** (sockets de la librería estándar `socket`).
- El host hace `bind` + `listen` + `accept`; el cliente hace `connect`.
- Los mensajes viajan como **JSON**, uno por línea (terminados en `\n`).
- Flujo de una jugada del cliente:
  1. El cliente envía `{"tipo": "jugar", "indice": i}`.
  2. El host la aplica en su `Game40` (resuelve captura/caída/limpia/turno).
  3. El host reenvía el **estado completo** actualizado a ambos.
- El cliente solo dibuja ese estado; nunca calcula reglas.

---

## 6. Repositorio

El enlace al repositorio de GitHub está en `enlace_github.txt`.
