# 📋 Bitácora de Gestión de Conflictos — Fórmula Asertiva

**Proyecto:** Piedra, Papel o Tijera  
**Equipo:** Los Yorch  
**Fase:** 5 — Fase final del desarrollo

---

## Conflicto #1: Error de ip al momento de ejecutar el juego

### Hechos
El dia de hoy 11/6/2026 nos encontrabamos realizando las pruebas para poder conectar nuestro juego en modo multijugador. Estabamos relizando la conexion para que la maquina virtual se conecte con la fisica mediante el cable Ethernet y la configuracion de IPS, pero no valia, a psear de que corregiamos y corregiamos el codigo e IPS, no funcionaba nada 

### Sentimientos
Esto provocó en Alex y Gabriel un sentimiento de agotacion y frustracion, pues llevaban mas de una hora sentados intentando resolver el problema de conexión que tenian 
### Necesidades
Necesitabamos calmarnos, pues nos dimos un respiro, y despejamos nuestras mentes y despues de unos 10 minutos nos volvimos a centrar en el problema y entendimos que era muy facil solucionarlo, pues, las IPS chcaban ya que creiamos que la IP de la maquina fisica del invitado (laptop de Alex) y la de la maquina virtual debian tener la misma IP y no chocarian pero estabamos en lo incorrecto, por ello reemplazamos la de la maquina virtual por la IP de 192.168.1.3 y logramos tener conexion, por lo que entendimos que si deseamo conectar más jugadores tenemos que intercalar en la configuracion de las IPS

### Petición
No tenemos ninguna peticion 

---

## Conflicto #2: Ahorrar tiempo 

### Hechos
Con el grupo, entendimos que, estar ejecutando cliente.py y server.py cada vez que quiiseramos jugar, es un gasto de memoria y de tiempo, por lo que buscamos la manera de que estos 2 apartados del codigo se ejecuten a la vez cuando se abra la interfaz, es decir se ejecute el juego, para asi ahorar tiempo y recursos de memoria y con ayuda de la IA (Gemini) lo logramos

### Sentimientos
Nos sentimos muy bien pues, logramos automatizar 2 tareas para ahorrar recursos

### Necesidades
Necesitabamos automatizar 2 procesos

### Petición
No tenemos ninguna peticion 
