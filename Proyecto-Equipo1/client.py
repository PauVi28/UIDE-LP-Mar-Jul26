import tkinter as tk
from tkinter import simpledialog, scrolledtext
import socket
import threading

class VentanaCliente:
    def __init__(self):
        self.raiz = tk.Tk()
        self.raiz.title("Cliente - Jugador 2")
        self.raiz.geometry("550x500")
        self.raiz.config(bg="#121214")
        self.raiz.resizable(False, False)
        
        self.titulo = tk.Label(self.raiz, text="CLIENTE: JUGADOR 2", font=("Segoe UI", 16, "bold"), bg="#121214", fg="#ffb703")
        self.titulo.pack(pady=(20, 10))
        
        self.consola = scrolledtext.ScrolledText(self.raiz, width=58, height=18, font=("Consolas", 10), bg="#1e1e24", fg="#f1f5f9", bd=0, highlightthickness=1, highlightbackground="#2a2a35", highlightcolor="#ffb703")
        self.consola.pack(pady=10, padx=15)
        self.consola.config(state="disabled")
        
        self.marco_entrada = tk.Frame(self.raiz, bg="#121214")
        self.marco_entrada.pack(pady=10)
        
        self.entrada_intento = tk.Entry(self.marco_entrada, font=("Segoe UI", 12), width=15, bg="#1e1e24", fg="#ffffff", insertbackground="white", state="disabled")
        self.entrada_intento.pack(side=tk.LEFT, padx=5)
        
        self.btn_enviar = tk.Button(self.marco_entrada, text="Enviar Intento", font=("Segoe UI", 10, "bold"), bg="#ffb703", fg="#121214", state="disabled", command=self.enviar_intento_j2)
        self.btn_enviar.pack(side=tk.LEFT, padx=5)
        
        self.cliente = None
        self.mi_turno = False
        self.entrada_intento.bind("<Return>", lambda event: self.enviar_intento_j2())

    def agregar_texto(self, texto):
        self.consola.config(state="normal")
        if "--- " in texto:
            self.consola.insert(tk.END, f"\n{texto}\n", "titulo")
        elif "VICTORIA" in texto or "GANASTE" in texto:
            self.consola.insert(tk.END, f"\n{texto}\n", "victoria")
        elif "PERDISTE" in texto or "[ERROR]" in texto:
            self.consola.insert(tk.END, f"\n{texto}\n", "error")
        else:
            self.consola.insert(tk.END, f"  -> {texto}\n", "normal")
            
        self.consola.tag_config("titulo", foreground="#4ade80", font=("Consolas", 11, "bold"))
        self.consola.tag_config("victoria", foreground="#4ade80", font=("Consolas", 12, "bold"))
        self.consola.tag_config("error", foreground="#f72585", font=("Consolas", 10, "bold"))
        self.consola.tag_config("normal", foreground="#e2e8f0")
        self.consola.see(tk.END)
        self.consola.config(state="disabled")

    def conectar_servidor(self):
        ip_j1 = simpledialog.askstring("Conexión", "Introduce la IP del Jugador 1 (ej: 127.0.0.1):", parent=self.raiz)
        if not ip_j1: ip_j1 = "127.0.0.1"
        
        self.agregar_texto(f"Intentando conectar a {ip_j1}...")
        threading.Thread(target=self.cliente_red, args=(ip_j1,), daemon=True).start()

    def cliente_red(self, ip):
        PUERTO = 65432
        try:
            self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cliente.connect((ip, PUERTO))
            self.agregar_texto("[OK] ¡Conectado con éxito al Jugador 1!")
            
            limite = self.cliente.recv(1024).decode('utf-8')
            self.agregar_texto(f"Rango de la partida: 1 a {limite}")
            self.agregar_texto("Espera a que el Jugador 1 juegue...")
            
            while True:
                msg = self.cliente.recv(1024).decode('utf-8')
                if not msg: break
                
                if "PERDISTE:" in msg:
                    self.agregar_texto(f"[FIN] {msg.split(':')[1]}")
                    break
                elif "GANASTE:" in msg:
                    self.agregar_texto(f"[VICTORIA] {msg.split(':')[1]}")
                    break
                
                if "TURNO:" in msg:
                    self.agregar_texto(msg.split(':')[1])
                else:
                    self.agregar_texto(msg)
                    
                self.activar_mi_turno()
        except:
            self.agregar_texto("[ERROR] Error de conexión.")
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

    def enviar_intento_j2(self):
        if not self.mi_turno: return
        entrada = self.entrada_intento.get().strip()
        self.entrada_intento.delete(0, tk.END)
        
        try:
            intento = int(entrada)
            self.agregar_texto(f"Tu intento: {intento}")
            self.cliente.sendall(str(intento).encode('utf-8'))
            self.mi_turno = False
            self.desactivar_controles()
            self.agregar_texto("Esperando respuesta e intento del Jugador 1...")
        except ValueError:
            self.agregar_texto("[ERROR] Ingresa solo números enteros.")

app = VentanaCliente()
app.raiz.after(100, app.conectar_servidor)
app.raiz.mainloop()
