# 📋 Bitácora de Gestión de Conflictos — Fórmula Asertiva

**Proyecto:** Piedra, Papel o Tijera  
**Equipo:** [Nombre del equipo]  
**Fase:** 3 — Inicio del Desarrollo (Semanas 11–12)

---

## Conflicto #1: Error de módulo al ejecutar el código

### 🔍 Hechos
Al intentar ejecutar el juego, Python lanzó el error `ModuleNotFoundError: No module named 'game_logic'`. Esto ocurrió porque todo el código fue escrito en un único archivo `.py`, cuando la arquitectura del proyecto requiere que cada componente esté en su propio archivo separado (`game_logic.py`, `juego.py`, `server.py`, `client.py`).

### 💬 Sentimientos
La situación generó frustración en el equipo al no poder ver el programa funcionar, y cierta incertidumbre sobre si la arquitectura cliente-servidor era más compleja de lo esperado.

### ✅ Necesidades
El proyecto requiere que los archivos estén correctamente separados en módulos independientes, todos ubicados en la misma carpeta, para que Python pueda importar correctamente las funciones entre archivos.

### 🤝 Petición
Se acordó como equipo revisar la estructura de carpetas antes de ejecutar cualquier archivo, asegurando que los 4 módulos (`game_logic.py`, `juego.py`, `server.py`, `client.py`) estén siempre en el mismo directorio. Además, se estableció probar el modo local primero antes de avanzar al modo multijugador.

---

## Conflicto #2: [Agregar otro conflicto real del equipo aquí]

### 🔍 Hechos
[Descripción objetiva del problema]

### 💬 Sentimientos
[Impacto en el equipo]

### ✅ Necesidades
[Qué necesita el proyecto para avanzar]

### 🤝 Petición
[Solución concreta propuesta]
