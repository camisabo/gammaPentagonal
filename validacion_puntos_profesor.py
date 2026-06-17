"""
Validación Específica del Criptosistema Γ-Pentagonal
con Puntos y Valores del Profesor

Este script valida:
1. Asignación correcta de valores n(j,i) = 2i + j
2. Composiciones como suma de cuadrados
3. Trayectorias en puntos específicos del profesor
"""

from gamma_pentagonal_cryptosystem import GammaPentagonalCryptosystem
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle
import numpy as np


class ValidadorEspecifico:
    """Validador de ejemplos específicos del profesor"""
    
    def __init__(self):
        self.crypto = GammaPentagonalCryptosystem(grid_size=20)
    
    # ========== 1. VALIDACIÓN DE PUNTOS Y VALORES n ==========
    
    def validar_puntos_ejemplo(self):
        """
        Valida que los puntos del profesor dan los valores n correctos
        """
        print("\n" + "=" * 80)
        print("1. VALIDACIÓN DE PUNTOS Y VALORES n(j,i)".center(80))
        print("=" * 80)
        
        puntos_profesor = [
            ((1, 1), 3, "1²+1²+1²"),
            ((1, 4), 9, "3²"),
            ((3, 3), 9, "3² (o 2²+2²+1²)"),
            ((5, 2), 9, "3² (o 2²+2²+1²)"),
        ]
        
        print("\n📍 Fórmula: n(j,i) = 2i + j\n")
        print(f"{'Punto (j,i)':>15} {'Cálculo':>25} {'Valor n':>10} {'Esperado':>10} {'Status':>10}")
        print("-" * 80)
        
        all_correct = True
        for (j, i), expected_n, description in puntos_profesor:
            calculated_n = self.crypto.n_function(j, i)
            calculation = f"2({i}) + {j} = {2*i} + {j}"
            
            is_correct = calculated_n == expected_n
            status = "✓ CORRECTO" if is_correct else "✗ ERROR"
            all_correct = all_correct and is_correct
            
            print(f"({j:1},{i:1}){'':<10} {calculation:>25} {calculated_n:>10} {expected_n:>10} {status:>10}")
        
        print("-" * 80)
        if all_correct:
            print("✅ Todos los puntos validan correctamente\n")
        else:
            print("❌ Hay errores en la validación\n")
        
        return all_correct
    
    # ========== 2. ANÁLISIS DE COMPOSICIONES DE CUADRADOS ==========
    
    def analizar_composiciones(self, n_values=[3, 5, 6, 9]):
        """
        Analiza las composiciones de cuadrados para valores n específicos
        """
        print("\n" + "=" * 80)
        print("2. COMPOSICIONES COMO SUMA DE CUADRADOS".center(80))
        print("=" * 80)
        
        print("\n📊 Descomposiciones de n como suma de a lo más 3 cuadrados\n")
        
        for n in n_values:
            print(f"{'─' * 80}")
            print(f"n = {n}:")
            print(f"  Fórmula: n = a² + b² + c²  (donde a,b,c ≥ 0)\n")
            
            # Genera todas las composiciones
            composiciones = []
            squares = [i*i for i in range(int(np.sqrt(n)) + 1)]
            
            # Un cuadrado
            for sq in squares:
                if sq == n:
                    composiciones.append(f"  • {n} = {int(np.sqrt(sq))}²")
            
            # Dos cuadrados
            for sq1 in squares:
                for sq2 in squares:
                    if sq1 + sq2 == n and sq1 <= sq2:
                        a = int(np.sqrt(sq1))
                        b = int(np.sqrt(sq2))
                        if sq1 > 0 and sq2 > 0:
                            composiciones.append(f"  • {n} = {a}² + {b}² = {sq1} + {sq2}")
            
            # Tres cuadrados
            for sq1 in squares:
                for sq2 in squares:
                    for sq3 in squares:
                        if sq1 + sq2 + sq3 == n and sq1 <= sq2 <= sq3:
                            a = int(np.sqrt(sq1))
                            b = int(np.sqrt(sq2))
                            c = int(np.sqrt(sq3))
                            if sq1 > 0 and sq2 > 0 and sq3 > 0:
                                if (sq1, sq2, sq3) not in [(s1, s2, s3) for s1, s2, s3 in 
                                                           [(int(np.sqrt(x))**2, int(np.sqrt(y))**2, int(np.sqrt(z))**2) 
                                                            for x, y, z in squares for sq in squares]]:
                                    composiciones.append(f"  • {n} = {a}² + {b}² + {c}² = {sq1} + {sq2} + {sq3}")
            
            # Eliminar duplicados
            composiciones = list(set(composiciones))
            
            if composiciones:
                for comp in sorted(composiciones)[:10]:  # Mostrar primeras 10
                    print(comp)
                if len(composiciones) > 10:
                    print(f"  ... y {len(composiciones) - 10} más")
            
            alpha_val = self.crypto.alpha(n % 10, (n // 10) % 10)  # Usar punto equivalente
            print(f"\n  α(para n={n}): {self.crypto.count_square_partitions(n, max_squares=3)} composiciones")
        
        print(f"\n{'─' * 80}\n")
    
    # ========== 3. ANÁLISIS DE PUNTOS DEL PROFESOR ==========
    
    def analizar_puntos_profesor(self):
        """
        Analiza los puntos específicos mencionados en las gráficas
        """
        print("\n" + "=" * 80)
        print("3. PUNTOS ESPECÍFICOS DE LAS GRÁFICAS DEL PROFESOR".center(80))
        print("=" * 80)
        
        puntos_graficas = [
            ((6, 4), "Tipo I y II"),
            ((7, 6), "Tipo I y II"),
            ((6, 7), "Tipo III"),
        ]
        
        print("\n🎯 Análisis detallado de los puntos en las gráficas:\n")
        
        for (j, i), tipo in puntos_graficas:
            n_val = self.crypto.n_function(j, i)
            alpha_val = self.crypto.alpha(j, i)
            equiv_class = self.crypto.get_equivalence_class(n_val)
            
            print(f"{'─' * 80}")
            print(f"Punto v({j},{i}) - Trayectorias de {tipo}:")
            print(f"  n({j},{i}) = 2({i}) + {j} = {n_val}")
            print(f"  α({j},{i}) = {alpha_val}")
            print(f"  Clase de equivalencia C_{n_val}: {sorted(list(equiv_class))}")
            
            # Trayectorias
            type_i = self.crypto.get_type_i_paths(j, i)
            type_ii = self.crypto.get_type_ii_paths(j, i)
            type_iii = self.crypto.get_type_iii_paths(j, i)
            
            print(f"\n  Trayectorias disponibles:")
            print(f"    • Tipo I:   {len(type_i):3} trayectorias")
            print(f"    • Tipo II:  {len(type_ii):3} trayectorias")
            print(f"    • Tipo III: {len(type_iii):3} trayectorias")
            print(f"    ───────────────────")
            print(f"    • TOTAL:    {len(type_i) + len(type_ii) + len(type_iii):3} trayectorias")
            
            # Mostrar primeras trayectorias
            print(f"\n  Primeras trayectorias Tipo I:")
            for idx, path in enumerate(type_i[:3], 1):
                path_str = " → ".join([f"({p[0]},{p[1]})" for p in path])
                print(f"    {idx}. {path_str}")
            if len(type_i) > 3:
                print(f"    ... y {len(type_i) - 3} más")
        
        print(f"\n{'─' * 80}\n")
    
    # ========== 4. VISUALIZACIÓN DE PUNTOS ==========
    
    def visualizar_puntos_profesor(self):
        """
        Crea una visualización similar a la del profesor
        """
        print("\n" + "=" * 80)
        print("4. GENERANDO VISUALIZACIONES".center(80))
        print("=" * 80)
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 14))
        
        # ========== Gráfica 1: Puntos de Ejemplo ==========
        ax = axes[0, 0]
        
        # Dibuja grilla
        for i in range(6):
            for j in range(8):
                ax.plot(j, i, 'o', color='lightblue', markersize=8)
        
        # Puntos del profesor
        puntos_especiales = [
            ((1, 1), 3, "red"),
            ((1, 4), 9, "blue"),
            ((3, 3), 9, "green"),
            ((5, 2), 9, "purple"),
        ]
        
        for (j, i), n_val, color in puntos_especiales:
            ax.plot(j, i, 'o', color=color, markersize=15, label=f"({j},{i}): n={n_val}")
            ax.text(j+0.2, i+0.2, f"n={n_val}", fontsize=10, fontweight='bold')
        
        ax.set_xlabel('j (columna)', fontsize=12, fontweight='bold')
        ax.set_ylabel('i (fila)', fontsize=12, fontweight='bold')
        ax.set_title('Puntos de Ejemplo con Valores n(j,i)', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)
        ax.set_xlim(-0.5, 7.5)
        ax.set_ylim(-0.5, 5.5)
        
        # ========== Gráfica 2: Puntos de Trayectorias Tipo I y II ==========
        ax = axes[0, 1]
        
        # Dibuja grilla
        for i in range(8):
            for j in range(9):
                ax.plot(j, i, 'o', color='lightgray', markersize=6, alpha=0.5)
        
        # Puntos especiales
        puntos_tipos = [
            ((6, 4), "Tipo I/II", "red"),
            ((7, 6), "Tipo I/II", "blue"),
        ]
        
        for (j, i), tipo, color in puntos_tipos:
            n_val = self.crypto.n_function(j, i)
            alpha_val = self.crypto.alpha(j, i)
            
            ax.plot(j, i, 'o', color=color, markersize=15)
            ax.text(j+0.3, i+0.3, f"({j},{i})\nn={n_val}\nα={alpha_val}", 
                   fontsize=9, fontweight='bold', bbox=dict(boxstyle='round', 
                   facecolor=color, alpha=0.3))
            
            # Dibuja algunas trayectorias
            type_i = self.crypto.get_type_i_paths(j, i)
            for path in type_i[:2]:  # Primeras 2
                path_array = np.array(path)
                ax.plot(path_array[:, 0], path_array[:, 1], 'o-', 
                       color=color, alpha=0.5, linewidth=1.5)
        
        ax.set_xlabel('j (columna)', fontsize=12, fontweight='bold')
        ax.set_ylabel('i (fila)', fontsize=12, fontweight='bold')
        ax.set_title('Puntos de Trayectorias Tipo I y II', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-0.5, 8.5)
        ax.set_ylim(-0.5, 7.5)
        
        # ========== Gráfica 3: Punto de Trayectorias Tipo III ==========
        ax = axes[1, 0]
        
        # Dibuja grilla
        for i in range(9):
            for j in range(9):
                ax.plot(j, i, 'o', color='lightgray', markersize=6, alpha=0.5)
        
        j, i = 6, 7
        n_val = self.crypto.n_function(j, i)
        alpha_val = self.crypto.alpha(j, i)
        
        ax.plot(j, i, 'o', color='darkgreen', markersize=18)
        ax.text(j+0.4, i+0.4, f"({j},{i})\nTipo III\nn={n_val}\nα={alpha_val}", 
               fontsize=10, fontweight='bold', bbox=dict(boxstyle='round', 
               facecolor='green', alpha=0.3))
        
        # Dibuja origen
        ax.plot(0, 0, 's', color='black', markersize=12, label='Origen (0,0)')
        
        # Dibuja algunas trayectorias Tipo III
        type_iii = self.crypto.get_type_iii_paths(j, i)
        for idx, path in enumerate(type_iii[:3]):
            path_array = np.array(path)
            ax.plot(path_array[:, 0], path_array[:, 1], 'o--', 
                   color=plt.cm.Greens(0.3 + idx*0.2), alpha=0.7, linewidth=2, 
                   label=f'Ruta {idx+1}')
        
        ax.set_xlabel('j (columna)', fontsize=12, fontweight='bold')
        ax.set_ylabel('i (fila)', fontsize=12, fontweight='bold')
        ax.set_title(f'Trayectorias Tipo III a ({j},{i})', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=9)
        ax.set_xlim(-0.5, 8.5)
        ax.set_ylim(-0.5, 8.5)
        
        # ========== Gráfica 4: Comparación de Valores α ==========
        ax = axes[1, 1]
        
        # Calcula α para rango de puntos
        n_values = []
        alpha_values = []
        
        for i in range(0, 5):
            for j in range(0, 5):
                n = self.crypto.n_function(j, i)
                alpha = self.crypto.alpha(j, i)
                n_values.append(n)
                alpha_values.append(alpha)
        
        # Gráfica de dispersión
        unique_n = sorted(set(n_values))
        unique_alpha = [self.crypto.count_square_partitions(n, max_squares=3) for n in unique_n]
        
        ax.plot(unique_n, unique_alpha, 'bo-', linewidth=2, markersize=8, label='α(n)')
        ax.fill_between(unique_n, unique_alpha, alpha=0.2)
        
        # Marca puntos especiales del profesor
        special_points = [(3, 3), (9, self.crypto.count_square_partitions(9, max_squares=3))]
        for n, alpha in special_points:
            ax.plot(n, alpha, 'r*', markersize=20)
        
        ax.set_xlabel('n = 2i + j', fontsize=12, fontweight='bold')
        ax.set_ylabel('α(n) - Número de composiciones', fontsize=12, fontweight='bold')
        ax.set_title('Distribución de α según n', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)
        
        plt.tight_layout()
        plt.savefig('validacion_puntos_profesor.png', dpi=150, bbox_inches='tight')
        print("\n✓ Gráfica guardada como 'validacion_puntos_profesor.png'")
        plt.show()
    
    # ========== 5. TABLA RESUMIDA ==========
    
    def tabla_resumen(self):
        """
        Crea una tabla de resumen de todos los valores
        """
        print("\n" + "=" * 80)
        print("5. TABLA RESUMEN DE VALIDACIÓN".center(80))
        print("=" * 80)
        
        print("\n📋 Resumen de Puntos del Profesor:\n")
        
        puntos_total = [
            ((1, 1), "Ejemplo básico"),
            ((1, 4), "Equivalente a (3,3) y (5,2)"),
            ((3, 3), "Equivalente a (1,4) y (5,2)"),
            ((5, 2), "Equivalente a (1,4) y (3,3)"),
            ((6, 4), "Trayectorias Tipo I y II"),
            ((7, 6), "Trayectorias Tipo I y II"),
            ((6, 7), "Trayectorias Tipo III"),
        ]
        
        print(f"{'Punto (j,i)':>15} {'n(j,i)':>10} {'α(j,i)':>10} {'Clase':>30} {'Descripción':>20}")
        print("-" * 90)
        
        for (j, i), descripcion in puntos_total:
            n_val = self.crypto.n_function(j, i)
            alpha_val = self.crypto.alpha(j, i)
            equiv_class = sorted(list(self.crypto.get_equivalence_class(n_val)))
            
            # Formatea clase
            class_str = str(equiv_class)[:28]
            
            print(f"({j:1},{i:1}){'':<10} {n_val:>10} {alpha_val:>10} {class_str:>30} {descripcion:>20}")
        
        print("-" * 90)
        print()


def main():
    """Función principal"""
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + "VALIDACIÓN ESPECÍFICA DEL CRIPTOSISTEMA Γ-PENTAGONAL".center(78) + "║")
    print("║" + "Con Puntos y Ejemplos del Profesor".center(78) + "║")
    print("╚" + "═" * 78 + "╝")
    
    validador = ValidadorEspecifico()
    
    # Ejecuta todas las validaciones
    validador.validar_puntos_ejemplo()
    
    validador.analizar_composiciones(n_values=[3, 5, 6, 9])
    
    validador.analizar_puntos_profesor()
    
    validador.tabla_resumen()
    
    print("\n" + "=" * 80)
    print("GENERANDO VISUALIZACIONES".center(80))
    print("=" * 80)
    validador.visualizar_puntos_profesor()
    
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + "✅ VALIDACIÓN COMPLETADA EXITOSAMENTE".center(78) + "║")
    print("╚" + "═" * 78 + "╝\n")


if __name__ == "__main__":
    main()
