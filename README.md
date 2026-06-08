# ✂️ Piedra, Papel o Tijera — Proyecto UIDE

Juego de Piedra, Papel o Tijera con modo local contra IA y modo multijugador en red LAN mediante sockets TCP.

Desarrollado como proyecto de la asignatura **Lógica de Programación** — Ingeniería en Sistemas de Información, UIDE. Periodo Marzo–Julio 2026.

---

## 🏗️ Estructura del Proyecto

```
ProyectoJuego/
├── game_logic.py   # Lógica del juego (determina ganador)
├── juego.py        # Modo local contra la IA
├── server.py       # Servidor TCP para modo multijugador
├── client.py       # Cliente para conectarse al servidor
├── LICENSE         # Licencia MIT
└── README.md       # Este archivo
```

---

## ▶️ Cómo ejecutar

### Modo Local
```bash
python juego.py
```

### Modo Multijugador LAN
1. En la máquina servidor, correr:
```bash
python server.py
```
2. En cada máquina cliente, editar `client.py` y cambiar `SERVER_IP` por la IP del servidor, luego correr:
```bash
python client.py
```

---

## ⚙️ Stack Técnico

- **Lenguaje:** Python 3
- **Comunicación:** Sockets TCP (`import socket`)
- **Entorno:** Máquinas virtuales en red LAN

---

## 👥 Créditos

| Integrante | Rol |
|---|---|
| [Nombre 1] | Lógica del juego |
| [Nombre 2] | Servidor y cliente |
| [Nombre 3] | Interfaz y pruebas |

> Este proyecto fue desarrollado con apoyo de herramientas de IA (Claude - Anthropic) para depuración y estructura del código. Toda la lógica fue revisada, comprendida y adaptada por el equipo.

---

## 📜 Licencia

MIT License

Copyright (c) 2026 [Nombre del Equipo] — UIDE

Permission is hereby granted, free of charge, to any person obtaining a copy of this software to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
