from objeto3d import Objeto3D

def carregar_parametros(arquivo):
    """
    Carrega os parâmetros da câmera e iluminação de um arquivo de texto.
    """
    parametros = {}
    with open(arquivo, 'r') as f:
        for linha in f:
            if '=' in linha:
                chave, valor = linha.split('=')
                valor = valor.strip()
                # Se o valor contém apenas um número, converta para float
                if ' ' not in valor:
                    parametros[chave.strip()] = float(valor)
                else:
                    # Caso contrário, converta para lista de floats
                    parametros[chave.strip()] = list(map(float, valor.split()))
    return parametros

def carregar_objeto(arquivo, material):
    """
    Carrega um objeto 3D a partir de um arquivo no formato BYU.
    """
    vertices = []
    triangulos = []
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
        num_vertices, num_triangulos = map(int, linhas[0].split())
        
        # Carregar vértices
        for i in range(1, num_vertices + 1):
            vertices.append(tuple(map(float, linhas[i].split())))
        
        # Carregar triângulos
        for i in range(num_vertices + 1, num_vertices + num_triangulos + 1):
            indices = list(map(int, linhas[i].split()))
            # Verificar se os índices estão dentro do intervalo válido
            if all(1 <= idx <= num_vertices for idx in indices):
                # Ajustar índices para base 0 (subtrair 1)
                triangulos.append((indices[0] - 1, indices[1] - 1, indices[2] - 1))
            else:
                print(f"Erro: Índices inválidos na linha {i}: {linhas[i].strip()}")
                return None
    
    # Retornar um objeto da classe Objeto3D com o material
    return Objeto3D(vertices, triangulos, material)