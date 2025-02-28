class ZBuffer:
    def __init__(self, largura, altura):
        """
        Inicializa o z-buffer com uma matriz de profundidade.
        """
        self.buffer = [[float('inf') for _ in range(altura)] for _ in range(largura)]

    def atualizar(self, x, y, z):
        """
        Atualiza o z-buffer se a profundidade do pixel for menor que o valor atual.
        """
        if z < self.buffer[x][y]:
            self.buffer[x][y] = z
            return True
        return False