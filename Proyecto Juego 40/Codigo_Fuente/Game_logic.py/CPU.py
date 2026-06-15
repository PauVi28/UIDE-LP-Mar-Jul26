from logica import reglas40

def jugar_cpu(juego):

    mano = juego.mano_cpu
    if not mano:
        return 0
        
    mejor_indice = None
    mejor_cantidad = 0
    for i, carta in enumerate(mano):
        capturadas = reglas40.buscar_captura(juego.mesa, carta)
        if len(capturadas) > mejor_cantidad:
            mejor_cantidad = len(capturadas)
            mejor_indice = i

    if mejor_indice is not None:
        return mejor_indice
        
    return 0
