"""
Replicación de Gráficas del Profesor
Genera visualizaciones exactas de los puntos y trayectorias mencionados
"""

from gamma_pentagonal_cryptosystem import GammaPentagonalCryptosystem
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle
import numpy as np


class GeneradorGraficasProfesor:
    """Genera las gráficas exactas mostradas por el profesor"""
    
    def __init__(self):
        self.crypto = GammaPentagonalCryptosystem(grid_size=20)
    
    def figura_1_puntos_basicos(self):
        """
        Figura 1: Puntos básicos con valores n y α
        """
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Parámetros de la grilla
        max_j = 6
        max_i = 5
        
        # Dibuja los puntos de la grilla
        for i in range(max_i + 1):
            for j in range(max_j + 1):
                ax.plot(j, i, 'o', color='lightblue', markersize=10, 
                       markeredgecolor='black', markeredgewidth=0.5)
        
        # Puntos especiales con etiquetas
        puntos_especiales = [
            ((1, 1), 3, 1, "red"),
            ((1, 4), 9, 2, "blue"),
            ((3, 3), 9, 2, "green"),
            ((5, 2), 9, 2, "purple"),
        ]
        
        for (j, i), n, alpha, color in puntos_especiales:
            # Dibuja punto grande
            ax.plot(j, i, 'o', color=color, markersize=18, 
                   markeredgecolor='black', markeredgewidth=2, zorder=5)
            
            # Etiqueta con nombre y valores
            label_text = f"({j},{i})\nn={n}\nα={alpha}"
            ax.text(j, i-0.8, label_text, ha='center', va='top', 
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor=color, alpha=0.5))
        
        # Grilla y ejes
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xlabel('j (columna)', fontsize=13, fontweight='bold')
        ax.set_ylabel('i (fila)', fontsize=13, fontweight='bold')
        ax.set_title('Figura 1: Puntos de Ejemplo - Función n(j,i) = 2i + j', 
                    fontsize=14, fontweight='bold', pad=20)
        
        # Anotaciones
        ax.text(0.5, 5.2, 'Puntos equivalentes:\n(1,4), (3,3), (5,2)\nTodos con n=9', 
               fontsize=10, style='italic',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        
        ax.set_xlim(-0.5, max_j + 0.5)
        ax.set_ylim(-1.5, max_i + 0.8)
        ax.set_aspect('equal')
        
        plt.tight_layout()
        plt.savefig('figura_1_puntos_basicos.png', dpi=150, bbox_inches='tight')
        print("✓ Figura 1 guardada: 'figura_1_puntos_basicos.png'")
        plt.show()
    
    def figura_2_trayectorias_tipo_i_ii(self):
        """
        Figura 2: Trayectorias Tipo I y II terminando en (6,4) y (7,6)
        """
        fig, axes = plt.subplots(1, 2, figsize=(16, 7))
        
        puntos_destino = [(6, 4), (7, 6)]
        
        for ax, (j_dest, i_dest) in zip(axes, puntos_destino):
            # Grilla
            for i in range(i_dest + 1):
                for j in range(j_dest + 1):
                    ax.plot(j, i, 'o', color='lightgray', markersize=8, alpha=0.5)
            
            # Origen
            ax.plot(0, 0, 's', color='black', markersize=15, label='Origen (0,0)', zorder=5)
            
            # Destino
            ax.plot(j_dest, i_dest, '*', color='red', markersize=25, 
                   label=f'Destino ({j_dest},{i_dest})', zorder=5)
            
            # Obtiene valores
            n_val = self.crypto.n_function(j_dest, i_dest)
            alpha_val = self.crypto.alpha(j_dest, i_dest)
            
            # Obtiene trayectorias
            type_i = self.crypto.get_type_i_paths(j_dest, i_dest)
            type_ii = self.crypto.get_type_ii_paths(j_dest, i_dest)
            
            # Dibuja Tipo I
            colors_i = plt.cm.Blues(np.linspace(0.4, 0.9, min(3, len(type_i))))
            for idx, path in enumerate(type_i[:3]):
                path_array = np.array(path)
                ax.plot(path_array[:, 0], path_array[:, 1], 'o-', 
                       color=colors_i[idx], linewidth=2, markersize=4, 
                       alpha=0.7, label=f'Tipo I - Ruta {idx+1}' if idx == 0 else '')
            
            # Dibuja Tipo II (con color diferente)
            colors_ii = plt.cm.Oranges(np.linspace(0.4, 0.9, min(2, len(type_ii))))
            for idx, path in enumerate(type_ii[:2]):
                path_array = np.array(path)
                ax.plot(path_array[:, 0], path_array[:, 1], 's--', 
                       color=colors_ii[idx], linewidth=2, markersize=5, 
                       alpha=0.7, label=f'Tipo II - Ruta {idx+1}' if idx == 0 else '')
            
            # Configuración
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('j (columna)', fontsize=12, fontweight='bold')
            ax.set_ylabel('i (fila)', fontsize=12, fontweight='bold')
            ax.set_title(f'Trayectorias a v({j_dest},{i_dest})\nn={n_val}, α={alpha_val}', 
                        fontsize=13, fontweight='bold')
            ax.legend(fontsize=9, loc='upper left')
            ax.set_xlim(-0.5, j_dest + 0.5)
            ax.set_ylim(-0.5, i_dest + 0.5)
            
            # Estadísticas
            total_i = len(type_i)
            total_ii = len(type_ii)
            ax.text(0.98, 0.02, f'Tipo I: {total_i}\nTipo II: {total_ii}\nTotal: {total_i + total_ii}',
                   transform=ax.transAxes, fontsize=10, verticalalignment='bottom',
                   horizontalalignment='right',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        fig.suptitle('Figura 2: Trayectorias Tipo I y II', fontsize=15, fontweight='bold', y=1.00)
        plt.tight_layout()
        plt.savefig('figura_2_trayectorias_tipo_i_ii.png', dpi=150, bbox_inches='tight')
        print("✓ Figura 2 guardada: 'figura_2_trayectorias_tipo_i_ii.png'")
        plt.show()
    
    def figura_3_trayectorias_tipo_iii(self):
        """
        Figura 3: Trayectorias Tipo III terminando en (6,7)
        """
        fig, ax = plt.subplots(figsize=(13, 11))
        
        j_dest, i_dest = 6, 7
        
        # Grilla
        for i in range(i_dest + 1):
            for j in range(j_dest + 1):
                ax.plot(j, i, 'o', color='lightgray', markersize=8, alpha=0.5)
        
        # Origen
        ax.plot(0, 0, 's', color='black', markersize=18, label='Origen (0,0)', zorder=5)
        
        # Destino
        ax.plot(j_dest, i_dest, '*', color='darkgreen', markersize=35, 
               label=f'Destino ({j_dest},{i_dest})', zorder=5)
        
        # Valores
        n_val = self.crypto.n_function(j_dest, i_dest)
        alpha_val = self.crypto.alpha(j_dest, i_dest)
        
        # Obtiene trayectorias
        type_iii = self.crypto.get_type_iii_paths(j_dest, i_dest)
        
        # Dibuja trayectorias Tipo III
        colors = plt.cm.Greens(np.linspace(0.3, 0.9, min(5, len(type_iii))))
        for idx, path in enumerate(type_iii[:5]):
            path_array = np.array(path)
            ax.plot(path_array[:, 0], path_array[:, 1], 'o-', 
                   color=colors[idx], linewidth=2.5, markersize=6, 
                   alpha=0.8, label=f'Ruta {idx+1}')
        
        # Líneas de referencia
        ax.axhline(y=0, color='gray', linestyle=':', alpha=0.3)
        ax.axvline(x=0, color='gray', linestyle=':', alpha=0.3)
        
        # Configuración
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('j (columna)', fontsize=13, fontweight='bold')
        ax.set_ylabel('i (fila)', fontsize=13, fontweight='bold')
        ax.set_title(f'Figura 3: Trayectorias Tipo III a v({j_dest},{i_dest})\nn={n_val}, α={alpha_val}',
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(fontsize=10, loc='upper left', ncol=1)
        ax.set_xlim(-0.5, j_dest + 0.5)
        ax.set_ylim(-0.5, i_dest + 0.5)
        ax.set_aspect('equal')
        
        # Anotación
        ax.text(0.98, 0.02, f'Total Tipo III: {len(type_iii)}',
               transform=ax.transAxes, fontsize=11, verticalalignment='bottom',
               horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig('figura_3_trayectorias_tipo_iii.png', dpi=150, bbox_inches='tight')
        print("✓ Figura 3 guardada: 'figura_3_trayectorias_tipo_iii.png'")
        plt.show()
    
    def figura_4_comparacion_completa(self):
        """
        Figura 4: Comparación completa de todos los puntos del profesor
        """
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)
        
        # Puntos a comparar
        puntos_comparar = [
            ((1, 1), "Ejemplo Básico"),
            ((1, 4), "Equivalente n=9"),
            ((3, 3), "Equivalente n=9"),
            ((5, 2), "Equivalente n=9"),
            ((6, 4), "Tipo I/II"),
            ((7, 6), "Tipo I/II"),
            ((6, 7), "Tipo III"),
        ]
        
        for idx, ((j, i), tipo) in enumerate(puntos_comparar):
            ax = fig.add_subplot(gs[idx // 3, idx % 3])
            
            n_val = self.crypto.n_function(j, i)
            alpha_val = self.crypto.alpha(j, i)
            
            # Grilla pequeña
            for ii in range(max(1, i) + 1):
                for jj in range(max(1, j) + 1):
                    ax.plot(jj, ii, 'o', color='lightgray', markersize=6, alpha=0.4)
            
            # Punto
            ax.plot(j, i, 'o', color='red', markersize=15, 
                   markeredgecolor='black', markeredgewidth=1, zorder=5)
            
            # Origen
            ax.plot(0, 0, 's', color='black', markersize=8, zorder=4)
            
            # Algunas trayectorias
            type_i = self.crypto.get_type_i_paths(j, i)
            for path in type_i[:2]:
                path_array = np.array(path)
                ax.plot(path_array[:, 0], path_array[:, 1], '-', 
                       color='blue', alpha=0.4, linewidth=1)
            
            # Labels
            ax.text(j*0.5, i*1.1, f"({j},{i})\nn={n_val}, α={alpha_val}",
                   ha='center', fontsize=9, fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
            
            ax.set_title(f'{tipo}', fontsize=10, fontweight='bold')
            ax.grid(True, alpha=0.2)
            ax.set_xlim(-0.5, j + 0.5)
            ax.set_ylim(-0.5, i + 0.5)
        
        # Elimina el último subplot si hay espacio
        if len(puntos_comparar) < 9:
            ax = fig.add_subplot(gs[2, 2])
            ax.axis('off')
            
            # Añade leyenda
            leyenda_text = """
LEYENDA:
• ■ = Origen (0,0)
• ● = Punto estudiado
• ─ = Trayectoria (muestra 2)
            
VALORES:
n = 2i + j
α = composiciones
            """
            ax.text(0.5, 0.5, leyenda_text, ha='center', va='center',
                   fontsize=10, fontfamily='monospace',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        
        fig.suptitle('Figura 4: Comparación de Todos los Puntos del Profesor',
                    fontsize=15, fontweight='bold')
        plt.savefig('figura_4_comparacion_completa.png', dpi=150, bbox_inches='tight')
        print("✓ Figura 4 guardada: 'figura_4_comparacion_completa.png'")
        plt.show()
    
    def figura_5_tabla_resumen_visual(self):
        """
        Figura 5: Tabla visual con todos los datos
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.axis('off')
        
        # Datos para la tabla
        datos = [
            ['Punto (j,i)', 'n(j,i)', 'α(j,i)', 'Clase Equivalencia', 'Tipo de Trayectoria'],
            ['(1,1)', '3', '1', 'C₃', 'Básico'],
            ['(1,4)', '9', '2', 'C₉: {(1,4), (3,3), (5,2)}', 'Equivalente'],
            ['(3,3)', '9', '2', 'C₉: {(1,4), (3,3), (5,2)}', 'Equivalente'],
            ['(5,2)', '9', '2', 'C₉: {(1,4), (3,3), (5,2)}', 'Equivalente'],
            ['(6,4)', '16', '3', 'C₁₆', 'Tipo I/II'],
            ['(7,6)', '18', '?', 'C₁₈', 'Tipo I/II'],
            ['(6,7)', '19', '?', 'C₁₉', 'Tipo III'],
        ]
        
        # Crea tabla
        table = ax.table(cellText=datos, cellLoc='center', loc='center',
                        colWidths=[0.15, 0.10, 0.10, 0.35, 0.25])
        
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2.5)
        
        # Formatea encabezado
        for i in range(5):
            table[(0, i)].set_facecolor('#4CAF50')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Colores alternos para filas
        for i in range(1, len(datos)):
            for j in range(5):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#f0f0f0')
                else:
                    table[(i, j)].set_facecolor('#ffffff')
                
                # Resalta clase equivalente
                if j == 3 and 'C₉' in datos[i][j]:
                    table[(i, j)].set_facecolor('#fff9c4')
        
        # Título
        plt.text(0.5, 0.98, 'Tabla 1: Resumen de Puntos del Criptosistema Γ-Pentagonal',
                ha='center', va='top', fontsize=14, fontweight='bold',
                transform=ax.transAxes)
        
        # Anotaciones
        anotacion = """
Notas Importantes:
• Todos los puntos en C₉ = {(1,4), (3,3), (5,2)} son equivalentes con α = 2
• n(j,i) = 2i + j define la asignación de valores
• α(j,i) cuenta el número de trayectorias admisibles (composiciones de cuadrados)
• Los puntos (6,4) y (7,6) demuestran Trayectorias Tipo I y II
• El punto (6,7) demuestra Trayectorias Tipo III con restricción de pendiente
        """
        
        plt.text(0.5, 0.05, anotacion, ha='center', va='bottom', fontsize=9,
                style='italic', transform=ax.transAxes,
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig('figura_5_tabla_resumen.png', dpi=150, bbox_inches='tight')
        print("✓ Figura 5 guardada: 'figura_5_tabla_resumen.png'")
        plt.show()


def main():
    """Función principal"""
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + "REPLICACIÓN DE GRÁFICAS DEL PROFESOR".center(78) + "║")
    print("║" + "Criptosistema Γ-Pentagonal".center(78) + "║")
    print("╚" + "═" * 78 + "╝")
    
    generador = GeneradorGraficasProfesor()
    
    print("\n📊 Generando gráficas...")
    print("-" * 80)
    
    print("\nGenerando Figura 1: Puntos Básicos...")
    generador.figura_1_puntos_basicos()
    
    print("\nGenerando Figura 2: Trayectorias Tipo I y II...")
    generador.figura_2_trayectorias_tipo_i_ii()
    
    print("\nGenerando Figura 3: Trayectorias Tipo III...")
    generador.figura_3_trayectorias_tipo_iii()
    
    print("\nGenerando Figura 4: Comparación Completa...")
    generador.figura_4_comparacion_completa()
    
    print("\nGenerando Figura 5: Tabla Resumen Visual...")
    generador.figura_5_tabla_resumen_visual()
    
    print("\n" + "═" * 80)
    print("✅ TODAS LAS GRÁFICAS GENERADAS EXITOSAMENTE".center(80))
    print("═" * 80)
    print("\nArchivos generados:")
    print("  1. figura_1_puntos_basicos.png")
    print("  2. figura_2_trayectorias_tipo_i_ii.png")
    print("  3. figura_3_trayectorias_tipo_iii.png")
    print("  4. figura_4_comparacion_completa.png")
    print("  5. figura_5_tabla_resumen.png")
    print()


if __name__ == "__main__":
    main()
