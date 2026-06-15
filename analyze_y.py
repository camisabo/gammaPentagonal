"""
Análisis Final de Y - Deducción de Lógica Correcta
"""

plaintext = "criptografiayseguridad"
expected_coords = [
    (0, 18), (1, 11), (2, 3), (2, 12), (2, 16), (3, 5), (4, 1), (5, 14),
    (8, 0), (2, 2), (2, 4), (8, 0), (9, 15), (1, 10), (5, 0), (5, 4),
    (5, 16), (7, 13), (7, 7), (0, 19), (1, 18), (2, 0)
]

expected_x = [x for x, y in expected_coords]
expected_y = [y for x, y in expected_coords]

print("=" * 80)
print("DEDUCCIÓN DE LÓGICA Y")
print("=" * 80)

print(f"\nTexto:    {' '.join(plaintext)}")
print(f"X actual: {expected_x}")
print(f"Y actual: {expected_y}")

# Tabla Delta X confirmada
delta_x_table = [8, 1, 1, 0, 0, 1, 1, 1, 3, 4, 0, 6, 1, 2, 4, 0, 0, 2, 0, 3, 1, 1]

print(f"ΔX table: {delta_x_table}")
print(f"X coincide: {[expected_x[i] for i in range(len(expected_x))]}")

# Análisis de Y: intentar encontrar patrón
print("\n\nAnálisis de Y:")
print("-" * 80)

print("\nPor posición:")
for i, (char, y, x) in enumerate(zip(plaintext, expected_y, expected_x)):
    ord_val = ord(char)
    y_prev = expected_y[i-1] if i > 0 else -6
    
    # ¿Delta Y?
    delta_y = (y - y_prev) % 20
    
    # ¿Relación con carácter?
    ord_mod10 = ord_val % 10
    ord_mod20 = ord_val % 20
    ascii_val = ord_val
    
    print(f"[{i+1:2d}] {char} → Y={y:2d}  ord={ord_val}(mod10:{ord_mod10}, mod20:{ord_mod20})  ΔY={delta_y:2d}  X={x}")

# Hipótesis: Y depende de la salida X anterior
print("\n\nAnálisis: ¿Y depende de X anterior?")
print("-" * 80)

for i, (char, y, x) in enumerate(zip(plaintext, expected_y, expected_x)):
    x_prev = expected_x[i-1] if i > 0 else (-8 % 10)
    y_prev = expected_y[i-1] if i > 0 else (-6 % 20)
    
    # Intentar relaciones
    rel1 = (x * 10 + ord(char)) % 20
    rel2 = (y_prev + ord(char)) % 20
    rel3 = (y_prev + x * 2) % 20
    rel4 = (y_prev + x_prev * 3 + ord(char)) % 20
    
    print(f"[{i+1:2d}] Y={y:2d}  rel1={rel1:2d}  rel2={rel2:2d}  rel3={rel3:2d}  rel4={rel4:2d}")

# Intentar encontrar transformación simple
print("\n\nIntentando transformación acumulada:")
print("-" * 80)

# Acumular desde el principio
y_test = (-6) % 20  # Y inicial
delta_y_needed = []

print(f"Y inicial: {y_test}\n")

for i, (char, y_expected) in enumerate(zip(plaintext, expected_y)):
    x_current = expected_x[i]
    x_prev = expected_x[i-1] if i > 0 else (-8 % 10)
    
    # ¿Qué delta necesitamos?
    delta_needed = (y_expected - y_test) % 20
    delta_y_needed.append(delta_needed)
    
    # Analizar este delta
    ord_val = ord(char)
    
    # Hipótesis de función
    h1 = ord_val % 20
    h2 = (ord_val + x_current * 5) % 20
    h3 = (ord_val + x_prev * 7) % 20
    h4 = (ord_val + x_current * 3 + i * 2) % 20
    
    match_str = ""
    if h1 == delta_needed:
        match_str = "✓ H1"
    elif h2 == delta_needed:
        match_str = "✓ H2"
    elif h3 == delta_needed:
        match_str = "✓ H3"
    elif h4 == delta_needed:
        match_str = "✓ H4"
    
    print(f"[{i+1:2d}] {char} ΔY_needed={delta_needed:2d}  H1={h1:2d}  H2={h2:2d}  H3={h3:2d}  H4={h4:2d}  {match_str}")
    
    y_test = (y_test + delta_needed) % 20

print(f"\nDeltas Y acumulados: {delta_y_needed}")

print("\n" + "=" * 80)
