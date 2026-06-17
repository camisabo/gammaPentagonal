"""
Script Maestro: Ejecuta Todas las Validaciones del Profesor
Interfaz interactiva para validar el Criptosistema Γ-Pentagonal
"""

import os
import sys
import subprocess


def limpiar_pantalla():
    """Limpia la pantalla"""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_menu_principal():
    """Muestra el menú principal"""
    print("\n" + "╔" + "═" * 88 + "╗")
    print("║" + "CRIPTOSISTEMA Γ-PENTAGONAL - VALIDACIÓN COMPLETA".center(88) + "║")
    print("║" + "Sistema de Validación de Ejemplos del Profesor".center(88) + "║")
    print("╚" + "═" * 88 + "╝")
    
    print("\n📋 MENÚ PRINCIPAL - Selecciona una opción:\n")
    
    opciones = [
        ("Validación de Puntos del Profesor", 
         "validacion_puntos_profesor.py",
         "Valida los 7 puntos específicos mencionados por el profesor"),
        
        ("Análisis Detallado de Composiciones",
         "analisis_composiciones_detallado.py",
         "Análisis profundo de composiciones como suma de cuadrados"),
        
        ("Generación de Gráficas del Profesor",
         "graficas_profesor.py",
         "Replica las 5 gráficas mostradas en clase"),
        
        ("Ejemplos Interactivos de Uso",
         "ejemplos_uso.py",
         "8 ejemplos prácticos interactivos"),
        
        ("Análisis Avanzado Completo",
         "advanced_analysis.py",
         "Benchmarks, validación matemática y reportes"),
        
        ("Demostración Principal del Sistema",
         "gamma_pentagonal_cryptosystem.py",
         "Demostración completa del criptosistema"),
        
        ("EJECUTAR TODAS LAS VALIDACIONES (SECUENCIAL)",
         "all",
         "Ejecuta todas las validaciones en orden recomendado"),
    ]
    
    for i, (nombre, archivo, descripcion) in enumerate(opciones, 1):
        print(f"   {i}. {nombre}")
        print(f"      └─ {descripcion}")
        print()
    
    print(f"   0. Salir\n")
    
    return opciones


def ejecutar_script(archivo):
    """Ejecuta un script Python"""
    try:
        print(f"\n{'─' * 90}")
        print(f"Ejecutando: {archivo}")
        print(f"{'─' * 90}\n")
        
        resultado = subprocess.run([sys.executable, archivo], cwd=os.getcwd())
        
        if resultado.returncode == 0:
            print(f"\n✅ Script completado exitosamente")
        else:
            print(f"\n⚠️ Script terminó con código: {resultado.returncode}")
        
        return True
    
    except FileNotFoundError:
        print(f"\n❌ Error: No se encontró el archivo '{archivo}'")
        print(f"   Asegúrate de estar en el directorio correcto:")
        print(f"   {os.getcwd()}")
        return False
    except Exception as e:
        print(f"\n❌ Error al ejecutar: {str(e)}")
        return False


def ejecutar_todas():
    """Ejecuta todas las validaciones en orden"""
    print("\n" + "═" * 90)
    print("EJECUTANDO TODAS LAS VALIDACIONES (ORDEN SECUENCIAL RECOMENDADO)".center(90))
    print("═" * 90)
    
    secuencia = [
        ("validacion_puntos_profesor.py", 
         "PASO 1: Validación de Puntos Específicos"),
        
        ("analisis_composiciones_detallado.py",
         "PASO 2: Análisis Matemático Detallado"),
        
        ("graficas_profesor.py",
         "PASO 3: Generación de Gráficas"),
    ]
    
    completados = 0
    fallos = 0
    
    for script, descripcion in secuencia:
        print(f"\n{'▶' * 45}")
        print(f"\n{descripcion}")
        print(f"Archivo: {script}")
        
        if ejecutar_script(script):
            completados += 1
        else:
            fallos += 1
        
        if completados + fallos < len(secuencia):
            print(f"\n{'─' * 90}")
            respuesta = input("¿Continuar con el siguiente script? (S/n): ").lower()
            if respuesta == 'n':
                print("\n⏹️  Ejecución cancelada por el usuario")
                break
    
    # Resumen final
    print(f"\n{'═' * 90}")
    print("RESUMEN FINAL".center(90))
    print(f"{'═' * 90}")
    print(f"\n   ✅ Scripts completados exitosamente: {completados}")
    print(f"   ❌ Scripts con errores: {fallos}")
    print(f"   📊 Total procesado: {completados + fallos}/{len(secuencia)}")
    
    if fallos == 0:
        print(f"\n   🎉 ¡TODAS LAS VALIDACIONES COMPLETADAS EXITOSAMENTE!")
    
    print()


def menu_interactivo():
    """Menú interactivo principal"""
    while True:
        limpiar_pantalla()
        opciones = mostrar_menu_principal()
        
        try:
            choice = input("   ¿Qué deseas hacer? Ingresa número (0-7): ").strip()
            
            if choice == '0':
                print("\n   👋 ¡Hasta luego!\n")
                break
            
            elif choice == '7':
                ejecutar_todas()
                input("\nPresiona Enter para volver al menú...")
            
            elif choice.isdigit() and 1 <= int(choice) <= 6:
                idx = int(choice) - 1
                archivo = opciones[idx][1]
                ejecutar_script(archivo)
                input("\nPresiona Enter para volver al menú...")
            
            else:
                print("\n   ❌ Opción inválida. Por favor ingresa un número entre 0-7.")
                input("\nPresiona Enter para intentar de nuevo...")
        
        except KeyboardInterrupt:
            print("\n\n   👋 Programa interrumpido por el usuario.\n")
            break
        except Exception as e:
            print(f"\n   ❌ Error: {str(e)}")
            input("\nPresiona Enter para continuar...")


def main_simple():
    """Interfaz no interactiva para ejecución directa"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validador del Criptosistema Γ-Pentagonal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python ejecutar_validaciones.py                 # Menú interactivo
  python ejecutar_validaciones.py --all           # Ejecutar todas las validaciones
  python ejecutar_validaciones.py --puntos        # Solo validación de puntos
  python ejecutar_validaciones.py --graficas      # Solo generación de gráficas
        """
    )
    
    parser.add_argument('--all', action='store_true',
                       help='Ejecutar todas las validaciones en secuencia')
    parser.add_argument('--puntos', action='store_true',
                       help='Ejecutar validación de puntos')
    parser.add_argument('--composiciones', action='store_true',
                       help='Ejecutar análisis de composiciones')
    parser.add_argument('--graficas', action='store_true',
                       help='Generar gráficas del profesor')
    parser.add_argument('--ejemplos', action='store_true',
                       help='Ejecutar ejemplos interactivos')
    parser.add_argument('--analisis', action='store_true',
                       help='Ejecutar análisis avanzado')
    
    args = parser.parse_args()
    
    # Si no hay argumentos, muestra menú interactivo
    if not any(vars(args).values()):
        menu_interactivo()
        return
    
    # Ejecuta según argumentos
    scripts_ejecutar = []
    
    if args.all:
        scripts_ejecutar = [
            "validacion_puntos_profesor.py",
            "analisis_composiciones_detallado.py",
            "graficas_profesor.py",
        ]
    else:
        if args.puntos:
            scripts_ejecutar.append("validacion_puntos_profesor.py")
        if args.composiciones:
            scripts_ejecutar.append("analisis_composiciones_detallado.py")
        if args.graficas:
            scripts_ejecutar.append("graficas_profesor.py")
        if args.ejemplos:
            scripts_ejecutar.append("ejemplos_uso.py")
        if args.analisis:
            scripts_ejecutar.append("advanced_analysis.py")
    
    # Ejecuta scripts
    for script in scripts_ejecutar:
        if os.path.exists(script):
            ejecutar_script(script)
            print("\n")
        else:
            print(f"⚠️ Advertencia: {script} no encontrado")


def main():
    """Punto de entrada principal"""
    # Verifica si hay argumentos de línea de comandos
    if len(sys.argv) > 1:
        main_simple()
    else:
        menu_interactivo()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!\n")
        sys.exit(0)
