import os
import wave
import struct
import math
import random

SR = 22050 
DIRECTORIO = os.path.join(os.path.dirname(__file__), "assets", "sonidos")


def envolvente(i, n, ataque=0.01):
    
    t = i / n
    a = min(1.0, t / ataque) if ataque > 0 else 1.0
    caida = 1.0 - t
    return a * caida


def tono(freq, dur, vol=0.5):
    n = int(SR * dur)
    return [vol * envolvente(i, n) * math.sin(2 * math.pi * freq * i / SR)
            for i in range(n)]


def ruido(dur, vol=0.5):
    n = int(SR * dur)
    return [vol * envolvente(i, n) * (random.random() * 2 - 1) for i in range(n)]


def silencio(dur):
    return [0.0] * int(SR * dur)


def mezclar(*pistas):
   
    largo = max(len(p) for p in pistas)
    salida = [0.0] * largo
    for p in pistas:
        for i, m in enumerate(p):
            salida[i] += m
    return salida


def guardar(nombre, muestras):
    ruta = os.path.join(DIRECTORIO, nombre)
    archivo = wave.open(ruta, "w")
    archivo.setnchannels(1)
    archivo.setsampwidth(2)
    archivo.setframerate(SR)
    datos = bytearray()
    for m in muestras:
        valor = max(-1.0, min(1.0, m))
        datos += struct.pack("<h", int(valor * 30000))
    archivo.writeframes(bytes(datos))
    archivo.close()
    print("creado:", nombre)


def main():
    os.makedirs(DIRECTORIO, exist_ok=True)

    guardar("clic.wav", tono(880, 0.06, 0.4))

    guardar("carta.wav", mezclar(tono(220, 0.10, 0.35), ruido(0.08, 0.15)))

    guardar("captura.wav", tono(660, 0.08, 0.4) + tono(880, 0.10, 0.4))

    guardar("caida.wav", tono(523, 0.08, 0.4) + tono(659, 0.08, 0.4) + tono(784, 0.12, 0.45))

    guardar("limpia.wav",
            tono(659, 0.06, 0.4) + tono(784, 0.06, 0.4) +
            tono(988, 0.06, 0.4) + tono(1318, 0.12, 0.45))

    guardar("ganar.wav",
            tono(523, 0.15, 0.45) + tono(659, 0.15, 0.45) +
            tono(784, 0.15, 0.45) + tono(1046, 0.30, 0.5))

    repartir = []
    for _ in range(6):
        repartir += ruido(0.03, 0.25) + silencio(0.02)
    guardar("repartir.wav", repartir)

    print("Listo. Sonidos en:", DIRECTORIO)


if __name__ == "__main__":
    main()
