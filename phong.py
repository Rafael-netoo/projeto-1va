def calcular_phong(normal, luz, camera, material):
    """
    Calcula a cor de um ponto usando o modelo de iluminação de Phong.
    """
    # Vetor da luz (L)
    L = normalizar((luz.Pi[0] - camera.posicao[0], luz.Pi[1] - camera.posicao[1], luz.Pi[2] - camera.posicao[2]))
    
    # Vetor normal (N)
    N = normalizar(normal)
    
    # Vetor de visão (V)
    V = normalizar((camera.posicao[0], camera.posicao[1], camera.posicao[2]))
    
    # Vetor de reflexão (R)
    R = refletir(L, N)

    # Componente ambiente
    ambiente = [luz.Iamb[i] * material['Ka'] for i in range(3)]
    
    # Componente difusa
    difusa = [luz.Ii[i] * material['Kd'][i] * max(0, N[0] * L[0] + N[1] * L[1] + N[2] * L[2]) for i in range(3)]
    
    # Componente especular
    especular = [luz.Ii[i] * material['Ks'] * (max(0, R[0] * V[0] + R[1] * V[1] + R[2] * V[2]) ** material['eta']) for i in range(3)]

    # Cor final (ambiente + difusa + especular)
    cor = [int(ambiente[i] + difusa[i] + especular[i]) for i in range(3)]
    return tuple(cor)

def normalizar(vetor):
    """
    Normaliza um vetor 3D.
    """
    magnitude = (vetor[0]**2 + vetor[1]**2 + vetor[2]**2) ** 0.5
    if magnitude == 0:
        return (0, 0, 0)  # Evita divisão por zero
    return (vetor[0] / magnitude, vetor[1] / magnitude, vetor[2] / magnitude)

def refletir(L, N):
    """
    Calcula o vetor de reflexão da luz (R) dado o vetor de luz (L) e a normal (N).
    """
    dot = L[0] * N[0] + L[1] * N[1] + L[2] * N[2]
    return (
        2 * dot * N[0] - L[0],
        2 * dot * N[1] - L[1],
        2 * dot * N[2] - L[2]
    )