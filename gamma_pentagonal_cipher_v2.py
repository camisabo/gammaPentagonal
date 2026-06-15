"""
Criptosistema Gamma-Pentagonal REVISADO - Deducción de Lógica
Basado en análisis del vector de prueba académico UNAL
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
from typing import List, Tuple
from collections import Counter


class GammaPentagonalCipherV2:
    """
    Versión revisada del Criptosistema Gamma-Pentagonal.
    
    Basada en análisis del vector de prueba UNAL.
    """
    
    def __init__(self, p0: Tuple[int, int] = (-8, -6)):
        """
        Inicializa el cifrador.
        
        Args:
            p0 (Tuple): Punto inicial del grafo en coordenadas (x, y).
        """
        self.p0 = p0
        self.trajectory = []
        self.state = p0
        
        # Mapeo de caracteres a valores iniciales deducido del vector de prueba
        # Esto representa la "permutación sigma" implícita en el sistema
        self.char_map = {
            'a': 8, 'b': 7, 'c': 0, 'd': 0, 'e': 5, 'f': 2,
            'g': 4, 'h': 6, 'i': 2, 'j': 9, 'k': 3, 'l': 1,
            'm': 8, 'n': 5, 'o': 3, 'p': 2, 'q': 1, 'r': 1,
            's': 1, 't': 2, 'u': 5, 'v': 6, 'w': 7, 'x': 8,
            'y': 9, 'z': 0
        }
    
    def _compute_next_x(self, current_x: int, char: str, step: int) -> int:
        """
        Computa la siguiente coordenada X.
        
        Basada en análisis del vector de prueba:
        - La secuencia X muestra incrementos que responden al carácter
        - Se mantiene un contador/acumulador que evoluciona
        """
        char_val = ord(char) % 10
        # Incremento basado en el carácter y su posición
        increment = (char_val + step // 3) % 10
        next_x = (current_x + increment) % 10
        return next_x
    
    def _compute_next_y(self, current_y: int, char: str, 
                       current_x: int, step: int) -> int:
        """
        Computa la siguiente coordenada Y.
        
        Utiliza:
        - Valor ASCII del carácter
        - Posición en el texto
        - Estado anterior
        - Rango módulo 20
        """
        char_val = ord(char)
        # Incremento complejo que mezcla múltiples parámetros
        increment = (char_val + current_x * 5 + step * 3) % 20
        next_y = (current_y + increment) % 20
        return next_y
    
    def encrypt(self, plaintext: str) -> List[Tuple[int, int]]:
        """
        Cifra un texto plano.
        
        Args:
            plaintext (str): Texto a cifrar
            
        Returns:
            List[Tuple]: Lista de coordenadas (x, y)
        """
        self.trajectory = []
        current_x = self.p0[0] % 10  # Normalizar X inicial
        current_y = self.p0[1] % 20  # Normalizar Y inicial
        ciphertext_coords = []
        
        for step, char in enumerate(plaintext.lower()):
            # Calcular próximas coordenadas
            next_x = self._compute_next_x(current_x, char, step)
            next_y = self._compute_next_y(current_y, char, next_x, step)
            
            # Normalizar al rango [0, 20)
            next_x = next_x % 10
            next_y = next_y % 20
            
            # Actualizar estado
            current_x = next_x
            current_y = next_y
            
            self.trajectory.append((next_x, next_y))
            ciphertext_coords.append((next_x, next_y))
        
        return ciphertext_coords


class GammaPentagonalVisualizer:
    """Generador de visualizaciones."""
    
    def __init__(self, ciphertext_coords: List[Tuple[int, int]], 
                 plaintext: str, p0: Tuple[int, int] = (-8, -6)):
        self.coords = ciphertext_coords
        self.plaintext = plaintext
        self.p0 = p0
    
    def visualize_trajectory_graph(self, title: str = "Grafo de Trayectorias Gamma-Pentagonal",
                                   figsize: Tuple[int, int] = (14, 10)):
        """Visualiza el grafo de trayectorias."""
        fig, ax = plt.subplots(figsize=figsize)
        G = nx.DiGraph()
        
        # Agregar nodo inicial P0
        G.add_node(f"P₀{self.p0}")
        pos = {f"P₀{self.p0}": (self.p0[0], self.p0[1])}
        
        # Agregar nodos para cada coordenada
        for i, coord in enumerate(self.coords):
            node_label = f"C{i+1}{coord}"
            G.add_node(node_label)
            pos[node_label] = coord
        
        # Agregar aristas
        if self.coords:
            G.add_edge(f"P₀{self.p0}", f"C1{self.coords[0]}")
        
        for i in range(len(self.coords) - 1):
            G.add_edge(f"C{i+1}{self.coords[i]}", 
                      f"C{i+2}{self.coords[i+1]}")
        
        # Dibujar
        node_colors = ['#FF6B6B'] + ['#4ECDC4'] * len(self.coords)
        node_sizes = [2000] + [1500] * len(self.coords)
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                              node_size=node_sizes, ax=ax, alpha=0.9)
        nx.draw_networkx_edges(G, pos, edge_color='gray', 
                              arrows=True, arrowsize=20, 
                              arrowstyle='->', ax=ax, width=2)
        nx.draw_networkx_labels(G, pos, font_size=7, font_weight='bold', ax=ax)
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        plt.tight_layout()
        return fig, ax
    
    def visualize_entropy_heatmaps(self, figsize: Tuple[int, int] = (16, 6)):
        """Visualiza mapas de calor antes y después."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # ANTES: Distribución de caracteres
        char_to_category = {
            'a': 0, 'b': 0, 'c': 0,
            'd': 1, 'e': 1, 'f': 1,
            'g': 2, 'h': 2, 'i': 2,
            'j': 3, 'k': 3, 'l': 3,
            'm': 4, 'n': 4, 'o': 4,
            'p': 5, 'q': 5, 'r': 5,
            's': 6, 't': 6, 'u': 6,
            'v': 7, 'w': 7, 'x': 7,
            'y': 8, 'z': 8,
            ' ': 9
        }
        
        category_counts = [0] * 10
        for char in self.plaintext.lower():
            if char in char_to_category:
                category_counts[char_to_category[char]] += 1
            else:
                category_counts[9] += 1
        
        heatmap_before = np.array(category_counts).reshape(2, 5)
        
        sns.heatmap(heatmap_before, annot=True, fmt='d', cmap='YlOrRd',
                   cbar_kws={'label': 'Frecuencia'}, ax=ax1,
                   xticklabels=['Grupo 1-5', 'Grupo 6-10', 'Grupo 11-15', 
                               'Grupo 16-20', 'Otros'],
                   yticklabels=['Fila 1', 'Fila 2'])
        ax1.set_title('ANTES: Distribución de Frecuencia del Texto Plano',
                     fontsize=12, fontweight='bold')
        
        # DESPUÉS: Distribución espacial
        cell_counts = np.zeros((2, 5), dtype=int)
        for x, y in self.coords:
            cell_x = x % 5
            cell_y = y % 2
            cell_counts[cell_y, cell_x] += 1
        
        sns.heatmap(cell_counts, annot=True, fmt='d', cmap='viridis',
                   cbar_kws={'label': 'Frecuencia'}, ax=ax2,
                   xticklabels=['x∈[0,4)', 'x∈[5,9)', 'x∈[10,14)', 
                               'x∈[15,19)', 'x∈[20,24)'],
                   yticklabels=['y∈[0,9)', 'y∈[10,19)'])
        ax2.set_title('DESPUÉS: Distribución Espacial de Coordenadas Cifradas',
                     fontsize=12, fontweight='bold')
        
        plt.suptitle('Análisis de Entropía: Destrucción de Patrones de Lenguaje',
                    fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        return fig, (ax1, ax2)


def main():
    """Función principal."""
    print("\n" + "=" * 70)
    print("CRIPTOSISTEMA GAMMA-PENTAGONAL V2 (REVISADO)")
    print("=" * 70 + "\n")
    
    # Vector de prueba
    expected_coords = [
        (0, 18), (1, 11), (2, 3), (2, 12), (2, 16), (3, 5), (4, 1), (5, 14),
        (8, 0), (2, 2), (2, 4), (8, 0), (9, 15), (1, 10), (5, 0), (5, 4),
        (5, 16), (7, 13), (7, 7), (0, 19), (1, 18), (2, 0)
    ]
    plaintext = "criptografiayseguridad"
    
    cipher = GammaPentagonalCipherV2()
    result_coords = cipher.encrypt(plaintext)
    
    # Validación
    print("VALIDACIÓN CONTRA VECTOR DE PRUEBA")
    print("-" * 70)
    matches = sum(1 for e, r in zip(expected_coords, result_coords) if e == r)
    print(f"Coincidencias: {matches}/{len(expected_coords)}")
    
    if matches > 0:
        print(f"\n✓ Mejora: Se lograron {matches} coincidencias")
    
    # Mostrar primeras coordinadas
    print(f"\nPrimeras 5 coordenadas:")
    print(f"  Esperadas: {expected_coords[:5]}")
    print(f"  Obtenidas: {result_coords[:5]}")
    
    # Generar visualizaciones
    print("\nGenerando visualizaciones...")
    visualizer = GammaPentagonalVisualizer(result_coords, plaintext)
    
    fig1, _ = visualizer.visualize_trajectory_graph()
    plt.savefig('gamma_pentagonal_trajectory_v2.png', dpi=300, bbox_inches='tight')
    print("✓ Grafo guardado como 'gamma_pentagonal_trajectory_v2.png'")
    
    fig2, _ = visualizer.visualize_entropy_heatmaps()
    plt.savefig('gamma_pentagonal_entropy_v2.png', dpi=300, bbox_inches='tight')
    print("✓ Mapas de calor guardados como 'gamma_pentagonal_entropy_v2.png'")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
