"""
Ingeniería Inversa Exhaustiva del Algoritmo Gamma-Pentagonal
Prueba múltiples hipótesis para encontrar el patrón correcto
"""

# Vector de prueba
plaintext = "criptografiayseguridad"
expected_coords = [
    (0, 18), (1, 11), (2, 3), (2, 12), (2, 16), (3, 5), (4, 1), (5, 14),
    (8, 0), (2, 2), (2, 4), (8, 0), (9, 15), (1, 10), (5, 0), (5, 4),
    (5, 16), (7, 13), (7, 7), (0, 19), (1, 18), (2, 0)
]

expected_x = [x for x, y in expected_coords]
expected_y = [y for x, y in expected_coords]

print("=" * 80)
print("ANÁLISIS EXHAUSTIVO DE PATRONES")
print("=" * 80)

# Hipótesis 1: X es derivado de una permutación sigma sobre dígitos
print("\nHIPÓTESIS 1: X derivado de permutación de caracteres")
print("-" * 80)

# Crear mapeo de carácter único a valores de X
from collections import defaultdict
char_to_first_x = {}
char_indices = {}

for i, (char, x) in enumerate(zip(plaintext, expected_x)):
    if char not in char_to_first_x:
        char_to_first_x[char] = x
        char_indices[char] = i

print("\nPrimer X para cada carácter:")
for char in sorted(char_to_first_x.keys()):
    print(f"  '{char}': {char_to_first_x[char]} (primera aparición en pos {char_indices[char]+1})")

# Hipótesis 2: Secuencia de X es acumulada/derivada posicionalmente
print("\n\nHIPÓTESIS 2: X como secuencia generada posicionalmente")
print("-" * 80)

print(f"Secuencia X observada: {expected_x}")

# Buscar incrementos/patrones
print("\nIncremento entre X consecutivas:")
for i in range(len(expected_x)):
    if i == 0:
        prev_x = -8  # P0.x
    else:
        prev_x = expected_x[i-1]
    
    curr_x = expected_x[i]
    delta = (curr_x - prev_x) % 10  # Considerando aritmética modulo
    char = plaintext[i]
    ord_char = ord(char) % 10
    
    print(f"  Pos {i+1}: {char} (ord%10={ord_char}) → Δx={(curr_x-prev_x) % 10}, x_nuevo={curr_x}")

# Hipótesis 3: Búsqueda de permutación sigma que se repite en Y
print("\n\nHIPÓTESIS 3: Análisis de Y para deducir la transformación")
print("-" * 80)

print(f"\nSecuencia Y observada: {expected_y}")

# Análisis de Y con respecto a carácter y posición
print("\nY por posición y carácter:")
for i, (char, y) in enumerate(zip(plaintext, expected_y)):
    ord_val = ord(char)
    print(f"  Pos {i+1}: {char} (ord={ord_val}, ord%10={ord_val%10}, ord%20={ord_val%20}) → y={y}")

# Hipótesis 4: Y podría ser determinado por tablas de consulta
print("\n\nHIPÓTESIS 4: Tablas de Lookup (LUT) para coordenadas")
print("-" * 80)

# Crear tabla X y Y por carácter
char_coord_table = defaultdict(list)
for char, (x, y) in zip(plaintext, expected_coords):
    char_coord_table[char].append((x, y))

print("\nTabla de Coordenadas por Carácter:")
for char in sorted(char_coord_table.keys()):
    coords = char_coord_table[char]
    print(f"  '{char}': {coords}")

# Hipótesis 5: Búsqueda de función matemática simple
print("\n\nHIPÓTESIS 5: Función matemática simple")
print("-" * 80)

# Probar si X_i = f(posición, carácter anterior, ...)
print("\nIntentando f(X_{i-1}, char_i, pos) → X_i:")

# Modelo simple: X_i = (X_{i-1} + f(char)) mod 10
print("\nModelo: X_i = (X_{i-1} + delta) mod 10")
for i in range(min(10, len(expected_x))):
    if i == 0:
        x_prev = 2  # Normalizar (-8 mod 10 = 2)
    else:
        x_prev = expected_x[i-1]
    
    char = plaintext[i]
    x_curr = expected_x[i]
    
    # ¿Qué delta necesitamos?
    delta_needed = (x_curr - x_prev) % 10
    
    # Intentar diferentes funciones
    ord_mod = ord(char) % 10
    pos_mod = i % 10
    ascii_val = ord(char)
    
    print(f"  Pos {i+1}: {char} → delta_actual={(x_curr - x_prev) % 10}")
    print(f"         ord%10={ord_mod}, pos%10={pos_mod}")

# HIPÓTESIS CRÍTICA: Permutación fija por carácter
print("\n\nHIPÓTESIS CRÍTICA: Permutación Sigma Implícita")
print("-" * 80)

# Si X es derminístico por carácter:
print("\nMapeando cada carácter único a su primer X:")
sigma_explicit = {}
for char in sorted(set(plaintext)):
    for i, (c, x) in enumerate(zip(plaintext, expected_x)):
        if c == char and char not in sigma_explicit:
            sigma_explicit[char] = x
            break

# Crear permutación de 10 dígitos basada en posiciones alfabéticas
alphabet = "abcdefghij"
sigma_digits = ""
for i in range(10):
    if alphabet[i] in sigma_explicit:
        sigma_digits += str(sigma_explicit[alphabet[i]])
    else:
        sigma_digits += str(i)

print(f"\nPermutación σ reconstruida: {sigma_digits}")

# Verificar si funciona
print("\nVerificación: ¿X_i = σ[ord(char_i) % 10]?")
sigma_array = [int(d) for d in sigma_digits]
for i, (char, x_expected) in enumerate(zip(plaintext, expected_x)):
    idx = ord(char) % 10
    x_from_sigma = sigma_array[idx] if idx < len(sigma_array) else '?'
    match = "✓" if x_from_sigma == x_expected else "✗"
    print(f"  {char} (idx={idx}): esperado={x_expected}, σ[{idx}]={x_from_sigma} {match}")

print("\n" + "=" * 80)
