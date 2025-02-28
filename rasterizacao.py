import pygame
from zbuffer import ZBuffer  # Importar a classe ZBuffer
from phong import calcular_phong  # Importar a função calcular_phong

def rasterizar_poligono(tela, pontos, cor, z_buffer):
    """
    Rasteriza um polígono (triângulo) na tela, aplicando o z-buffer.
    """
    # Ordenar pontos pelo eixo Y (necessário para o algoritmo scan-line)
    pontos = sorted(pontos, key=lambda p: p[1])

    # Obter as coordenadas mínimas e máximas do polígono
    y_min = int(pontos[0][1])
    y_max = int(pontos[-1][1])

    # Criar uma lista de arestas ativas
    arestas = []
    for i in range(len(pontos)):
        x1, y1 = pontos[i]
        x2, y2 = pontos[(i + 1) % len(pontos)]
        if y1 != y2:
            if y1 < y2:
                arestas.append({'x': x1, 'y_min': y1, 'y_max': y2, 'x_inc': (x2 - x1) / (y2 - y1)})
            else:
                arestas.append({'x': x2, 'y_min': y2, 'y_max': y1, 'x_inc': (x1 - x2) / (y1 - y2)})

    # Ordenar arestas por y_min
    arestas.sort(key=lambda a: a['y_min'])

    # Inicializar a lista de arestas ativas
    arestas_ativas = []
    y_atual = y_min

    while y_atual <= y_max:
        # Adicionar arestas à lista de arestas ativas
        while arestas and arestas[0]['y_min'] <= y_atual:
            arestas_ativas.append(arestas.pop(0))

        # Remover arestas que não estão mais ativas
        arestas_ativas = [a for a in arestas_ativas if a['y_max'] > y_atual]

        # Ordenar arestas ativas por x
        arestas_ativas.sort(key=lambda a: a['x'])

        # Desenhar linhas horizontais entre pares de arestas
        for i in range(0, len(arestas_ativas), 2):
            x_inicio = int(arestas_ativas[i]['x'])
            x_fim = int(arestas_ativas[i + 1]['x'])
            for x in range(x_inicio, x_fim + 1):
                # Verificar z-buffer antes de desenhar o pixel
                if z_buffer.atualizar(x, y_atual, 0):  # Profundidade fixa para teste
                    pygame.draw.circle(tela, cor, (x, y_atual), 1)

        # Atualizar y_atual e as posições x das arestas ativas
        y_atual += 1
        for a in arestas_ativas:
            a['x'] += a['x_inc']

def rasterizar_cena(tela, objeto, camera, luz):
    """
    Renderiza toda a cena, aplicando iluminação e z-buffer.
    """
    z_buffer = ZBuffer(tela.get_width(), tela.get_height())  # Resetar z-buffer a cada frame
    for tri in objeto.triangulos:
        # Verificar se os índices do triângulo estão dentro do intervalo válido
        if all(0 <= idx < len(objeto.vertices) for idx in tri):
            # Projetar vértices do triângulo na tela
            pontos_projetados = [camera.projetar_perspectiva(objeto.vertices[i]) for i in tri]

            # Calcular a normal do triângulo
            normal = objeto.calcular_normal(tri)

            # Calcular a cor do triângulo usando o modelo de Phong
            cor = calcular_phong(normal, luz, camera, objeto.material)  # Passar objeto.material

            # Rasterizar o triângulo
            rasterizar_poligono(tela, pontos_projetados, cor, z_buffer)
        else:
            print(f"Erro: Índices inválidos no triângulo {tri}")