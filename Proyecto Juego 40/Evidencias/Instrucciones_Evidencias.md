[INSTRUCCIONES_EVIDENCIAS.md](https://github.com/user-attachments/files/28980494/INSTRUCCIONES_EVIDENCIAS.md)
# Evidencias — qué capturar y cómo

Esta carpeta debe contener las **capturas de pantalla reales** tomadas en sus
dos máquinas virtuales. No se pueden generar de antemano porque son la prueba de
que la red y el juego funcionan en su entorno. Aquí está, exactamente, qué debe
mostrar cada imagen y los comandos para obtenerla.

Nombres de archivo esperados (PNG):

```
Evidencias/
├── ip.png          configuración / direcciones IP de las dos VMs
├── ping.png        prueba de ping entre las máquinas
├── servidor.png    servidor (host) en ejecución
├── cliente.png     cliente conectado
└── pruebas.png     el juego funcionando (jugadas y/o ganador)
```

Para tomar una captura: en Windows usa la tecla **Impr Pant** o la app
**Recortes**; en Linux usa **Captura de pantalla** o `gnome-screenshot`.

---

## 1. ip.png — Configuración IP
Mostrar la dirección IP de cada VM (idealmente las dos máquinas en la imagen, o
dos capturas combinadas).
- Windows: abrir CMD y ejecutar `ipconfig`
- Linux: ejecutar `ip addr` (o `ifconfig`)
Debe verse la IPv4 de cada máquina (por ejemplo 192.168.1.10 y 192.168.1.11) y
que están en la misma subred.

## 2. ping.png — Prueba de conectividad
Desde una VM hacer ping a la otra y mostrar que responde:
- `ping 192.168.1.10` (poner la IP de la otra máquina)
Debe verse que llegan las respuestas y **0% de paquetes perdidos**.
Recomendado: una captura de cliente→host y, si se puede, también host→cliente.

## 3. servidor.png — Servidor en ejecución
En el host, dentro de `Codigo_Fuente/`, ejecutar:
- `python server.py`
Capturar la terminal con el mensaje "Escuchando en 0.0.0.0:5050 ..." junto a la
ventana "SERVIDOR ACTIVO / Esperando a que se conecte un jugador...".

## 4. cliente.png — Cliente conectado
En la otra VM ejecutar:
- `python client.py <IP_DEL_HOST>`
Capturar la consola del cliente con "Conectado al servidor." y la ventana del
juego ya abierta. (Si pueden, que se vea también que el host dice
"Cliente conectado.")

## 5. pruebas.png — Funcionamiento del juego
Capturar el juego en marcha mostrando AMBAS pantallas: una jugada/captura en la
mesa, los marcadores, y/o el cartel final "GANASTE / GANO EL RIVAL" cuando
alguien llega a 40. Pueden incluir más de una captura si quieren (pruebas1.png,
pruebas2.png, etc.).

---

### Consejo
Pongan en cada captura algo que identifique la máquina (el nombre del equipo o
su IP visible en la terminal). Así queda claro que la prueba se hizo entre dos
máquinas distintas y no en una sola.
