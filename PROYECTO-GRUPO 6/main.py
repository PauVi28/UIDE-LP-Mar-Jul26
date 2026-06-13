from tkinter import *
from random import choice
from juego.logica import ganador

ventana = Tk()
ventana.title("Piedra Papel o Tijera")
ventana.geometry("1200x800")
ventana.resizable(False, False)

# ===== IMÁGENES =====
img_fondo = PhotoImage(file="Imagenes/fondo.png")

img_piedra = PhotoImage(file="Imagenes/piedracn.png")
img_piedra = img_piedra.subsample(4, 4)

img_papel = PhotoImage(file="Imagenes/papel patricio.png")
img_papel = img_papel.subsample(4, 4)

img_tijera = PhotoImage(file="Imagenes/tijeras patricio.png")
img_tijera = img_tijera.subsample(4, 4)

# ===== FONDO =====
fondo = Label(ventana, image=img_fondo)
fondo.place(x=0, y=0, relwidth=1, relheight=1)
fondo.lower()  # Envía el fondo detrás de todo


def limpiar():
    for widget in ventana.winfo_children():
        if widget != fondo:
            widget.destroy()


def volver_menu():
    limpiar()
    menu_principal()


def jugar(jugada):
    opciones = ["piedra", "papel", "tijera"]
    computadora = choice(opciones)

    resultado.config(
        text=f"Tu elección: {jugada}\nComputadora: {computadora}\n\n{ganador(jugada, computadora)}"
    )


def modo_local():
    global resultado

    limpiar()

    Label(
        ventana,
        text="MODO LOCAL",
        font=("Arial", 24, "bold")
    ).pack(pady=20)

    marco = Frame(ventana)
    marco.pack(pady=20)

    Button(
        marco,
        image=img_piedra,
        command=lambda: jugar("piedra")
    ).grid(row=0, column=0, padx=20)

    Button(
        marco,
        image=img_papel,
        command=lambda: jugar("papel")
    ).grid(row=0, column=1, padx=20)

    Button(
        marco,
        image=img_tijera,
        command=lambda: jugar("tijera")
    ).grid(row=0, column=2, padx=20)

    Label(marco, text="Piedra").grid(row=1, column=0)
    Label(marco, text="Papel").grid(row=1, column=1)
    Label(marco, text="Tijera").grid(row=1, column=2)

    resultado = Label(
        ventana,
        text="Selecciona una opción",
        font=("Arial", 16)
    )
    resultado.pack(pady=20)

    Button(
        ventana,
        text="Volver al menú",
        width=20,
        command=volver_menu
    ).pack(pady=5)

    Button(
        ventana,
        text="Salir",
        width=20,
        command=ventana.destroy
    ).pack(pady=5)


def modo_multijugador():
    limpiar()

    Label(
        ventana,
        text="MODO MULTIJUGADOR",
        font=("Arial", 24, "bold")
    ).pack(pady=20)

    Label(
        ventana,
        text="Usar servidor.py y cliente.py para la conexión LAN",
        font=("Arial", 14)
    ).pack(pady=20)

    Button(
        ventana,
        text="Volver al menú",
        width=20,
        command=volver_menu
    ).pack(pady=5)

    Button(
        ventana,
        text="Salir",
        width=20,
        command=ventana.destroy
    ).pack(pady=5)


def menu_principal():
    Label(
        ventana,
        text="PIEDRA PAPEL O TIJERA",
        font=("Arial", 28, "bold")
    ).pack(pady=20)

    Button(
        ventana,
        text="Modo Local",
        width=25,
        height=2,
        command=modo_local
    ).pack(pady=10)

    Button(
        ventana,
        text="Modo Multijugador",
        width=25,
        height=2,
        command=modo_multijugador
    ).pack(pady=10)

    Button(
        ventana,
        text="Salir",
        width=25,
        height=2,
        command=ventana.destroy
    ).pack(pady=10)


menu_principal()

ventana.mainloop()