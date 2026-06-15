"""
Análisis Inverso del Vector de Prueba Académico UNAL
Para deducir la permutación sigma y la lógica del algoritmo Gamma-Pentagonal
"""

import numpy as np
from collections import defaultdict

# Vector de prueba académico
plaintext = "criptografiayseguridad"
expected_coords = [
    (0, 18), (1, 11), (2, 3), (2, 12), (2, 16), (3, 5), (4, 1), (5, 14),
    (8, 0), (2, 2), (2, 4), (8, 0), (9, 15), (1, 10), (5, 0), (5, 4),
    (5, 16), (7, 13), (7, 7), (0, 19), (1, 18), (2, 0)
]

print("=" * 70)
print("ANÁLISIS INVERSO: DEDUCCIÓN DE PARÁMETROS DEL ALGORITMO")
print("=" * 70)
print(f"\nTexto Plano: {plaintext}")
print(f"Longitud: {len(plaintext)}")
print(f"Coordenadas Esperadas: {len(expected_coords)}\n")

# Análisis 1: Mapeo de caracteres
print("ANÁLISIS 1: Mapeo de Caracteres a Coordenadas")
print("-" * 70)

char_to_coords = defaultdict(list)
for i, (char, coord) in enumerate(zip(plaintext, expected_coords)):
    char_to_coords[char].append((i, coord))
    
for char in sorted(char_to_coords.keys()):
    coords_list = char_to_coords[char]
    print(f"\nCarácter '{char}':")
    for idx, (pos, coord) in enumerate(coords_list):
        print(f"  Posición {pos+1}: {coord}")

# Análisis 2: Patrones de coordenada X
print("\n\nANÁLISIS 2: Patrones de Coordenada X")
print("-" * 70)

x_values = [x for x, y in expected_coords]
y_values = [y for x, y in expected_coords]

print(f"Valores X: {x_values}")
print(f"Rango X: [{min(x_values)}, {max(x_values)}]")
print(f"\nValores Y: {y_values}")
print(f"Rango Y: [{min(y_values)}, {max(y_values)}]")

# Análisis 3: Diferencias entre coordenadas consecutivas
print("\n\nANÁLISIS 3: Diferencias entre Coordenadas Consecutivas")
print("-" * 70)

print("Pos  Char  Δx  Δy  Coord")
for i in range(len(expected_coords)):
    if i == 0:
        dx, dy = expected_coords[i][0] - (-8), expected_coords[i][1] - (-6)
    else:
        dx = (expected_coords[i][0] - expected_coords[i-1][0]) % 20
        dy = (expected_coords[i][1] - expected_coords[i-1][1]) % 20
    print(f" {i+1:2d}   {plaintext[i]}    {dx:2d}  {dy:2d}   {expected_coords[i]}")

# Análisis 4: Búsqueda de permutación sigma
print("\n\nANÁLISIS 4: Búsqueda de Permutación Sigma")
print("-" * 70)

# Si X es derivado de la permutación, intentar deducirla
# Asumir que X depende del carácter
print("\nIntentando mapeo directo carácter → X:")
char_x_map = {}
for char, coords_list in char_to_coords.items():
    x_vals = [coord[0] for _, coord in coords_list]
    print(f"  '{char}': {x_vals}")

# Análisis 5: Orden de caracteres en alfabeto
print("\n\nANÁLISIS 5: Relación con Posición en Alfabeto")
print("-" * 70)

print("Char  Ord(char)  Ord%10  First_X  First_Y")
seen = set()
for char, coords_list in char_to_coords.items():
    if char not in seen:
        first_coord = coords_list[0][1]
        print(f" {char}     {ord(char)}      {ord(char)%10}       {first_coord[0]}      {first_coord[1]}")
        seen.add(char)

# Análisis 6: Permutación deducida
print("\n\nANÁLISIS 6: Deducción de Permutación σ")
print("-" * 70)

# Método: Si el primer X de cada carácter es consistente
sigma_map = {}
for i, char in enumerate(plaintext):
    if char not in sigma_map:
        sigma_map[char] = expected_coords[i][0]

print("\nMapeo carácter → X (permutación deducida):")
for char in sorted(sigma_map.keys()):
    print(f"  σ({char}) = {sigma_map[char]}")

# Crear permutación de 10 dígitos
print("\n\nPERMUTACIÓN SIGMA RECONSTRUIDA:")
print("-" * 70)

# Mapear caracteres a dígitos 0-9
char_list = sorted(sigma_map.keys())
sigma_string = ""
for i in range(10):
    if i < len(char_list):
        sigma_string += str(sigma_map[char_list[i]] % 10)
    else:
        sigma_string += str(i)

print(f"Permutación σ: {sigma_string}")

# Validación: intentar reconstruir patrón
print("\n\nVALIDACIÓN: Búsqueda de Patrón")
print("-" * 70)

# Verificar si hay un patrón simple en X
print("\nPatrón en X:")
for i, (char, (x, y)) in enumerate(zip(plaintext, expected_coords)):
    # Intentar varias hipótesis
    h1 = i  # X = posición
    h2 = ord(char) % 10  # X = ord(char) % 10
    h3 = ord(char) % 20  # X = ord(char) % 20
    
    if i < 5:
        print(f"  Pos {i+1}: Actual X={x}, H1(pos)={h1}, H2(ord%10)={h2}, H3(ord%20)={h3}")

print("\n" + "=" * 70)
