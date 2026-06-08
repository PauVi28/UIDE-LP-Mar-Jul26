import random

def jugar_cpu(mano_cpu):

    if len(mano_cpu) > 0:

        indice = random.randint(0, len(mano_cpu) - 1)

        return mano_cpu.pop(indice)

    return None
