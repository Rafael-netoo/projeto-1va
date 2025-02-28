class Luz:
    def __init__(self, parametros):
        """
        Inicializa a luz com os parâmetros fornecidos.
        """
        self.Iamb = parametros.get('Iamb', [100, 100, 100])  # Intensidade da luz ambiente
        self.Ii = parametros.get('Ii', [127, 213, 254])      # Intensidade da luz pontual
        self.Pi = parametros.get('Pi', [60, 5, -10])         # Posição da luz pontual
        self.Ka = parametros.get('Ka', 0.2)                  # Coeficiente de reflexão ambiente
        self.Kd = parametros.get('Kd', [0.5, 0.3, 0.2])      # Coeficiente de reflexão difusa
        self.Ks = parametros.get('Ks', 0.5)                  # Coeficiente de reflexão especular
        self.eta = parametros.get('η', 1)                    # Expoente de brilho (eta)