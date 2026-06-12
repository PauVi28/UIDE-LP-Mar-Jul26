import tkinter as tk
import random
import socket
import threading
from game_logic import determinar_ganador

# ── 1. CONFIGURACIÓN DE LA VENTANA PRINCIPAL ────────────────
ventana = tk.Tk()
ventana.title("Piedra, Papel o Tijera")
ventana.geometry("400x500")
ventana.configure(bg="#1a1a2e")
ventana.resizable(False, False)

# Variables globales para controlar los textos y botones
lbl_tu = None
lbl_ia_o_rival = None
lbl_resultado = None
btn_piedra = None
btn_papel = None
btn_tijera = None

# Variables de control de modo y red
modo_actual = "local" # Puede ser "local" o "multijugador"
socket_cliente = None


def limpiar_pantalla():
    """Borra todos los elementos visuales para cambiar de pantalla"""
    for elemento in ventana.winfo_children():
        elemento.destroy()


# ── 2. PANTALLA: MENÚ PRINCIPAL ─────────────────────────────
def mostrar_menu_principal():
    global socket_cliente
    
    # Si regresamos al menú, cerramos conexiones abiertas por seguridad
    if socket_cliente:
        try:
            socket_cliente.close()
        except:
            pass
        socket_cliente = None

    limpiar_pantalla()

    tk.Label(ventana, text="PIEDRA · PAPEL · TIJERA", bg="#1a1a2e", fg="white",
             font=("Courier New", 14, "bold"), pady=40).pack()

    tk.Label(ventana, text="Selecciona un modo de juego:", bg="#1a1a2e", fg="#aaaaaa",
             font=("Courier New", 11)).pack(pady=10)

    # Botón Modo Local
    tk.Button(ventana, text="🖥️   Juego Local (vs IA)", bg="#16213e", fg="white",
              font=("Courier New", 12, "bold"), width=25, height=2, relief="flat", cursor="hand2",
              command=iniciar_modo_local).pack(pady=10)

    # Botón Modo Multijugador (¡Automático por cable Ethernet!)
    tk.Button(ventana, text="🌐   Juego Multijugador", bg="#0f3460", fg="white",
              font=("Courier New", 12, "bold"), width=25, height=2, relief="flat", cursor="hand2",
              command=iniciar_modo_multijugador).pack(pady=10)

    # Botón Salir
    tk.Button(ventana, text="🚪   Salir", bg="#16213e", fg="white",
              font=("Courier New", 12, "bold"), width=25, height=2, relief="flat", cursor="hand2",
              command=ventana.destroy).pack(pady=10)


# ── 3. PANTALLA ÚNICA DE JUEGO (LA MISMA INTERFAZ PARA TODO) ──
def mostrar_tablero_juego(titulo_modo, mensaje_estado, botones_activos=True):
    global lbl_tu, lbl_ia_o_rival, lbl_resultado, btn_piedra, btn_papel, btn_tijera
    limpiar_pantalla()

    tk.Label(ventana, text=titulo_modo, bg="#1a1a2e", fg="white", 
             font=("Courier New", 13, "bold"), pady=15).pack()
    
    tk.Label(ventana, text="Elige tu jugada haciendo clic:", bg="#1a1a2e", fg="#aaaaaa", 
             font=("Courier New", 11)).pack(pady=10)

    # Estado inicial de los botones según la conexión
    estado_inicial = "normal" if botones_activos else "disabled"

    # Botones gráficos interactivos
    btn_piedra = tk.Button(ventana, text="🪨 Piedra", bg="#16213e", fg="white", font=("Courier New", 11, "bold"), 
                           width=16, height=2, relief="flat", state=estado_inicial, command=lambda: procesar_eleccion("piedra"))
    btn_piedra.pack(pady=5)

    btn_papel = tk.Button(ventana, text="📄 Papel", bg="#16213e", fg="white", font=("Courier New", 11, "bold"), 
                          width=16, height=2, relief="flat", state=estado_inicial, command=lambda: procesar_eleccion("papel"))
    btn_papel.pack(pady=5)

    btn_tijera = tk.Button(ventana, text="✂️ Tijera", bg="#16213e", fg="white", font=("Courier New", 11, "bold"), 
                           width=16, height=2, relief="flat", state=estado_inicial, command=lambda: procesar_eleccion("tijera"))
    btn_tijera.pack(pady=5)

    tk.Frame(ventana, bg="#2a2a2a", height=2).pack(fill="x", padx=40, pady=15)

    # Etiquetas de texto informativas
    lbl_tu = tk.Label(ventana, text="Tú: Esperando elección...", bg="#1a1a2e", fg="white", font=("Courier New", 11))
    lbl_tu.pack()

    lbl_ia_o_rival = tk.Label(ventana, text="Rival: ---", bg="#1a1a2e", fg="#aaaaaa", font=("Courier New", 11))
    lbl_ia_o_rival.pack()

    color_msg = "#ffd166" if not botones_activos else "white"
    lbl_resultado = tk.Label(ventana, text=mensaje_estado, bg="#1a1a2e", fg=color_msg, font=("Courier New", 13, "bold"), pady=10)
    lbl_resultado.pack()

    tk.Button(ventana, text="← Volver al menú", bg="#1a1a2e", fg="#aaaaaa", font=("Courier New", 9),
              relief="flat", command=mostrar_menu_principal).pack(pady=5)


# ── 4. CONTROLADOR DE JUGADAS (LOCAL VS MULTIJUGADOR) ────────
def procesar_eleccion(jugada):
    """Se ejecuta inmediatamente cuando haces clic en Piedra, Papel o Tijera"""
    global modo_actual
    
    # Bloqueamos botones para evitar doble clic erróneo
    btn_piedra.config(state="disabled")
    btn_papel.config(state="disabled")
    btn_tijera.config(state="disabled")
    
    lbl_tu.config(text=f"Tú elegiste: {jugada.capitalize()}")

    if modo_actual == "local":
        # Lógica contra la IA instantánea
        opciones = ['piedra', 'papel', 'tijera']
        jugada_ia = random.choice(opciones)
        resultado = determinar_ganador(jugada, jugada_ia)
        
        lbl_ia_o_rival.config(text=f"IA eligió: {jugada_ia.capitalize()}")
        if resultado == "ganas": lbl_resultado.config(text="¡Ganaste! 🎉", fg="#00ff87")
        elif resultado == "pierdes": lbl_resultado.config(text="Perdiste 😔", fg="#ff4d6d")
        else: lbl_resultado.config(text="Empate 🤝", fg="#ffd166")
        
    else:
        # Lógica Multijugador: Enviar jugada por la red en segundo plano
        lbl_resultado.config(text="Esperando la jugada del rival...", fg="#ffd166")
        threading.Thread(target=hilo_intercambio_red, args=(jugada,), daemon=True).start()


# ── 5. LÓGICA DE DETECCIÓN Y CONFIGURACIÓN DE RED AUTOMÁTICA ──

def iniciar_modo_local():
    global modo_actual
    modo_actual = "local"
    mostrar_tablero_juego("MODO LOCAL: VS IA", "¡Elige para jugar!")


def iniciar_modo_multijugador():
    global modo_actual
    modo_actual = "multijugador"
    
    # Dibujamos la pantalla bloqueada mientras se establece la conexión
    mostrar_tablero_juego("MODO MULTIJUGADOR (RED)", "Configurando conexión por cable...", botones_activos=False)
    
    # Lanzamos el analizador automático de red en segundo plano
    threading.Thread(target=hilo_detector_de_rol, daemon=True).start()


def hilo_detector_de_rol():
    """Detecta qué IP tiene esta computadora en su tarjeta de red para saber si es Host o Invitado"""
    IP_SERVIDOR_CABLE = '192.168.1.1'
    
    try:
        # Intentamos obtener la IP de nuestra propia máquina conectada
        nombre_equipo = socket.gethostname()
        ips_locales = socket.gethostbyname_ex(nombre_equipo)[2]
    except:
        ips_locales = []

    # Si nuestra IP es la 192.168.1.1, significa que SOMOS EL SERVIDOR
    if IP_SERVIDOR_CABLE in ips_locales:
        ventana.after(0, lambda: lbl_resultado.config(text="Eres el HOST. Esperando al rival..."))
        threading.Thread(target=hilo_servidor_backend, daemon=True).start()
        threading.Thread(target=hilo_cliente_backend, args=("127.0.0.1",), daemon=True).start()
    else:
        # Si no tenemos esa IP, asumimos que somos el INVITADO e intentamos conectar por el cable
        ventana.after(0, lambda: lbl_resultado.config(text="Eres INVITADO. Conectando al Host..."))
        threading.Thread(target=hilo_cliente_backend, args=(IP_SERVIDOR_CABLE,), daemon=True).start()


def hilo_servidor_backend():
    """Lógica del servidor para sincronizar a ambos jugadores por red"""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', 65432))
        server.listen(2)

        conn1, addr1 = server.accept()
        conn2, addr2 = server.accept()

        # Desbloquea las interfaces de ambos al estar conectados
        conn1.sendall("START".encode())
        conn2.sendall("START".encode())

        j1 = conn1.recv(1024).decode().strip()
        j2 = conn2.recv(1024).decode().strip()

        resultado = determinar_ganador(j1, j2)

        if resultado == "empate":
            conn1.sendall("Empate 🤝".encode())
            conn2.sendall("Empate 🤝".encode())
        elif resultado == "ganas":
            conn1.sendall("Ganaste 🎉".encode())
            conn2.sendall("Perdiste 😔".encode())
        else:
            conn1.sendall("Perdiste 😔".encode())
            conn2.sendall("Ganaste 🎉".encode())

        conn1.close()
        conn2.close()
        server.close()
    except:
        pass


def hilo_cliente_backend(ip_destino):
    """Conecta el socket de la interfaz gráfica al flujo de red"""
    global socket_cliente
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket_cliente.connect((ip_destino, 65432))
        msg = socket_cliente.recv(1024).decode()
        if msg == "START":
            # Cuando el servidor da luz verde, activamos los botones en Tkinter
            ventana.after(0, activar_interfaz_multijugador)
    except:
        ventana.after(0, lambda: lbl_resultado.config(text="Error de conexión por cable ❌", fg="#ff4d6d"))


def activar_interfaz_multijugador():
    btn_piedra.config(state="normal")
    btn_papel.config(state="normal")
    btn_tijera.config(state="normal")
    lbl_resultado.config(text="¡Conectados! Hagan su elección.", fg="#00ff87")
    lbl_ia_o_rival.config(text="Rival: Conectado ✅")


def hilo_intercambio_red(jugada):
    global socket_cliente
    try:
        socket_cliente.sendall(jugada.encode())
        final = socket_cliente.recv(1024).decode()
        
        color = "#ffd166"
        if "Ganaste" in final: color = "#00ff87"
        elif "Perdiste" in final: color = "#ff4d6d"
        
        ventana.after(0, lambda: lbl_resultado.config(text=final, fg=color))
    except:
        ventana.after(0, lambda: lbl_resultado.config(text="Conexión perdida ❌", fg="#ff4d6d"))


# ── 6. INICIO DE LA APLICACIÓN ──────────────────────────────
mostrar_menu_principal()
ventana.mainloop()