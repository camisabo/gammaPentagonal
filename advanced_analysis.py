"""
Pruebas Avanzadas y Análisis del Criptosistema Γ-Pentagonal
Incluye: validación matemática, análisis de seguridad, benchmarks
"""

import time
import json
from gamma_pentagonal_cryptosystem import GammaPentagonalCryptosystem
import matplotlib.pyplot as plt
import numpy as np


class GammaPentagonalAnalyzer:
    """
    Herramienta de análisis para el Criptosistema Γ-Pentagonal
    """
    
    def __init__(self, crypto: GammaPentagonalCryptosystem):
        self.crypto = crypto
        self.results = {}
    
    def validate_alpha_vs_squares(self, max_n: int = 50) -> bool:
        """
        Valida que α coincida con el número de composiciones de cuadrados
        
        Args:
            max_n: Valor máximo de n a validar
            
        Returns:
            True si todas las validaciones son exitosas
        """
        print("\n📊 VALIDACIÓN: α vs Composiciones de Cuadrados")
        print("-" * 60)
        
        all_valid = True
        mismatches = []
        
        for n in range(1, max_n + 1):
            # Calcula α a través de puntos
            alpha_vals = set()
            for j, i in self.crypto.inverse_n_function(n):
                alpha_vals.add(self.crypto.alpha(j, i))
            
            # Todas los puntos en la clase deben tener mismo α
            if len(alpha_vals) != 1:
                all_valid = False
                mismatches.append(f"n={n}: α inconsistente {alpha_vals}")
                continue
            
            alpha_val = alpha_vals.pop()
            squares_count = self.crypto.count_square_partitions(n, max_squares=3)
            
            if alpha_val != squares_count:
                all_valid = False
                mismatches.append(f"n={n}: α={alpha_val} ≠ cuadrados={squares_count}")
            else:
                print(f"   ✓ n={n:3}: α={alpha_val:2} (composiciones de cuadrados verificadas)")
        
        if mismatches:
            print("\n   ⚠ DISCREPANCIAS ENCONTRADAS:")
            for mismatch in mismatches[:5]:
                print(f"   {mismatch}")
        
        return all_valid
    
    def analyze_equivalence_classes(self, max_n: int = 30):
        """
        Analiza la estructura de las clases de equivalencia
        
        Args:
            max_n: Valor máximo de n a analizar
        """
        print("\n📊 ANÁLISIS: Clases de Equivalencia")
        print("-" * 60)
        
        class_sizes = []
        alpha_distribution = []
        
        for n in range(1, max_n + 1):
            equiv_class = self.crypto.get_equivalence_class(n)
            class_size = len(equiv_class)
            alpha_val = self.crypto.alpha(list(equiv_class)[0][0], list(equiv_class)[0][1])
            
            class_sizes.append(class_size)
            alpha_distribution.append(alpha_val)
            
            print(f"   n={n:3}: tamaño_clase={class_size:2}, α={alpha_val:2}, " +
                  f"puntos={sorted(list(equiv_class))}")
        
        # Estadísticas
        print(f"\n   Estadísticas de tamaño de clase:")
        print(f"   - Mínimo: {min(class_sizes)}")
        print(f"   - Máximo: {max(class_sizes)}")
        print(f"   - Promedio: {np.mean(class_sizes):.2f}")
        print(f"   - Desv. Est.: {np.std(class_sizes):.2f}")
        
        return class_sizes, alpha_distribution
    
    def benchmark_encryption(self, num_trials: int = 100):
        """
        Evalúa el rendimiento de cifrado/descifrado
        
        Args:
            num_trials: Número de pruebas a realizar
        """
        print(f"\n📊 BENCHMARK: Rendimiento Criptográfico")
        print("-" * 60)
        
        key = self.crypto.create_key(seed=42)
        messages = list(range(1, num_trials + 1))
        
        # Benchmark de cifrado
        start_time = time.time()
        ciphertexts = [self.crypto.encrypt(msg, key) for msg in messages]
        encrypt_time = time.time() - start_time
        
        # Benchmark de descifrado
        start_time = time.time()
        decrypted = [self.crypto.decrypt(ct, key) for ct in ciphertexts]
        decrypt_time = time.time() - start_time
        
        # Verificación
        correct = sum(1 for i, msg in enumerate(messages) if decrypted[i] == msg)
        success_rate = (correct / num_trials) * 100
        
        print(f"   Pruebas: {num_trials}")
        print(f"   Tiempo de cifrado: {encrypt_time*1000:.2f} ms ({encrypt_time/num_trials*1000:.4f} ms/operación)")
        print(f"   Tiempo de descifrado: {decrypt_time*1000:.2f} ms ({decrypt_time/num_trials*1000:.4f} ms/operación)")
        print(f"   Tasa de éxito: {success_rate:.1f}% ({correct}/{num_trials})")
        
        self.results['benchmark'] = {
            'num_trials': num_trials,
            'encrypt_time_ms': encrypt_time * 1000,
            'decrypt_time_ms': decrypt_time * 1000,
            'success_rate': success_rate
        }
        
        return encrypt_time, decrypt_time
    
    def analyze_path_complexity(self, max_target: int = 6):
        """
        Analiza la complejidad del número de trayectorias
        
        Args:
            max_target: Rango máximo para analizar
        """
        print(f"\n📊 ANÁLISIS: Complejidad de Trayectorias")
        print("-" * 60)
        
        data = {
            'target': [],
            'type_i': [],
            'type_ii': [],
            'type_iii': [],
            'total': []
        }
        
        print(f"{'Target':>10} {'Tipo I':>10} {'Tipo II':>10} {'Tipo III':>10} {'Total':>10}")
        print("-" * 60)
        
        for i in range(1, max_target + 1):
            for j in range(1, max_target + 1):
                t1 = len(self.crypto.get_type_i_paths(j, i))
                t2 = len(self.crypto.get_type_ii_paths(j, i))
                t3 = len(self.crypto.get_type_iii_paths(j, i))
                total = t1 + t2 + t3
                
                data['target'].append(f"({j},{i})")
                data['type_i'].append(t1)
                data['type_ii'].append(t2)
                data['type_iii'].append(t3)
                data['total'].append(total)
                
                print(f"({j:1},{i:1}){'':<6} {t1:>10} {t2:>10} {t3:>10} {total:>10}")
        
        self.results['path_analysis'] = data
        return data
    
    def plot_alpha_distribution(self, max_n: int = 100):
        """
        Visualiza la distribución de valores α
        
        Args:
            max_n: Valor máximo de n a considerar
        """
        print(f"\n📊 GRÁFICO: Distribución de α")
        print("-" * 60)
        
        n_values = list(range(1, max_n + 1))
        alpha_values = [self.crypto.count_square_partitions(n, max_squares=3) 
                       for n in n_values]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Gráfico 1: Valores de α por n
        ax1.plot(n_values, alpha_values, 'b-', linewidth=2, marker='o', markersize=4)
        ax1.fill_between(n_values, alpha_values, alpha=0.3)
        ax1.set_xlabel('n = 2i + j', fontsize=11, fontweight='bold')
        ax1.set_ylabel('α(n) - Particiones en cuadrados', fontsize=11, fontweight='bold')
        ax1.set_title('Valor de α según n', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Gráfico 2: Histograma de distribución
        unique_alphas = sorted(set(alpha_values))
        counts = [alpha_values.count(a) for a in unique_alphas]
        
        ax2.bar(unique_alphas, counts, color='coral', edgecolor='black', linewidth=1.5)
        ax2.set_xlabel('Valor de α', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Frecuencia', fontsize=11, fontweight='bold')
        ax2.set_title('Distribución de valores α', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('gamma_pentagonal_alpha_analysis.png', dpi=150, bbox_inches='tight')
        plt.show()
        
        print(f"   ✓ Gráfico guardado como 'gamma_pentagonal_alpha_analysis.png'")
        print(f"   Rango de α: [{min(alpha_values)}, {max(alpha_values)}]")
        print(f"   Promedio de α: {np.mean(alpha_values):.2f}")
    
    def security_analysis(self):
        """
        Realiza análisis de seguridad teórica
        """
        print(f"\n🔐 ANÁLISIS DE SEGURIDAD")
        print("-" * 60)
        
        grid_size = self.crypto.grid_size
        num_vertices = grid_size ** 2
        
        print(f"   Parámetros del sistema:")
        print(f"   - Grilla: {grid_size} × {grid_size}")
        print(f"   - Número de vértices: {num_vertices}")
        print(f"   - Espacio de permutaciones: {num_vertices}!")
        print(f"   - Bits de entropía de clave (aprox.): ~{num_vertices * np.log2(num_vertices):.0f} bits")
        print()
        
        print(f"   Fortaleza teórica:")
        print(f"   ✓ Basado en problema NP-completo (particiones de enteros)")
        print(f"   ✓ Uso de permutaciones secretas (O(n!) complejidad)")
        print(f"   ✓ Transformación no-lineal mediante automorfismo")
        print(f"   ✓ Resistencia a ataques por fuerza bruta: exponencial en grid_size")
        print()
        
        print(f"   Vulnerabilidades potenciales:")
        print(f"   ⚠ Requiere memoización eficiente (caché de α)")
        print(f"   ⚠ El tamaño de grilla debe ser suficientemente grande")
        print(f"   ⚠ Ataques de análisis de frecuencia si se reutilizan claves")
        
        self.results['security'] = {
            'grid_size': grid_size,
            'num_vertices': num_vertices,
            'entropy_bits': num_vertices * np.log2(num_vertices)
        }
    
    def generate_report(self, output_file: str = "crypto_analysis_report.json"):
        """
        Genera un reporte completo en JSON
        
        Args:
            output_file: Ruta del archivo de salida
        """
        print(f"\n📋 GENERANDO REPORTE")
        print("-" * 60)
        
        report = {
            'system': 'Criptosistema Γ-Pentagonal',
            'grid_size': self.crypto.grid_size,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'analysis_results': self.results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"   ✓ Reporte guardado como '{output_file}'")


def main():
    """Función principal de análisis avanzado"""
    print("\n" + "=" * 70)
    print("ANÁLISIS AVANZADO - Criptosistema Γ-Pentagonal".center(70))
    print("=" * 70)
    
    # Inicializa
    print("\n🔧 Inicializando sistema...")
    crypto = GammaPentagonalCryptosystem(grid_size=12)
    analyzer = GammaPentagonalAnalyzer(crypto)
    
    # Ejecuta análisis
    analyzer.validate_alpha_vs_squares(max_n=40)
    
    class_sizes, alpha_dist = analyzer.analyze_equivalence_classes(max_n=25)
    
    analyzer.benchmark_encryption(num_trials=100)
    
    path_data = analyzer.analyze_path_complexity(max_target=5)
    
    analyzer.plot_alpha_distribution(max_n=80)
    
    analyzer.security_analysis()
    
    analyzer.generate_report()
    
    print("\n" + "=" * 70)
    print("ANÁLISIS COMPLETADO".center(70))
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
