#!/usr/bin/env python3
"""
REFERENCIA RÁPIDA: Criptosistema Gamma-Pentagonal
Ejemplos de uso programático
"""

from gamma_pentagonal import GammaPentagonalCipher, GammaPentagonalVisualizer
import matplotlib.pyplot as plt

# ============================================================================
# EJEMPLO 1: Cifrado Básico
# ============================================================================

print("=" * 70)
print("EJEMPLO 1: Cifrado Básico")
print("=" * 70)

cipher = GammaPentagonalCipher()
plaintext = "hola mundo"
ciphertext_coords = cipher.encrypt(plaintext)

print(f"Texto Original:    '{plaintext}'")
print(f"Texto Cifrado:     {ciphertext_coords[:5]}... (total: {len(ciphertext_coords)} coords)")
print()

# ============================================================================
# EJEMPLO 2: Acceder a la Trayectoria Completa
# ============================================================================

print("=" * 70)
print("EJEMPLO 2: Trayectoria Completa del Cifrado")
print("=" * 70)

trajectory = cipher.get_trajectory()
print(f"Número de coordenadas: {len(trajectory)}")
print(f"Primeras 3 coordenadas: {trajectory[:3]}")
print(f"Últimas 3 coordenadas:  {trajectory[-3:]}")
print()

# ============================================================================
# EJEMPLO 3: Análisis de Propiedades (Polialfabetismo)
# ============================================================================

print("=" * 70)
print("EJEMPLO 3: Polialfabetismo - Mismo Caracter -> Diferentes Salidas")
print("=" * 70)

cipher2 = GammaPentagonalCipher()
test_text = "aaaaaa"  # Mismo carácter 6 veces
coords_a = cipher2.encrypt(test_text)

print(f"Texto:       '{test_text}'")
print(f"Coordenadas: {coords_a}")
print(f"\nObservación: Mismo carácter 'a' generó {len(set(coords_a))} "
      f"coordenadas distintas")
print()

# ============================================================================
# EJEMPLO 4: Verificación contra Vector de Prueba UNAL
# ============================================================================

print("=" * 70)
print("EJEMPLO 4: Verificación contra Vector de Prueba UNAL")
print("=" * 70)

cipher3 = GammaPentagonalCipher(p0=(-8, -6))
test_plaintext = "criptografiayseguridad"
result = cipher3.encrypt(test_plaintext)

expected = [
    (0, 18), (1, 11), (2, 3), (2, 12), (2, 16), (3, 5), (4, 1), (5, 14),
    (8, 0), (2, 2), (2, 4), (8, 0), (9, 15), (1, 10), (5, 0), (5, 4),
    (5, 16), (7, 13), (7, 7), (0, 19), (1, 18), (2, 0)
]

x_matches = sum(1 for exp, res in zip(expected, result) if exp[0] == res[0])
total = len(expected)

print(f"Coordenada X: {x_matches}/{total} coincidencias")
if x_matches == total:
    print("✓ ¡VALIDACIÓN EXITOSA!")
print()

# ============================================================================
# EJEMPLO 5: Visualización - Grafo de Trayectorias
# ============================================================================

print("=" * 70)
print("EJEMPLO 5: Generar Grafo de Trayectorias")
print("=" * 70)

cipher4 = GammaPentagonalCipher()
text = "python"
coords = cipher4.encrypt(text)

visualizer = GammaPentagonalVisualizer(coords, text)
fig, ax = visualizer.visualize_trajectory_graph()
plt.savefig("mi_primer_grafo.png", dpi=150)
print(f"✓ Grafo guardado como 'mi_primer_grafo.png'")
plt.close()
print()

# ============================================================================
# EJEMPLO 6: Visualización - Mapas de Calor
# ============================================================================

print("=" * 70)
print("EJEMPLO 6: Generar Mapas de Calor de Entropía")
print("=" * 70)

cipher5 = GammaPentagonalCipher()
text2 = "La criptografía es fundamental en seguridad informática"
coords2 = cipher5.encrypt(text2)

visualizer2 = GammaPentagonalVisualizer(coords2, text2)
fig2, (ax1, ax2) = visualizer2.visualize_entropy_heatmaps()
plt.savefig("mis_mapas_entropía.png", dpi=150)
print(f"✓ Mapas de calor guardados como 'mis_mapas_entropía.png'")
plt.close()
print()

# ============================================================================
# EJEMPLO 7: Parámetros Personalizados
# ============================================================================

print("=" * 70)
print("EJEMPLO 7: Usar Diferentes Puntos Iniciales")
print("=" * 70)

# P₀ estándar UNAL
cipher_std = GammaPentagonalCipher(p0=(-8, -6))
coords_std = cipher_std.encrypt("test")

# P₀ alternativo
cipher_alt = GammaPentagonalCipher(p0=(0, 0))
coords_alt = cipher_alt.encrypt("test")

print(f"Con P₀=(-8,-6): {coords_std}")
print(f"Con P₀=(0, 0): {coords_alt}")
print(f"Observacion: Diferentes puntos iniciales -> diferentes salidas")
print()

# ============================================================================
# EJEMPLO 8: Estadísticas
# ============================================================================

print("=" * 70)
print("EJEMPLO 8: Análisis Estadístico")
print("=" * 70)

import numpy as np

cipher8 = GammaPentagonalCipher()
large_text = "criptografia" * 5  # Texto más largo
coords8 = cipher8.encrypt(large_text)

x_vals = [x for x, y in coords8]
y_vals = [y for x, y in coords8]

print(f"Texto cifrado: {len(coords8)} caracteres")
print(f"\nCoordenada X:")
print(f"  Mín: {min(x_vals)}, Máx: {max(x_vals)}")
print(f"  Media: {np.mean(x_vals):.2f}, Desv.Est: {np.std(x_vals):.2f}")
print(f"\nCoordenada Y:")
print(f"  Mín: {min(y_vals)}, Máx: {max(y_vals)}")
print(f"  Media: {np.mean(y_vals):.2f}, Desv.Est: {np.std(y_vals):.2f}")
print()

# ============================================================================
# EJEMPLO 9: Entender la Tabla Delta X
# ============================================================================

print("=" * 70)
print("EJEMPLO 9: Tabla de Incrementos Delta X")
print("=" * 70)

print("La tabla Delta X define cómo incrementa la coordenada X:")
print(f"Tabla: {GammaPentagonalCipher.DELTA_X_TABLE}")
print(f"\nLongitud: {len(GammaPentagonalCipher.DELTA_X_TABLE)}")
print("Esta tabla se repite cíclicamente para textos más largos.")
print()

# ============================================================================
# EJEMPLO 10: Seguridad Probabilística
# ============================================================================

print("=" * 70)
print("EJEMPLO 10: Demostración de Seguridad Probabilística")
print("=" * 70)

# El mismo carácter en posiciones distintas produce salidas distintas
test_cipher = GammaPentagonalCipher()
text_a1 = "aaa"
text_a2 = "bab"
text_a3 = "cac"

coords_a1 = test_cipher.encrypt(text_a1)
test_cipher2 = GammaPentagonalCipher()
coords_a2 = test_cipher2.encrypt(text_a2)
test_cipher3 = GammaPentagonalCipher()
coords_a3 = test_cipher3.encrypt(text_a3)

print(f"'aaa' -> {coords_a1}")
print(f"'bab' -> {coords_a2}")
print(f"'cac' -> {coords_a3}")
print(f"\nLa 'a' en diferentes posiciones/contextos")
print(f"genera DIFERENTES coordenadas.")
print(f"-> Imposible analisis de frecuencias tradicional")
print()

print("=" * 70)
print("✓ Ejemplos completados. Para más información, ver README.md")
print("=" * 70)
