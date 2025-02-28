import pygame
from load import carregar_parametros, carregar_objeto
from camera import Camera
from luz import Luz
from rasterizacao import rasterizar_cena

# Configurações da janela
LARGURA_JANELA = 800
ALTURA_JANELA = 600

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
    pygame.display.set_caption("Renderização 3D com Phong e Z-Buffer")

    # Carregar parâmetros e objetos
    parametros = carregar_parametros('parametros.txt')
    camera = Camera(parametros, LARGURA_JANELA, ALTURA_JANELA)  # Passar dimensões da janela
    luz = Luz(parametros)

    # Definir material do objeto
    material = {
        'Ka': parametros.get('Ka', 0.2),
        'Kd': parametros.get('Kd', [0.5, 0.3, 0.2]),
        'Ks': parametros.get('Ks', 0.5),
        'Od': parametros.get('Od', [0.7, 0.5, 0.8]),
        'eta': parametros.get('η', 1)
    }

    # Carregar o objeto com o material
    objeto = carregar_objeto('objetos/maca2.byu', material)

    executando = True
    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        # Controles da câmera
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w]:  # Mover câmera para frente
            camera.posicao[2] += 10
        if teclas[pygame.K_s]:  # Mover câmera para trás
            camera.posicao[2] -= 10
        if teclas[pygame.K_a]:  # Mover câmera para a esquerda
            camera.posicao[0] -= 10
        if teclas[pygame.K_d]:  # Mover câmera para a direita
            camera.posicao[0] += 10
        if teclas[pygame.K_q]:  # Mover câmera para cima
            camera.posicao[1] -= 10
        if teclas[pygame.K_e]:  # Mover câmera para baixo
            camera.posicao[1] += 10

        # Recarregar parâmetros ao pressionar 'R'
        if teclas[pygame.K_r]:
            parametros = carregar_parametros('parametros.txt')
            camera = Camera(parametros, LARGURA_JANELA, ALTURA_JANELA)  # Atualizar câmera
            luz = Luz(parametros)

        # Renderizar cena
        tela.fill((0, 0, 0))  # Limpar tela
        rasterizar_cena(tela, objeto, camera, luz)
        pygame.display.flip()  # Atualizar tela

    pygame.quit()

if __name__ == "__main__":
    main()