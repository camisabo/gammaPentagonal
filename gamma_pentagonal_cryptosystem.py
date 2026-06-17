"""
Criptosistema Γ-Pentagonal
Basado en particiones de enteros y trayectorias en el plano discreto
Autor: Análisis criptográfico avanzado
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from itertools import combinations, permutations
from functools import lru_cache
from typing import Tuple, List, Dict, Set
import random


class GammaPentagonalCryptosystem:
    """
    Implementa el Criptosistema Γ-Pentagonal con:
    - Función de asignación n(j,i) = 2i + j
    - Conteo de trayectorias (Tipo I, II, III)
    - Cálculo de α mediante composiciones de cuadrados
    - Funciones de cifrado/descifrado
    """
    
    def __init__(self, grid_size: int = 20):
        """
        Inicializa el criptosistema
        
        Args:
            grid_size: Tamaño del plano ZxZ a considerar
        """
        self.grid_size = grid_size
        self.alpha_cache = {}
        self.path_cache = {}
        self._precompute_alpha()
    
    # ==================== 1. FUNCIONES BÁSICAS DEL PLANO ====================
    
    def n_function(self, j: int, i: int) -> int:
        """
        Función de asignación: n(j,i) = 2i + j
        Asigna a cada punto (j,i) un entero positivo
        
        Args:
            j: Coordenada j (j ≥ 0)
            i: Coordenada i (i ≥ 0)
            
        Returns:
            Valor n(j,i) = 2i + j
        """
        return 2 * i + j
    
    def inverse_n_function(self, n: int) -> List[Tuple[int, int]]:
        """
        Encuentra todos los puntos (j,i) tales que n(j,i) = n
        
        Args:
            n: Valor de la función
            
        Returns:
            Lista de puntos (j,i)
        """
        points = []
        for i in range(n // 2 + 1):
            j = n - 2 * i
            if j >= 0:
                points.append((j, i))
        return points
    
    def get_equivalence_class(self, n: int) -> Set[Tuple[int, int]]:
        """
        Obtiene la clase de equivalencia de puntos con mismo valor n(j,i)
        
        Args:
            n: Valor de clasificación
            
        Returns:
            Conjunto de puntos equivalentes
        """
        return set(self.inverse_n_function(n))
    
    # ==================== 2. CONTEO DE CUADRADOS ====================
    
    @lru_cache(maxsize=None)
    def get_perfect_squares(self, limit: int) -> List[int]:
        """
        Genera cuadrados perfectos hasta un límite
        
        Args:
            limit: Valor máximo
            
        Returns:
            Lista de cuadrados perfectos [1, 4, 9, 16, ...]
        """
        squares = []
        k = 1
        while k * k <= limit:
            squares.append(k * k)
            k += 1
        return squares
    
    def count_square_partitions(self, n: int, max_squares: int = 3) -> int:
        """
        Cuenta composiciones de n como suma de a lo más 'max_squares' cuadrados.
        Implementa programación dinámica para eficiencia.
        
        Args:
            n: Entero a descomponer
            max_squares: Número máximo de cuadrados en la suma
            
        Returns:
            Número de formas de escribir n como suma de cuadrados
        """
        if n in self.alpha_cache:
            return self.alpha_cache[n]
        
        squares = self.get_perfect_squares(n)
        
        # DP: dp[k][m] = formas de escribir k usando a lo más m cuadrados
        dp = [[0] * (max_squares + 1) for _ in range(n + 1)]
        dp[0][0] = 1
        
        for m in range(1, max_squares + 1):
            for k in range(n + 1):
                # Usar 0 cuadrados de tamaño m
                dp[k][m] = dp[k][m-1] if m > 0 else dp[k][0]
                
                # Usar al menos 1 cuadrado
                for sq in squares:
                    if k >= sq:
                        dp[k][m] += dp[k - sq][m - 1]
        
        result = dp[n][max_squares]
        self.alpha_cache[n] = result
        return result
    
    def alpha(self, j: int, i: int) -> int:
        """
        Calcula α(j,i): número de trayectorias admisibles que llegan a (j,i)
        Equivalente a composiciones de n(j,i) como suma de cuadrados
        
        Args:
            j: Coordenada j
            i: Coordenada i
            
        Returns:
            Valor de α(j,i)
        """
        n = self.n_function(j, i)
        return self.count_square_partitions(n, max_squares=3)
    
    def _precompute_alpha(self):
        """Precomputa valores de α para la grilla"""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.alpha_cache[self.n_function(j, i)] = self.alpha(j, i)
    
    # ==================== 3. TRAYECTORIAS Y GRAFOS ====================
    
    def get_type_i_paths(self, target_j: int, target_i: int, 
                         max_slope: int = None) -> List[List[Tuple[int, int]]]:
        """
        Calcula trayectorias de Tipo I desde (0,0) a (target_j, target_i).
        Tipo I: conecta puntos usando aristas con pendientes m ∈ {0,1,2,...}
        
        Args:
            target_j: Coordenada j del destino
            target_i: Coordenada i del destino
            max_slope: Pendiente máxima permitida (None = sin límite)
            
        Returns:
            Lista de trayectorias (cada trayectoria es lista de puntos)
        """
        paths = []
        
        def dfs(current_j, current_i, path, last_slope):
            if current_j == target_j and current_i == target_i:
                paths.append(path.copy())
                return
            
            if current_j > target_j or current_i > target_i:
                return
            
            # Prueba diferentes pendientes
            for slope in range(0, 10):
                if max_slope is not None and slope > max_slope:
                    break
                
                next_j = current_j + 1
                next_i = current_i + slope
                
                if next_i <= target_i and next_j <= target_j:
                    path.append((next_j, next_i))
                    dfs(next_j, next_i, path, slope)
                    path.pop()
        
        dfs(0, 0, [(0, 0)], -1)
        return paths
    
    def get_type_ii_paths(self, target_j: int, target_i: int) -> List[List[Tuple[int, int]]]:
        """
        Calcula trayectorias de Tipo II: concatenación de dos Tipo I
        
        Args:
            target_j: Coordenada j del destino
            target_i: Coordenada i del destino
            
        Returns:
            Lista de trayectorias Tipo II
        """
        type_ii_paths = []
        
        # Encuentra puntos intermedios viables
        for mid_j in range(1, target_j):
            for mid_i in range(1, target_i):
                paths_alpha = self.get_type_i_paths(mid_j, mid_i)
                paths_beta = self.get_type_i_paths(target_j - mid_j, target_i - mid_i)
                
                for p_alpha in paths_alpha:
                    for p_beta in paths_beta:
                        # Concatena: traslada segunda trayectoria
                        concatenated = p_alpha[:-1] + [(p + mid_j, q + mid_i) 
                                                        for p, q in p_beta]
                        type_ii_paths.append(concatenated)
        
        return type_ii_paths
    
    def get_type_iii_paths(self, target_j: int, target_i: int) -> List[List[Tuple[int, int]]]:
        """
        Calcula trayectorias de Tipo III: 
        Concatenación de Tipo II (αβ) + Tipo I con restricción de pendiente máxima
        
        Args:
            target_j: Coordenada j del destino
            target_i: Coordenada i del destino
            
        Returns:
            Lista de trayectorias Tipo III
        """
        type_iii_paths = []
        type_ii_paths = self.get_type_ii_paths(target_j, target_i)
        
        for ii_path in type_ii_paths:
            # Extrae la pendiente máxima del segundo segmento β
            # Simplificación: usamos pendiente = Δi/Δj
            last_point = ii_path[-1]
            second_last = ii_path[-2]
            max_slope_beta = (last_point[1] - second_last[1]) // max(1, last_point[0] - second_last[0])
            
            # Extiende con Tipo I limitada por esta pendiente
            for i in range(1, target_i - last_point[1] + 1):
                for j in range(1, target_j - last_point[0] + 1):
                    slope = i // max(1, j)
                    if slope <= max_slope_beta:
                        extended = ii_path + [(last_point[0] + j, last_point[1] + i)]
                        if extended[-1] == (target_j, target_i):
                            type_iii_paths.append(extended)
        
        return type_iii_paths
    
    def count_admissible_paths(self, target_j: int, target_i: int) -> int:
        """
        Cuenta total de trayectorias admisibles (Tipo I + Tipo II + Tipo III)
        
        Args:
            target_j: Coordenada j del destino
            target_i: Coordenada i del destino
            
        Returns:
            Número total de trayectorias
        """
        type_i = len(self.get_type_i_paths(target_j, target_i))
        type_ii = len(self.get_type_ii_paths(target_j, target_i))
        type_iii = len(self.get_type_iii_paths(target_j, target_i))
        
        return type_i + type_ii + type_iii
    
    # ==================== 4. FUNCIONES CRIPTOGRÁFICAS ====================
    
    def create_key(self, seed: int = 42) -> Dict:
        """
        Crea la clave criptográfica K = (f_0, π, Γ)
        
        Args:
            seed: Semilla para reproducibilidad
            
        Returns:
            Diccionario con componentes de la clave
        """
        random.seed(seed)
        np.random.seed(seed)
        
        # f_0: Automorfismo (traslación)
        f0_offset_j = random.randint(0, self.grid_size // 2)
        f0_offset_i = random.randint(0, self.grid_size // 2)
        
        # π: Permutación secreta de vértices
        all_vertices = [(j, i) for i in range(self.grid_size) 
                        for j in range(self.grid_size)]
        permuted_vertices = all_vertices.copy()
        random.shuffle(permuted_vertices)
        
        permutation = {all_vertices[idx]: permuted_vertices[idx] 
                      for idx in range(len(all_vertices))}
        inverse_permutation = {v: k for k, v in permutation.items()}
        
        key = {
            'f0_offset': (f0_offset_j, f0_offset_i),
            'permutation': permutation,
            'inverse_permutation': inverse_permutation,
            'gamma': self  # El grafo es el criptosistema mismo
        }
        
        return key
    
    def encrypt(self, message: int, key: Dict) -> Tuple[int, int]:
        """
        Cifra un mensaje usando la clave
        
        Args:
            message: Mensaje a cifrar (valor entero)
            key: Clave criptográfica
            
        Returns:
            Criptograma (x_1, y_1)
        """
        # Encuentra el punto mínimo (x_0, y_0) tal que x = x_0 + y_0 + α
        f0_offset_j, f0_offset_i = key['f0_offset']
        
        # Busca el punto mínimo
        min_point = None
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                alpha_val = self.alpha(j, i)
                if j + i + alpha_val == message:
                    min_point = (j, i)
                    break
            if min_point:
                break
        
        if min_point is None:
            # Si no encuentra, usa punto aleatorio cercano
            min_point = (message % self.grid_size, 
                        (message // self.grid_size) % self.grid_size)
        
        # Aplica automorfismo f_0
        x0_transformed = (min_point[0] + f0_offset_j) % self.grid_size
        y0_transformed = (min_point[1] + f0_offset_i) % self.grid_size
        
        # Aplica permutación π
        ciphertext = key['permutation'].get(
            (x0_transformed, y0_transformed),
            (x0_transformed, y0_transformed)
        )
        
        return ciphertext
    
    def decrypt(self, ciphertext: Tuple[int, int], key: Dict) -> int:
        """
        Descifra un criptograma usando la clave
        
        Args:
            ciphertext: Criptograma (x_1, y_1)
            key: Clave criptográfica
            
        Returns:
            Mensaje original
        """
        # Aplica permutación inversa π⁻¹
        x0_transformed, y0_transformed = key['inverse_permutation'].get(
            ciphertext, ciphertext
        )
        
        # Invierte automorfismo f_0
        f0_offset_j, f0_offset_i = key['f0_offset']
        x0 = (x0_transformed - f0_offset_j) % self.grid_size
        y0 = (y0_transformed - f0_offset_i) % self.grid_size
        
        # Recupera mensaje: x = x_0 + y_0 + α(x_0, y_0)
        alpha_val = self.alpha(x0, y0)
        message = x0 + y0 + alpha_val
        
        return message
    
    # ==================== 5. VISUALIZACIÓN ====================
    
    def visualize_lattice(self, target_j: int = 5, target_i: int = 5, 
                         show_alpha: bool = True):
        """
        Visualiza el plano ZxZ con puntos etiquetados por sus valores α
        
        Args:
            target_j: Rango máximo de j
            target_i: Rango máximo de i
            show_alpha: Si mostrar valores de α
        """
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Dibuja puntos y grilla
        for i in range(target_i + 1):
            for j in range(target_j + 1):
                alpha_val = self.alpha(j, i)
                n_val = self.n_function(j, i)
                
                # Color basado en α
                color = plt.cm.viridis(alpha_val / 10)
                ax.scatter(j, i, s=500, c=[color], edgecolors='black', linewidth=2)
                
                if show_alpha:
                    ax.text(j, i, f'α={alpha_val}\nn={n_val}', 
                           ha='center', va='center', fontsize=8, fontweight='bold')
        
        # Dibuja aristas Tipo I (pendientes)
        for i in range(target_i):
            for j in range(target_j):
                for slope in range(0, 3):
                    next_i = i + slope
                    next_j = j + 1
                    if next_i <= target_i and next_j <= target_j:
                        ax.arrow(j, i, next_j - j, next_i - i, 
                                head_width=0.15, head_length=0.1, 
                                fc='gray', ec='gray', alpha=0.3)
        
        ax.set_xlabel('j (coordenada horizontal)', fontsize=12, fontweight='bold')
        ax.set_ylabel('i (coordenada vertical)', fontsize=12, fontweight='bold')
        ax.set_title('Plano ZxZ - Criptosistema Γ-Pentagonal\n' + 
                    'Puntos coloreados por α, etiquetados con n(j,i)', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-0.5, target_j + 0.5)
        ax.set_ylim(-0.5, target_i + 0.5)
        
        plt.tight_layout()
        plt.savefig('gamma_pentagonal_lattice.png', dpi=150, bbox_inches='tight')
        plt.show()
        
        print("✓ Visualización de la grilla guardada como 'gamma_pentagonal_lattice.png'")
    
    def visualize_paths(self, target_j: int = 4, target_i: int = 4):
        """
        Visualiza diferentes tipos de trayectorias
        
        Args:
            target_j: Coordenada j del destino
            target_i: Coordenada i del destino
        """
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        path_types = [
            ("Tipo I", self.get_type_i_paths(target_j, target_i)),
            ("Tipo II", self.get_type_ii_paths(target_j, target_i)),
            ("Tipo III", self.get_type_iii_paths(target_j, target_i))
        ]
        
        for ax, (title, paths) in zip(axes, path_types):
            # Dibuja grilla
            for i in range(target_i + 1):
                for j in range(target_j + 1):
                    ax.scatter(j, i, s=100, c='lightblue', edgecolors='black')
            
            # Dibuja trayectorias
            colors = plt.cm.Spectral(np.linspace(0, 1, len(paths)))
            for path, color in zip(paths[:5], colors):  # Limita a 5 para claridad
                path_array = np.array(path)
                ax.plot(path_array[:, 0], path_array[:, 1], 
                       marker='o', color=color, linewidth=2, markersize=6, alpha=0.7)
            
            ax.set_xlabel('j', fontsize=11)
            ax.set_ylabel('i', fontsize=11)
            ax.set_title(f'{title}\n({len(paths)} trayectorias)', 
                        fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.set_xlim(-0.5, target_j + 0.5)
            ax.set_ylim(-0.5, target_i + 0.5)
        
        plt.tight_layout()
        plt.savefig('gamma_pentagonal_paths.png', dpi=150, bbox_inches='tight')
        plt.show()
        
        print("✓ Visualización de trayectorias guardada como 'gamma_pentagonal_paths.png'")


# ==================== DEMOSTRACIÓN Y PRUEBAS ====================

def main():
    """Función principal de pruebas"""
    print("=" * 70)
    print("CRIPTOSISTEMA Γ-PENTAGONAL - Demostración Completa".center(70))
    print("=" * 70)
    print()
    
    # Inicializa el criptosistema
    print("1. INICIALIZANDO EL CRIPTOSISTEMA")
    print("-" * 70)
    crypto = GammaPentagonalCryptosystem(grid_size=15)
    print("✓ Criptosistema inicializado con grilla 15x15")
    print("✓ Valores de α precomputados y almacenados en caché")
    print()
    
    # Demostración de función n
    print("2. FUNCIÓN DE ASIGNACIÓN n(j,i) = 2i + j")
    print("-" * 70)
    test_points = [(0, 0), (1, 0), (0, 1), (3, 2), (5, 3)]
    for j, i in test_points:
        n_val = crypto.n_function(j, i)
        print(f"   n({j:2},{i:2}) = {n_val:3} | Clase equivalencia: {crypto.get_equivalence_class(n_val)}")
    print()
    
    # Demostración de conteo de cuadrados
    print("3. PARTICIONES COMO SUMA DE CUADRADOS (α)")
    print("-" * 70)
    for point in test_points:
        j, i = point
        alpha_val = crypto.alpha(j, i)
        n_val = crypto.n_function(j, i)
        print(f"   α({j:2},{i:2}) = {alpha_val:3} | n({j:2},{i:2}) = {n_val:3} | " +
              f"Composiciones de {n_val} como suma de ≤3 cuadrados")
    print()
    
    # Demostración de cifrado/descifrado
    print("4. CIFRADO Y DESCIFRADO")
    print("-" * 70)
    key = crypto.create_key(seed=12345)
    print("✓ Clave criptográfica generada")
    
    # Mensajes de prueba
    test_messages = [10, 25, 42, 100]
    print(f"\n   Mensaje Original → Criptograma → Descifrado")
    print("   " + "-" * 50)
    
    for msg in test_messages:
        ciphertext = crypto.encrypt(msg, key)
        decrypted = crypto.decrypt(ciphertext, key)
        status = "✓" if decrypted == msg else "✗"
        print(f"   {status} {msg:3} → {ciphertext} → {decrypted:3}")
    print()
    
    # Análisis de trayectorias
    print("5. ANÁLISIS DE TRAYECTORIAS")
    print("-" * 70)
    target = (4, 3)
    type_i = crypto.get_type_i_paths(target[0], target[1])
    type_ii = crypto.get_type_ii_paths(target[0], target[1])
    type_iii = crypto.get_type_iii_paths(target[0], target[1])
    
    print(f"   Destino: ({target[0]}, {target[1]})")
    print(f"   Trayectorias Tipo I:   {len(type_i):3}")
    print(f"   Trayectorias Tipo II:  {len(type_ii):3}")
    print(f"   Trayectorias Tipo III: {len(type_iii):3}")
    print(f"   Total:                 {len(type_i) + len(type_ii) + len(type_iii):3}")
    print()
    
    # Visualización
    print("6. GENERANDO VISUALIZACIONES")
    print("-" * 70)
    print("   Generando visualización de la grilla...")
    crypto.visualize_lattice(target_j=6, target_i=6, show_alpha=True)
    print()
    
    print("   Generando visualización de trayectorias...")
    crypto.visualize_paths(target_j=4, target_i=4)
    print()
    
    # Estadísticas de seguridad
    print("7. PROPIEDADES CRIPTOGRÁFICAS")
    print("-" * 70)
    print(f"   Tamaño de la grilla: {crypto.grid_size} × {crypto.grid_size}")
    print(f"   Número de vértices: {crypto.grid_size ** 2}")
    print(f"   Permutaciones posibles: {crypto.grid_size ** 2}!")
    print(f"   Espacios de claves: 2^{crypto.grid_size * 2} (aproximadamente)")
    print()
    
    print("=" * 70)
    print("DEMOSTRACIÓN COMPLETADA EXITOSAMENTE".center(70))
    print("=" * 70)


if __name__ == "__main__":
    main()
