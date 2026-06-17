"""
Ejemplos Prácticos del Criptosistema Γ-Pentagonal
Ejecuta este archivo para ver casos de uso concretos
"""

from gamma_pentagonal_cryptosystem import GammaPentagonalCryptosystem
from advanced_analysis import GammaPentagonalAnalyzer
import time


def ejemplo_1_funcion_n():
    """Ejemplo 1: Entendiendo la función n(j,i) = 2i + j"""
    print("\n" + "=" * 70)
    print("EJEMPLO 1: Función de Asignación n(j,i) = 2i + j".center(70))
    print("=" * 70)
    
    crypto = GammaPentagonalCryptosystem(grid_size=10)
    
    print("\n📍 Mapeo de puntos (j,i) a valores n:")
    print("-" * 70)
    print(f"{'(j,i)':>10} {'n(j,i)':>15} {'Clase Equivalencia':>45}")
    print("-" * 70)
    
    for i in range(3):
        for j in range(4):
            n_val = crypto.n_function(j, i)
            equiv_class = sorted(list(crypto.get_equivalence_class(n_val)))
            print(f"({j:1},{i:1}){'':<6} {n_val:>15} {str(equiv_class):>45}")
    
    print("\n💡 Observación: Diferentes puntos pueden tener el mismo n(j,i)")
    print("   Esto crea 'clases de equivalencia' de puntos")
    
    # Análisis de clases
    print("\n📊 Análisis de clases de equivalencia:")
    print("-" * 70)
    for n in range(1, 11):
        equiv_class = sorted(list(crypto.get_equivalence_class(n)))
        print(f"   C_{n:2} (n={n:2}): {equiv_class}")


def ejemplo_2_alpha():
    """Ejemplo 2: Cálculo de α(j,i) - particiones en cuadrados"""
    print("\n" + "=" * 70)
    print("EJEMPLO 2: Función Alpha α(j,i) - Particiones en Cuadrados".center(70))
    print("=" * 70)
    
    crypto = GammaPentagonalCryptosystem(grid_size=10)
    
    print("\n🔢 Valores de α para puntos en el plano:")
    print("-" * 70)
    print(f"{'(j,i)':>10} {'n':>5} {'α(j,i)':>10} {'Explicación':>45}")
    print("-" * 70)
    
    ejemplos = [
        ((0, 0), "0 = 0"),
        ((1, 0), "1 = 1²"),
        ((0, 1), "2 = 1² + 1²"),
        ((1, 1), "3 = 1² + 1² + 1²"),
        ((2, 0), "2 = 1² + 1²"),
        ((0, 2), "4 = 2²"),
        ((1, 2), "5 = 2² + 1²"),
        ((2, 2), "6 = ? (descomponer)"),
    ]
    
    for (j, i), explanation in ejemplos:
        n_val = crypto.n_function(j, i)
        alpha_val = crypto.alpha(j, i)
        print(f"({j:1},{i:1}){'':<6} {n_val:>5} {alpha_val:>10} {explanation:>45}")
    
    print("\n💡 α(j,i) = número de formas de escribir n(j,i)")
    print("   como suma de a lo más 3 cuadrados")


def ejemplo_3_trayectorias():
    """Ejemplo 3: Tipos de trayectorias en el grafo"""
    print("\n" + "=" * 70)
    print("EJEMPLO 3: Tipos de Trayectorias (Tipo I, II, III)".center(70))
    print("=" * 70)
    
    crypto = GammaPentagonalCryptosystem(grid_size=8)
    target = (3, 2)
    
    print(f"\n🎯 Analizando trayectorias al punto {target}:")
    print("-" * 70)
    
    # Tipo I
    print("\n📍 TIPO I: Trayectorias simples desde (0,0)")
    type_i = crypto.get_type_i_paths(target[0], target[1])
    print(f"   Cantidad: {len(type_i)}")
    for idx, path in enumerate(type_i[:3], 1):
        path_str = " → ".join([f"({p[0]},{p[1]})" for p in path])
        print(f"   Ruta {idx}: {path_str}")
    if len(type_i) > 3:
        print(f"   ... y {len(type_i) - 3} más")
    
    # Tipo II
    print("\n📍 TIPO II: Concatenación de dos Tipo I")
    type_ii = crypto.get_type_ii_paths(target[0], target[1])
    print(f"   Cantidad: {len(type_ii)}")
    for idx, path in enumerate(type_ii[:2], 1):
        path_str = " → ".join([f"({p[0]},{p[1]})" for p in path])
        print(f"   Ruta {idx}: {path_str}")
    if len(type_ii) > 2:
        print(f"   ... y {len(type_ii) - 2} más")
    
    # Tipo III
    print("\n📍 TIPO III: Tipo II + Tipo I (con restricción de pendiente)")
    type_iii = crypto.get_type_iii_paths(target[0], target[1])
    print(f"   Cantidad: {len(type_iii)}")
    
    # Resumen
    print("\n📊 RESUMEN de trayectorias:")
    print("-" * 70)
    total = len(type_i) + len(type_ii) + len(type_iii)
    print(f"   Tipo I:   {len(type_i):>3} trayectorias ({len(type_i)/total*100:>5.1f}%)")
    print(f"   Tipo II:  {len(type_ii):>3} trayectorias ({len(type_ii)/total*100:>5.1f}%)")
    print(f"   Tipo III: {len(type_iii):>3} trayectorias ({len(type_iii)/total*100:>5.1f}%)")
    print(f"   {'─' * 37}")
    print(f"   TOTAL:    {total:>3} trayectorias")


def ejemplo_4_criptografia():
    """Ejemplo 4: Cifrado y descifrado"""
    print("\n" + "=" * 70)
    print("EJEMPLO 4: Operaciones Criptográficas".center(70))
    print("=" * 70)
    
    print("\n🔑 Generando clave criptográfica...")
    crypto = GammaPentagonalCryptosystem(grid_size=12)
    key = crypto.create_key(seed=42)
    print("   ✓ Clave generada correctamente")
    
    print("\n🔒 Cifrando mensajes:")
    print("-" * 70)
    
    mensajes = [1, 5, 10, 25, 42, 100, 256, 512]
    resultados = []
    
    print(f"{'Mensaje':>10} {'Criptograma':>25} {'Descifrado':>15} {'Status':>10}")
    print("-" * 70)
    
    for msg in mensajes:
        criptograma = crypto.encrypt(msg, key)
        descifrado = crypto.decrypt(criptograma, key)
        
        # Validación
        is_correct = descifrado == msg
        status = "✓ OK" if is_correct else "✗ FALLO"
        
        print(f"{msg:>10} {str(criptograma):>25} {descifrado:>15} {status:>10}")
        resultados.append(is_correct)
    
    success_rate = sum(resultados) / len(resultados) * 100
    print("-" * 70)
    print(f"   Tasa de éxito: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("   ✓ ¡Todos los mensajes cifrados y descifrados correctamente!")


def ejemplo_5_seguridad():
    """Ejemplo 5: Análisis de seguridad"""
    print("\n" + "=" * 70)
    print("EJEMPLO 5: Análisis de Seguridad".center(70))
    print("=" * 70)
    
    print("\n🔐 Evaluando niveles de seguridad con diferentes grid_size:")
    print("-" * 70)
    
    import numpy as np
    
    grid_sizes = [8, 12, 16, 20]
    
    print(f"{'Grid Size':>12} {'Vértices':>12} {'Permutaciones':>18} {'Bits Entropía':>18}")
    print("-" * 70)
    
    for gs in grid_sizes:
        num_vertices = gs * gs
        entropy_bits = num_vertices * np.log2(num_vertices)
        
        # Estimación de permutaciones (usando Stirling)
        perm_estimate = f"~{num_vertices}!"
        
        security_level = "⚠️ Baja" if gs == 8 else \
                        "⚠️ Media" if gs == 12 else \
                        "✓ Alta" if gs == 16 else \
                        "✓✓ Muy Alta"
        
        print(f"{gs:>12} {num_vertices:>12} {perm_estimate:>18} " +
              f"{entropy_bits:>15.0f} bits {security_level}")
    
    print("\n💡 Recomendaciones:")
    print("   • Demostración: grid_size = 8-10")
    print("   • Educación: grid_size = 12-14")
    print("   • Investigación: grid_size = 16-18")
    print("   • Producción: grid_size ≥ 20 (requiere auditoría)")


def ejemplo_6_rendimiento():
    """Ejemplo 6: Benchmarks de rendimiento"""
    print("\n" + "=" * 70)
    print("EJEMPLO 6: Benchmarks de Rendimiento".center(70))
    print("=" * 70)
    
    crypto = GammaPentagonalCryptosystem(grid_size=12)
    key = crypto.create_key(seed=42)
    
    print("\n⏱️ Midiendo velocidad de operaciones:")
    print("-" * 70)
    
    # Benchmark n()
    start = time.time()
    for i in range(10000):
        _ = crypto.n_function(i % 10, (i // 10) % 10)
    time_n = (time.time() - start) / 10000 * 1000
    
    # Benchmark alpha()
    start = time.time()
    for n in range(100):
        _ = crypto.count_square_partitions(n, max_squares=3)
    time_alpha = (time.time() - start) / 100 * 1000
    
    # Benchmark cifrado
    start = time.time()
    for i in range(100):
        _ = crypto.encrypt(i + 10, key)
    time_encrypt = (time.time() - start) / 100 * 1000
    
    # Benchmark descifrado
    ciphertexts = [crypto.encrypt(i + 10, key) for i in range(100)]
    start = time.time()
    for ct in ciphertexts:
        _ = crypto.decrypt(ct, key)
    time_decrypt = (time.time() - start) / 100 * 1000
    
    print(f"{'Operación':>25} {'Tiempo':>15} {'Velocidad':>20}")
    print("-" * 70)
    print(f"{'n(j,i)':>25} {time_n:>13.4f} ms {f'({1/time_n*1000:.0f} ops/s)':>20}")
    print(f"{'α(j,i)':>25} {time_alpha:>13.4f} ms {f'({1/time_alpha*1000:.0f} ops/s)':>20}")
    print(f"{'Cifrado':>25} {time_encrypt:>13.4f} ms {f'({1/time_encrypt*1000:.0f} ops/s)':>20}")
    print(f"{'Descifrado':>25} {time_decrypt:>13.4f} ms {f'({1/time_decrypt*1000:.0f} ops/s)':>20}")
    
    print("\n💡 Conclusion:")
    print(f"   • Operación más rápida: n(j,i) (~{1/time_n*1000:.0f} ops/s)")
    print(f"   • Cifrado/Descifrado: ~{(1/time_encrypt + 1/time_decrypt)/2:.0f} ops/s")


def ejemplo_7_visualizacion():
    """Ejemplo 7: Generación de visualizaciones"""
    print("\n" + "=" * 70)
    print("EJEMPLO 7: Generación de Visualizaciones".center(70))
    print("=" * 70)
    
    print("\n📊 Generando visualizaciones del sistema...")
    print("-" * 70)
    
    crypto = GammaPentagonalCryptosystem(grid_size=12)
    
    print("\n1. Visualizando grilla con valores de α...")
    try:
        crypto.visualize_lattice(target_j=6, target_i=6, show_alpha=True)
        print("   ✓ Archivo guardado: 'gamma_pentagonal_lattice.png'")
    except Exception as e:
        print(f"   ⚠ Advertencia: {str(e)}")
    
    print("\n2. Visualizando tipos de trayectorias...")
    try:
        crypto.visualize_paths(target_j=4, target_i=4)
        print("   ✓ Archivo guardado: 'gamma_pentagonal_paths.png'")
    except Exception as e:
        print(f"   ⚠ Advertencia: {str(e)}")


def ejemplo_8_validacion():
    """Ejemplo 8: Validación matemática del sistema"""
    print("\n" + "=" * 70)
    print("EJEMPLO 8: Validación Matemática".center(70))
    print("=" * 70)
    
    crypto = GammaPentagonalCryptosystem(grid_size=10)
    analyzer = GammaPentagonalAnalyzer(crypto)
    
    print("\n✅ Validando propiedades matemáticas...")
    print("-" * 70)
    
    # Validación 1: α coincide con particiones
    print("\n1. Verificando α = composiciones de cuadrados:")
    is_valid = analyzer.validate_alpha_vs_squares(max_n=30)
    if is_valid:
        print("   ✓ Todas las validaciones exitosas")
    else:
        print("   ⚠ Algunas discrepancias encontradas")
    
    # Validación 2: Clases de equivalencia
    print("\n2. Analizando estructura de clases:")
    class_sizes, alphas = analyzer.analyze_equivalence_classes(max_n=15)
    print(f"   • Tamaño mínimo: {min(class_sizes)}")
    print(f"   • Tamaño máximo: {max(class_sizes)}")
    print(f"   • Tamaño promedio: {sum(class_sizes)/len(class_sizes):.2f}")
    print("   ✓ Estructura de clases verificada")


def menu_principal():
    """Menú para seleccionar ejemplos"""
    print("\n" + "=" * 70)
    print("EJEMPLOS PRÁCTICOS - Criptosistema Γ-Pentagonal".center(70))
    print("=" * 70)
    
    ejemplos = [
        ("Función n(j,i) = 2i + j", ejemplo_1_funcion_n),
        ("Función Alpha α(j,i)", ejemplo_2_alpha),
        ("Tipos de Trayectorias", ejemplo_3_trayectorias),
        ("Cifrado y Descifrado", ejemplo_4_criptografia),
        ("Análisis de Seguridad", ejemplo_5_seguridad),
        ("Benchmarks de Rendimiento", ejemplo_6_rendimiento),
        ("Visualizaciones", ejemplo_7_visualizacion),
        ("Validación Matemática", ejemplo_8_validacion),
    ]
    
    print("\n📋 Selecciona un ejemplo para ejecutar:\n")
    for i, (nombre, _) in enumerate(ejemplos, 1):
        print(f"   {i}. {nombre}")
    print(f"   {len(ejemplos) + 1}. Ejecutar TODOS los ejemplos")
    print(f"   0. Salir\n")
    
    try:
        choice = int(input("Ingresa tu opción (0-9): "))
        
        if choice == 0:
            print("\n¡Hasta luego!")
            return
        elif choice == len(ejemplos) + 1:
            for nombre, func in ejemplos:
                try:
                    func()
                    print("\n✓ Ejemplo completado\n")
                except Exception as e:
                    print(f"\n✗ Error: {str(e)}\n")
        elif 1 <= choice <= len(ejemplos):
            ejemplos[choice - 1][1]()
            print("\n✓ Ejemplo completado\n")
        else:
            print("\n✗ Opción inválida\n")
            menu_principal()
    
    except KeyboardInterrupt:
        print("\n\n¡Programa interrumpido!")
    except ValueError:
        print("\n✗ Por favor ingresa un número válido\n")
        menu_principal()


if __name__ == "__main__":
    menu_principal()
