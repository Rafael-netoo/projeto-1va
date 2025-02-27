import pygame
import os
import math

# Configurações da janela
LARGURA_JANELA = 800
ALTURA_JANELA = 600

class Camera:
    def __init__(self):
        self.posicao = [0, 0, -1000]  # Posição da câmera (x, y, z)
        self.rotacao = [0, 0, 0]      # Rotação da câmera (pitch, yaw, roll)
        self.distancia_projecao = 1000  # Distância da câmera para a projeção
        self.velocidade_movimento = 10
        self.velocidade_rotacao = 0.01
        self.zoom_velocidade = 50

    def projetar_perspectiva(self, x, y, z):
        """ Aplica projeção em perspectiva nos vértices """
        # Translação do vértice em relação à câmera
        x -= self.posicao[0]
        y -= self.posicao[1]
        z -= self.posicao[2]

        # Rotação do vértice (pitch, yaw, roll)
        x, y, z = self.rotacionar_ponto(x, y, z)

        # Projeção em perspectiva
        if z + self.distancia_projecao <= 0:
            return (x, y)  # Evita divisão por zero ou valores negativos
        fator_projecao = self.distancia_projecao / (z + self.distancia_projecao)
        x_proj = (x - LARGURA_JANELA / 2) * fator_projecao + (LARGURA_JANELA / 2)
        y_proj = (y - ALTURA_JANELA / 2) * fator_projecao + (ALTURA_JANELA / 2)
        return (int(x_proj), int(y_proj))

    def rotacionar_ponto(self, x, y, z):
        """ Rotaciona um ponto ao redor da câmera """
        # Rotação em Y (yaw)
        cos_y = math.cos(self.rotacao[1])
        sin_y = math.sin(self.rotacao[1])
        x, z = x * cos_y - z * sin_y, x * sin_y + z * cos_y

        # Rotação em X (pitch)
        cos_x = math.cos(self.rotacao[0])
        sin_x = math.sin(self.rotacao[0])
        y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x

        return x, y, z

class Malha:
    def __init__(self, vertices, triangulos):
        self.vertices = vertices
        self.triangulos = triangulos
        self.normalizar()
    
    def normalizar(self):
        """ Normaliza os vértices para caber na tela e centraliza o objeto """
        if not self.vertices:
            return

        # Encontra os valores mínimos e máximos de cada eixo
        min_x = min(v[0] for v in self.vertices)
        max_x = max(v[0] for v in self.vertices)
        min_y = min(v[1] for v in self.vertices)
        max_y = max(v[1] for v in self.vertices)
        min_z = min(v[2] for v in self.vertices)
        max_z = max(v[2] for v in self.vertices)

        # Calcula o centro do objeto
        centro_x = (max_x + min_x) / 2
        centro_y = (max_y + min_y) / 2
        centro_z = (max_z + min_z) / 2

        # Calcula a escala para caber na tela
        largura_obj = max_x - min_x
        altura_obj = max_y - min_y
        escala = min(LARGURA_JANELA / largura_obj, ALTURA_JANELA / altura_obj) * 0.8

        # Centraliza e escala os vértices
        self.vertices = [
            (
                (x - centro_x) * escala,
                (y - centro_y) * escala,
                (z - centro_z) * escala
            )
            for x, y, z in self.vertices
        ]

    def desenhar_scanline(self, tela, camera, cor=(255, 255, 255)):
        """ Desenha os triângulos usando o algoritmo Scan-Line """
        for tri in self.triangulos:
            pontos = [camera.projetar_perspectiva(*self.vertices[i]) for i in tri]
            pygame.draw.polygon(tela, cor, pontos)

# Função para carregar malhas de um arquivo
def carregar_multiplas_malhas(arquivo):
    if not os.path.exists(arquivo):
        print(f"Erro: Arquivo '{arquivo}' não encontrado.")
        return []
    
    try:
        with open(arquivo, 'r') as f:
            linhas = [linha.strip() for linha in f if linha.strip()]
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return []

    malhas = []
    i = 0
    while i < len(linhas):
        try:
            num_vertices, num_triangulos = map(int, linhas[i].split())
            i += 1

            vertices = [tuple(map(float, linhas[i + j].split())) for j in range(num_vertices)]
            i += num_vertices

            triangulos = []
            for _ in range(num_triangulos):
                indices = list(map(int, linhas[i].split()))
                triangulos.append((indices[0] - 1, indices[1] - 1, indices[2] - 1))
                i += 1

            print(f"Malha carregada: {num_vertices} vértices, {num_triangulos} triângulos")
            malhas.append(Malha(vertices, triangulos))
        except ValueError as e:
            print(f"Erro ao processar arquivo na linha {i}: {linhas[i]}")
            print(f"Detalhes: {e}")
            break

    return malhas

# Função principal
def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
    pygame.display.set_caption("Renderização de Múltiplas Malhas BYU com Câmera")

    malhas = carregar_multiplas_malhas('./objetos/calice2.byu')
    camera = Camera()

    executando = True
    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        # Controles da câmera
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w]:  # Mover câmera para frente
            camera.posicao[2] += camera.velocidade_movimento
        if teclas[pygame.K_s]:  # Mover câmera para trás
            camera.posicao[2] -= camera.velocidade_movimento
        if teclas[pygame.K_a]:  # Mover câmera para a esquerda
            camera.posicao[0] -= camera.velocidade_movimento
        if teclas[pygame.K_d]:  # Mover câmera para a direita
            camera.posicao[0] += camera.velocidade_movimento
        if teclas[pygame.K_q]:  # Mover câmera para cima
            camera.posicao[1] -= camera.velocidade_movimento
        if teclas[pygame.K_e]:  # Mover câmera para baixo
            camera.posicao[1] += camera.velocidade_movimento
        if teclas[pygame.K_UP]:  # Rotacionar para cima (pitch)
            camera.rotacao[0] -= camera.velocidade_rotacao
        if teclas[pygame.K_DOWN]:  # Rotacionar para baixo (pitch)
            camera.rotacao[0] += camera.velocidade_rotacao
        if teclas[pygame.K_LEFT]:  # Rotacionar para a esquerda (yaw)
            camera.rotacao[1] -= camera.velocidade_rotacao
        if teclas[pygame.K_RIGHT]:  # Rotacionar para a direita (yaw)
            camera.rotacao[1] += camera.velocidade_rotacao
        if teclas[pygame.K_PAGEUP]:  # Zoom in
            camera.distancia_projecao -= camera.zoom_velocidade
        if teclas[pygame.K_PAGEDOWN]:  # Zoom out
            camera.distancia_projecao += camera.zoom_velocidade

        tela.fill((0, 0, 0))
        for malha in malhas:
            malha.desenhar_scanline(tela, camera)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()