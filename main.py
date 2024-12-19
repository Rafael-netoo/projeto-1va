import pygame  # Biblioteca para criação de jogos e gráficos 2D

# Configurações da janela
LARGURA_JANELA = 800  # Largura da janela em pixels
ALTURA_JANELA = 600  # Altura da janela em pixels

# Função para carregar múltiplas malhas de um arquivo
def carregar_multiplas_malhas(arquivo):
    """
    Lê um arquivo e carrega múltiplas malhas 3D. Cada malha é composta por vértices e triângulos.
    :param arquivo: Caminho do arquivo contendo os dados das malhas.
    :return: Lista de malhas, onde cada malha é uma tupla (vértices, triângulos).
    """
    with open(arquivo, 'r') as f:
        # Lê todas as linhas, removendo espaços em branco e ignorando linhas vazias
        linhas = [linha.strip() for linha in f if linha.strip()]

    malhas = []  # Lista para armazenar todas as malhas carregadas
    i = 0  # Índice para percorrer as linhas do arquivo

    while i < len(linhas):
        # Lê o número de vértices e triângulos da malha atual
        num_vertices, _ = map(int, linhas[i].split())
        i += 1  # Avança para a próxima linha

        # Lê os vértices
        vertices = []
        for _ in range(num_vertices):
            x, y, z = map(float, linhas[i].split())  # Coordenadas do vértice
            vertices.append((x, y, z))
            i += 1

        # Lê os triângulos
        triangulos = []
        while i < len(linhas) and len(linhas[i].split()) == 3:  # Triângulos têm 3 índices
            indices = list(map(int, linhas[i].split()))
            triangulos.append((indices[0] - 1, indices[1] - 1, indices[2] - 1))  # Subtração para ajustar índices
            i += 1

        # Adiciona a malha atual à lista
        malhas.append((vertices, triangulos))

    return malhas

# Função para normalizar os vértices de uma malha
def normalizar_vertices(vertices, largura, altura):
    """
    Ajusta os vértices para que a malha caiba na janela, centralizada e escalada adequadamente.
    :param vertices: Lista de vértices (x, y, z).
    :param largura: Largura da janela.
    :param altura: Altura da janela.
    :return: Lista de vértices normalizados.
    """
    # Determina os limites dos vértices (mínimo e máximo em cada eixo)
    min_x = min(v[0] for v in vertices)
    max_x = max(v[0] for v in vertices)
    min_y = min(v[1] for v in vertices)
    max_y = max(v[1] for v in vertices)

    # Calcula a escala e deslocamento para centralizar e redimensionar
    largura_objeto = max_x - min_x
    altura_objeto = max_y - min_y
    escala = min(LARGURA_JANELA / largura_objeto, ALTURA_JANELA / altura_objeto) * 0.9  # Margem de 10%

    offset_x = (largura / 2) - ((max_x + min_x) / 2) * escala
    offset_y = (altura / 2) - ((max_y + min_y) / 2) * escala

    # Aplica a transformação aos vértices
    vertices_normalizados = []
    for x, y, z in vertices:
        nx = x * escala + offset_x
        ny = y * escala + offset_y
        vertices_normalizados.append((nx, ny, z))

    return vertices_normalizados

# Função principal
def main():
    """
    Função principal do programa. Configura a janela, carrega e renderiza malhas.
    """
    pygame.init()  # Inicializa os módulos do Pygame

    # Configura a janela de exibição
    tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
    pygame.display.set_caption("Renderização de Múltiplas Malhas BYU")

    # Carrega todas as malhas do arquivo especificado
    malhas = carregar_multiplas_malhas('./objetos/maca2.byu')

    # Normaliza os vértices de cada malha para caber na janela
    malhas_normalizadas = []
    for vertices, triangulos in malhas:
        vertices_normalizados = normalizar_vertices(vertices, LARGURA_JANELA, ALTURA_JANELA)
        malhas_normalizadas.append((vertices_normalizados, triangulos))

    # Loop principal do programa
    executando = True
    while executando:
        for evento in pygame.event.get():  # Lida com eventos
            if evento.type == pygame.QUIT:  # Fecha o programa se o botão de sair for pressionado
                executando = False

        # Preenche o fundo da janela com preto
        tela.fill((0, 0, 0))

        # Renderiza todas as malhas na tela
        for vertices, triangulos in malhas_normalizadas:
            for tri in triangulos:
                # Verifica se todos os índices do triângulo são válidos
                if all(0 <= i < len(vertices) for i in tri):
                    pontos = [(vertices[i][0], vertices[i][1]) for i in tri]  # Obtém os pontos 2D do triângulo
                    pygame.draw.polygon(tela, (255, 255, 255), pontos)  # Desenha o triângulo na tela
                else:
                    print(f"Triângulo inválido: {tri}, Vértices disponíveis: {len(vertices)}")

        # Atualiza a exibição
        pygame.display.flip()

    pygame.quit()  # Encerra o Pygame

# Executa o programa se este arquivo for executado diretamente
if __name__ == "__main__":
    main()
