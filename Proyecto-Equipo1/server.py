import tkinter as tk
from tkinter import simpledialog, scrolledtext
import socket
import threading
import game_logic

class VentanaServidor:
    def __init__(self):
        self.raiz = tk.Tk()
        self.raiz.title("Servidor - Jugador 1")
        self.raiz.geometry("550x500")
        self.raiz.config(bg="#121214")
        self.raiz.resizable(False, False)
        
        self.titulo = tk.Label(self.raiz, text="SERVIDOR: JUGADOR 1", font=("Segoe UI", 16, "bold"), bg="#121214", fg="#4ade80")
        self.titulo.pack(pady=(20, 10))
        
        self.consola = scrolledtext.ScrolledText(self.raiz, width=58, height=18, font=("Consolas", 10), bg="#1e1e24", fg="#f1f5f9", bd=0, highlightthickness=1, highlightbackground="#2a2a35", highlightcolor="#4ade80")
        self.consola.pack(pady=10, padx=15)
        self.consola.config(state="disabled")
        
        self.marco_entrada = tk.Frame(self.raiz, bg="#121214")
        self.marco_entrada.pack(pady=10)
        
        self.entrada_intento = tk.Entry(self.marco_entrada, font=("Segoe UI", 12), width=15, bg="#1e1e24", fg="#ffffff", insertbackground="white", state="disabled")
        self.entrada_intento.pack(side=tk.LEFT, padx=5)
        
        self.btn_enviar = tk.Button(self.marco_entrada, text="Enviar Intento", font=("Segoe UI", 10, "bold"), bg="#4ade80", fg="#121214", state="disabled", command=self.enviar_intento_j1)
        self.btn_enviar.pack(side=tk.LEFT, padx=5)
        
        self.conexion = None
        self.numero_secreto = 0
        self.limite_superior = 100
        self.mi_turno = False
        
        self.entrada_intento.bind("<Return>", lambda event: self.enviar_intento_j1())

    def agregar_texto(self, texto):
        self.consola.config(state="normal")
        if "=== " in texto or "--- " in texto:
            self.consola.insert(tk.END, f"\n{texto}\n", "titulo")
        elif "[VICTORIA]" in texto or "GANASTE" in texto:
            self.consola.insert(tk.END, f"\n{texto}\n", "victoria")
        elif "[ERROR]" in texto or "PERDISTE" in texto:
            self.consola.insert(tk.END, f"\n{texto}\n", "error")
        else:
            self.consola.insert(tk.END, f"  -> {texto}\n", "normal")
        
        self.consola.tag_config("titulo", foreground="#ffb703", font=("Consolas", 11, "bold"))
        self.consola.tag_config("victoria", foreground="#4ade80", font=("Consolas", 12, "bold"))
        self.consola.tag_config("error", foreground="#f72585", font=("Consolas", 10, "bold"))
        self.consola.tag_config("normal", foreground="#e2e8f0")
        self.consola.see(tk.END)
        self.consola.config(state="disabled")

    def pedir_inicializacion(self):
        self.agregar_texto("=== CONFIGURACIÓN DE LA PARTIDA ===")
        nivel_str = simpledialog.askstring("Nivel", "Elige nivel:\n1. Fácil (1-50)\n2. Medio (1-100)\n3. Difícil (1-1000)", parent=self.raiz)
        
        try:
            nivel = int(nivel_str)
        except (ValueError, TypeError):
            nivel = 2 
            
        self.limite_superior = game_logic.seleccionar_limite(nivel)
        self.numero_secreto = game_logic.generar_numero(self.limite_superior)
        
        self.agregar_texto(f"Rango configurado: 1 a {self.limite_superior}")
        self.agregar_texto("Esperando que el Jugador 2 se conecte por red...")
        
        threading.Thread(target=self.servidor_red, daemon=True).start()

    def servidor_red(self):
        PUERTO = 65432
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind(('0.0.0.0', PUERTO))
        servidor.listen(1)
        self.conexion, direccion = servidor.accept()
        self.agregar_texto(f"[OK] Jugador 2 conectado desde: {direccion}")
        
        self.conexion.sendall(str(self.limite_superior).encode('utf-8'))
        self.activar_mi_turno()
        
        while True:
            try:
                datos = self.conexion.recv(1024).decode('utf-8')
                if not datos: break
                
                intento_j2 = int(datos)
                self.agregar_texto(f"Jugador 2 intentó con: {intento_j2}")
                
                res_j2 = game_logic.verificar_numero(intento_j2, self.numero_secreto)
                
                if res_j2 == "correcto":  
                    self.agregar_texto("[PERDISTE] El Jugador 2 adivinó el número.")
                    self.conexion.sendall("GANASTE:¡Felicidades! Adivinaste el número secreto.".encode('utf-8'))
                    break
                elif res_j2 == "mayor":
                    self.agregar_texto("El número secreto es mayor que lo que dijo el Jugador 2.")
                    self.conexion.sendall("El número secreto es mayor. ¡Tu turno!".encode('utf-8'))
                else:
                    self.agregar_texto("El número secreto es menor que lo que dijo el Jugador 2.")
                    self.conexion.sendall("El número secreto es menor. ¡Tu turno!".encode('utf-8'))
                
                self.activar_mi_turno()
            except:
                break
        self.desactivar_controles()

    def activar_mi_turno(self):
        self.mi_turno = True
        self.agregar_texto("--- ¡ES TU TURNO! ---")
        self.entrada_intento.config(state="normal")
        self.btn_enviar.config(state="normal")
        self.entrada_intento.focus()

    def desactivar_controles(self):
        self.entrada_intento.config(state="disabled")
        self.btn_enviar.config(state="disabled")

    def enviar_intento_j1(self):
        if not self.mi_turno: return
        entrada = self.entrada_intento.get().strip()
        self.entrada_intento.delete(0, tk.END)
        
        try:
            intento = int(entrada)
            self.agregar_texto(f"Tu intento: {intento}")
            
            res = game_logic.verificar_numero(intento, self.numero_secreto)
            
            if res == "correcto":  
                self.agregar_texto("[VICTORIA] ¡Ganaste la partida!")
                self.conexion.sendall("PERDISTE:El Jugador 1 adivinó el número secreto.".encode('utf-8'))
                self.desactivar_controles()
            else:
                pista = "MAYOR" if res == "mayor" else "MENOR"
                self.agregar_texto(f"El número secreto es {pista}.")
                self.conexion.sendall(f"TURNO:El Jugador 1 falló. Dijo {intento} y es {pista}.".encode('utf-8'))
                self.mi_turno = False
                self.desactivar_controles()
                self.agregar_texto("Esperando el turno del Jugador 2...")
        except ValueError:
            self.agregar_texto("[ERROR] Ingresa solo números enteros.")

app = VentanaServidor()
app.raiz.after(100, app.pedir_inicializacion)
app.raiz.mainloop()
