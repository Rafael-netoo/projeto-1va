class Camera:
    def __init__(self, parametros, largura_janela, altura_janela):
        """
        Inicializa a câmera com os parâmetros fornecidos e as dimensões da janela.
        """
        self.posicao = parametros['Ponto C']  # Posição da câmera no espaço 3D
        self.N = parametros['Vetor N']       # Vetor normal (direção da câmera)
        self.V = parametros['Vetor V']       # Vetor de visão (orientação da câmera)
        self.d = float(parametros['d'])      # Distância de projeção
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela

    def projetar_perspectiva(self, ponto):
        """
        Aplica projeção em perspectiva em um ponto 3D, considerando a posição da câmera.
        """
        # Transladar o ponto para o sistema de coordenadas da câmera
        x = ponto[0] - self.posicao[0]
        y = ponto[1] - self.posicao[1]
        z = ponto[2] - self.posicao[2]

        # Aplicar projeção em perspectiva
        if z + self.d <= 0:
            return (x, y)  # Evita divisão por zero ou valores negativos
        fator_projecao = self.d / (z + self.d)
        x_proj = x * fator_projecao
        y_proj = y * fator_projecao

        # Centralizar na tela
        return (int(x_proj + self.largura_janela / 2), int(y_proj + self.altura_janela / 2))