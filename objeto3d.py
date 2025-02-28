class Objeto3D:
    def __init__(self, vertices, triangulos, material):
        """
        Inicializa um objeto 3D com vértices, triângulos e material.
        """
        self.vertices = vertices
        self.triangulos = triangulos
        self.material = material  # Armazenar o material
        self.normalizar()  # Normalizar os vértices para centralizar o objeto

    def normalizar(self):
        """
        Normaliza os vértices para centralizar o objeto na origem.
        """
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

        # Centraliza os vértices na origem
        self.vertices = [(x - centro_x, y - centro_y, z - centro_z) for x, y, z in self.vertices]

    def calcular_normal(self, tri):
        """
        Calcula a normal de um triângulo.
        """
        v0, v1, v2 = [self.vertices[i] for i in tri]
        u = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])
        v = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])
        normal = (
            u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0]
        )
        return normal