# Renderizador de Múltiplas Malhas BYU

Este é um projeto simples em Python para carregar, normalizar e renderizar múltiplas malhas 3D a partir de arquivos no formato BYU. O projeto utiliza a biblioteca `pygame` para a visualização das malhas em uma interface gráfica.

## Funcionalidades

- **Carregamento de malhas 3D:** Suporte para arquivos BYU com várias malhas.
- **Normalização automática:** Ajusta as malhas para caberem na janela, com centralização e escala adequadas.
- **Renderização 2D:** Exibe os triângulos das malhas em uma tela gráfica.

## Tecnologias Utilizadas

- Python 3.8+
- Biblioteca [pygame](https://www.pygame.org/)

## Requisitos de Instalação

Antes de executar o projeto, certifique-se de que você possui o Python 3.8 ou superior instalado em seu sistema. Também é necessário instalar a biblioteca `pygame`.

### Instalação do pygame

Execute o seguinte comando para instalar o `pygame`:

```bash
pip install pygame
```

## Como Executar o Projeto

1. Clone este repositório em sua máquina local:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

2. Navegue até o diretório do projeto:

```bash
cd seu-repositorio
```

3. Certifique-se de que o arquivo `.byu` que você deseja renderizar esteja localizado no diretório `objetos`. Por exemplo:

```
./objetos/maca2.byu
```

4. Execute o script principal:

```bash
python main.py
```

5. Uma janela será aberta exibindo as malhas carregadas.

## Formato do Arquivo BYU

O projeto suporta arquivos BYU que seguem este formato:

- Primeira linha: quantidade de vértices e triângulos.
- Seguinte(s) linha(s): coordenadas dos vértices (x, y, z).
- Linhas restantes: triângulos representados pelos índices dos vértices (1-indexado).

Exemplo de um arquivo BYU:

```
4 2
0.0 0.0 0.0
1.0 0.0 0.0
0.0 1.0 0.0
1.0 1.0 0.0
1 2 3
2 3 4
```



