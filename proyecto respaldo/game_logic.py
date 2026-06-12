def determinar_ganador(jugada_1, jugada_2):
    """
    Determina el resultado desde la perspectiva de la jugada_1.
    Retorna: 'ganas', 'pierdes' o 'empate'
    """
    j1 = jugada_1.lower().strip()
    j2 = jugada_2.lower().strip()

    opciones_validas = ['piedra', 'papel', 'tijera']
    if j1 not in opciones_validas or j2 not in opciones_validas:
        return "error"

    if j1 == j2:
        return "empate"

    reglas = {
        'piedra': 'tijera',
        'papel': 'piedra',
        'tijera': 'papel'
    }

    if reglas[j1] == j2:
        return "ganas"
    else:
        return "pierdes"
