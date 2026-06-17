"""
Análisis Detallado de Composiciones como Suma de Cuadrados
Valida las descomposiciones específicas mencionadas por el profesor
"""

from gamma_pentagonal_cryptosystem import GammaPentagonalCryptosystem
import itertools


class AnalizadorComposiciones:
    """Analizador detallado de composiciones de cuadrados"""
    
    def __init__(self):
        self.crypto = GammaPentagonalCryptosystem(grid_size=15)
    
    def encontrar_composiciones_exactas(self, n, max_terminos=3):
        """
        Encuentra todas las composiciones (sumas donde el orden importa)
        de n como suma de cuadrados
        
        Args:
            n: Número a descomponer
            max_terminos: Máximo número de términos
        
        Returns:
            Lista de composiciones únicas
        """
        composiciones = []
        
        # Obtiene todos los cuadrados hasta n
        cuadrados = []
        k = 0
        while k * k <= n:
            cuadrados.append(k * k)
            k += 1
        
        # Caso 1: Un solo cuadrado
        if 1 <= max_terminos:
            for sq in cuadrados:
                if sq == n and sq > 0:
                    composiciones.append(([int(sq**0.5)], sq))
        
        # Caso 2: Dos cuadrados
        if 2 <= max_terminos:
            for sq1 in cuadrados:
                for sq2 in cuadrados:
                    if sq1 + sq2 == n:
                        a = int(sq1**0.5) if sq1 > 0 else 0
                        b = int(sq2**0.5) if sq2 > 0 else 0
                        if sq1 > 0 and sq2 > 0:
                            composiciones.append(([a, b], sq1 + sq2))
        
        # Caso 3: Tres cuadrados
        if 3 <= max_terminos:
            for sq1 in cuadrados:
                for sq2 in cuadrados:
                    for sq3 in cuadrados:
                        if sq1 + sq2 + sq3 == n:
                            a = int(sq1**0.5) if sq1 > 0 else 0
                            b = int(sq2**0.5) if sq2 > 0 else 0
                            c = int(sq3**0.5) if sq3 > 0 else 0
                            if sq1 > 0 and sq2 > 0 and sq3 > 0:
                                composiciones.append(([a, b, c], sq1 + sq2 + sq3))
        
        # Elimina duplicados (mantiene el orden)
        composiciones_unicas = []
        vistos = set()
        for comp, suma in composiciones:
            # Crea una tupla ordenada para detectar duplicados
            tupla = tuple(sorted(comp))
            if tupla not in vistos and suma == n:
                vistos.add(tupla)
                composiciones_unicas.append(comp)
        
        return composiciones_unicas
    
    def demostrar_composiciones_profesor(self):
        """
        Demuestra las composiciones específicas mencionadas por el profesor
        """
        print("\n" + "=" * 90)
        print("COMPOSICIONES ESPECÍFICAS DEL PROFESOR".center(90))
        print("=" * 90)
        
        ejemplos_profesor = [
            (3, "3 = 1² + 1² + 1²", [1, 1, 1]),
            (5, "5 = 4 + 1 = 2² + 1²", [2, 1]),
            (6, "6 = 4 + 1 + 1 = 2² + 1² + 1²", [2, 1, 1]),
            (9, "9 = 3² (o 2² + 2² + 1²)", [3]),
        ]
        
        print("\n✅ Validación de Ejemplos del Profesor:\n")
        
        for n, formula, componentes in ejemplos_profesor:
            print(f"{'─' * 90}")
            print(f"\n📊 n = {n}: {formula}")
            
            # Verifica la composición
            suma = sum(c**2 for c in componentes)
            is_correct = suma == n
            
            componentes_str = " + ".join([f"{c}²" for c in componentes])
            calculo = " + ".join([str(c**2) for c in componentes])
            
            print(f"\n   Composición: {componentes_str}")
            print(f"   Cálculo: {calculo} = {suma}")
            print(f"   Estado: {'✓ CORRECTO' if is_correct else '✗ INCORRECTO'}")
            
            # Obtiene todas las composiciones para este n
            todas_composiciones = self.encontrar_composiciones_exactas(n, max_terminos=3)
            
            print(f"\n   Todas las composiciones de {n}:")
            for idx, comp in enumerate(todas_composiciones, 1):
                comp_str = " + ".join([f"{c}²" for c in comp])
                comp_sum = " + ".join([str(c**2) for c in comp])
                print(f"   {idx}. {comp_str} = {comp_sum} = {n}")
            
            # Valida con α
            alpha_val = self.crypto.count_square_partitions(n, max_squares=3)
            print(f"\n   α({n}): {alpha_val} composiciones")
    
    def analizar_clases_equivalentes(self):
        """
        Analiza puntos equivalentes y sus composiciones
        """
        print("\n" + "=" * 90)
        print("ANÁLISIS DE CLASES EQUIVALENTES".center(90))
        print("=" * 90)
        
        print("\n📍 Puntos Equivalentes (puntos con el mismo valor n):\n")
        
        # Puntos mencionados por el profesor
        puntos_equivalentes = {
            9: [(1, 4), (3, 3), (5, 2)],
            3: [(1, 1)],
        }
        
        for n, puntos in puntos_equivalentes.items():
            print(f"{'─' * 90}")
            print(f"\nValor n = {n}:")
            print(f"  Puntos equivalentes: {puntos}")
            
            # Verifica que todos dan el mismo n
            print(f"\n  Verificación:")
            for j, i in puntos:
                n_calc = self.crypto.n_function(j, i)
                formula = f"2({i}) + {j} = {2*i + j}"
                status = "✓" if n_calc == n else "✗"
                print(f"    {status} ({j},{i}): {formula} = {n_calc}")
            
            # Composiciones
            composiciones = self.encontrar_composiciones_exactas(n, max_terminos=3)
            alpha_val = self.crypto.count_square_partitions(n, max_squares=3)
            
            print(f"\n  Composiciones para n = {n}:")
            for idx, comp in enumerate(composiciones, 1):
                comp_str = " + ".join([f"{c}²" for c in comp])
                print(f"    {idx}. {comp_str}")
            
            print(f"\n  α(n={n}) = {alpha_val} (total de composiciones)")
    
    def validar_equivalencia_alpha_composiciones(self):
        """
        Valida que α(j,i) = número de composiciones de n(j,i)
        """
        print("\n" + "=" * 90)
        print("VALIDACIÓN: α(j,i) = Composiciones de n(j,i)".center(90))
        print("=" * 90)
        
        print("\n🔍 Verificando que α coincide con composiciones:\n")
        
        print(f"{'Punto (j,i)':>15} {'n(j,i)':>10} {'α(j,i)':>10} {'Composiciones':>15} {'¿Igual?':>15}")
        print("-" * 90)
        
        todas_validas = True
        for i in range(0, 6):
            for j in range(0, 8):
                n_val = self.crypto.n_function(j, i)
                alpha_val = self.crypto.alpha(j, i)
                composiciones = len(self.encontrar_composiciones_exactas(n_val, max_terminos=3))
                
                if alpha_val == composiciones:
                    status = "✓ SÍ"
                else:
                    status = "✗ NO"
                    todas_validas = False
                
                print(f"({j:1},{i:1}){'':<10} {n_val:>10} {alpha_val:>10} {composiciones:>15} {status:>15}")
        
        print("-" * 90)
        if todas_validas:
            print("\n✅ ¡TODAS LAS VALIDACIONES EXITOSAS!")
        else:
            print("\n⚠️ Hay discrepancias en algunas validaciones")
    
    def resumen_matematico(self):
        """
        Proporciona un resumen matemático claro
        """
        print("\n" + "=" * 90)
        print("RESUMEN MATEMÁTICO".center(90))
        print("=" * 90)
        
        print("\n📐 Definiciones Clave:\n")
        
        print("1️⃣  FUNCIÓN n(j,i) = 2i + j")
        print("   • Asigna un número único a cada punto del plano")
        print("   • Ejemplo: n(3,2) = 2(2) + 3 = 7")
        print()
        
        print("2️⃣  CLASE DE EQUIVALENCIA C_n")
        print("   • Conjunto de todos los puntos (j,i) que tienen el mismo valor n")
        print("   • Ejemplo: C_9 = {(1,4), (3,3), (5,2)}")
        print("   • Todos estos puntos satisfacen: 2i + j = 9")
        print()
        
        print("3️⃣  COMPOSICIONES COMO SUMA DE CUADRADOS")
        print("   • Número de formas de escribir n = a² + b² + c²")
        print("   • Ejemplos:")
        print("     - n=3: 3 = 1² + 1² + 1²  (una composición)")
        print("     - n=5: 5 = 2² + 1²  (una composición)")
        print("     - n=9: 9 = 3²  ó  9 = 2² + 2² + 1²  (dos composiciones)")
        print()
        
        print("4️⃣  FUNCIÓN α(j,i)")
        print("   • α(j,i) = número de composiciones de n(j,i)")
        print("   • α(1,1) = α de 3 = 1 composición")
        print("   • α(1,4) = α(3,3) = α(5,2) = α de 9 = 2 composiciones")
        print()
        
        print("5️⃣  RELACIÓN CON TRAYECTORIAS")
        print("   • α(j,i) también cuenta el número de trayectorias admisibles")
        print("   • Tipo I: trayectorias simples")
        print("   • Tipo II: concatenación de dos Tipo I")
        print("   • Tipo III: Tipo II + Tipo I con restricción")
        print()


def main():
    """Función principal"""
    print("\n" + "╔" + "═" * 88 + "╗")
    print("║" + "ANÁLISIS DETALLADO DE COMPOSICIONES".center(88) + "║")
    print("║" + "Criptosistema Γ-Pentagonal".center(88) + "║")
    print("╚" + "═" * 88 + "╝")
    
    analizador = AnalizadorComposiciones()
    
    # Ejecuta análisis
    analizador.demostrar_composiciones_profesor()
    
    analizador.analizar_clases_equivalentes()
    
    analizador.validar_equivalencia_alpha_composiciones()
    
    analizador.resumen_matematico()
    
    print("\n" + "╔" + "═" * 88 + "╗")
    print("║" + "✅ ANÁLISIS COMPLETADO".center(88) + "║")
    print("╚" + "═" * 88 + "╝\n")


if __name__ == "__main__":
    main()
