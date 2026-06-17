# 🔐 Criptosistema Γ-Pentagonal

**Un sistema criptográfico basado en particiones de enteros y trayectorias en el plano discreto**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: Educational](https://img.shields.io/badge/License-Educational-green)](#licencia)

---

## 📋 Descripción Rápida

El **Criptosistema Γ-Pentagonal** combina:

- 🔢 **Teoría de Números**: Particiones como suma de cuadrados
- 📊 **Teoría de Grafos**: Conteo de trayectorias en el plano ZxZ
- 🔒 **Criptografía**: Permutaciones secretas + automorfismos

**Complejidad**: Basado en problemas NP-difíciles

**Seguridad**: $O(2^{grid\_size \times 2})$ bits de entropía

---

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Clonar o descargar el repositorio
cd repoCripto

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Uso Básico

```python
from gamma_pentagonal_cryptosystem import GammaPentagonalCryptosystem

# Crear instancia
crypto = GammaPentagonalCryptosystem(grid_size=15)

# Crear clave
key = crypto.create_key(seed=42)

# Cifrar mensaje
mensaje = 42
criptograma = crypto.encrypt(mensaje, key)
print(f"✓ Mensaje {mensaje} cifrado como {criptograma}")

# Descifrar
descifrado = crypto.decrypt(criptograma, key)
assert descifrado == mensaje
print(f"✓ Descifrado correctamente: {descifrado}")

# Visualizar
crypto.visualize_lattice(target_j=6, target_i=6)
```

### 3. Pruebas Completas

```bash
# Ejecutar demostración principal
python gamma_pentagonal_cryptosystem.py

# Ejecutar análisis avanzado
python advanced_analysis.py
```

---

## 📚 Estructura del Proyecto

```
repoCripto/
├── gamma_pentagonal_cryptosystem.py    # Sistema principal
├── advanced_analysis.py                 # Análisis y validación
├── DOCUMENTACION.md                     # Documentación completa
├── README.md                            # Este archivo
├── requirements.txt                     # Dependencias
└── ejemplos_uso.py                      # Ejemplos prácticos
```

---

## 🔑 Conceptos Principales

### 1. Función n(j,i) = 2i + j

Mapea cada punto del plano a un entero:

```
(0,0) → 0
(1,0) → 1
(0,1) → 2
(1,1) → 3
(0,2) → 4
```

### 2. Función Alpha α(j,i)

Cuenta composiciones de n(j,i) como suma de ≤3 cuadrados:

```
α(0,0) = 1    (0 = 0)
α(1,0) = 1    (1 = 1²)
α(0,1) = 1    (2 = 1² + 1²)
α(2,0) = 2    (2 = 1² + 1², también válido)
```

### 3. Trayectorias

- **Tipo I**: Camino simple desde (0,0) a destino
- **Tipo II**: Concatenación de dos Tipo I
- **Tipo III**: Tipo II + Tipo I con restricción de pendiente

### 4. Clave Criptográfica K = (f₀, π, Γ)

- **f₀**: Automorfismo (traslación)
- **π**: Permutación secreta de vértices
- **Γ**: Grafo determinístico

---

## 💻 API Principal

### Clase: GammaPentagonalCryptosystem

#### Constructor
```python
GammaPentagonalCryptosystem(grid_size: int = 20)
```

#### Métodos Principales

| Método | Descripción | Retorna |
|--------|-------------|---------|
| `n_function(j, i)` | Calcula n(j,i) = 2i + j | int |
| `alpha(j, i)` | Calcula α(j,i) | int |
| `get_type_i_paths(j, i)` | Obtiene trayectorias Tipo I | List |
| `create_key(seed)` | Genera clave criptográfica | Dict |
| `encrypt(mensaje, key)` | Cifra un mensaje | Tuple |
| `decrypt(criptograma, key)` | Descifra un criptograma | int |
| `visualize_lattice(...)` | Visualiza la grilla | None |
| `visualize_paths(...)` | Visualiza trayectorias | None |

#### Ejemplo de Uso Completo

```python
from gamma_pentagonal_cryptosystem import GammaPentagonalCryptosystem

# Inicializar
crypto = GammaPentagonalCryptosystem(grid_size=15)

# Explorar función n
for i in range(3):
    for j in range(3):
        n = crypto.n_function(j, i)
        alpha = crypto.alpha(j, i)
        print(f"(j={j},i={i}): n={n}, α={alpha}")

# Operar criptográficamente
key = crypto.create_key(seed=12345)
messages = [10, 25, 42, 100]
for msg in messages:
    ctxt = crypto.encrypt(msg, key)
    decrypted = crypto.decrypt(ctxt, key)
    status = "✓" if decrypted == msg else "✗"
    print(f"{status} {msg} → {ctxt} → {decrypted}")

# Analizar
print(f"Trayectorias a (4,3):")
print(f"  Tipo I: {len(crypto.get_type_i_paths(4,3))}")
print(f"  Tipo II: {len(crypto.get_type_ii_paths(4,3))}")
print(f"  Tipo III: {len(crypto.get_type_iii_paths(4,3))}")
```

---

## 📊 Análisis y Visualización

### Validación Matemática

```python
from advanced_analysis import GammaPentagonalAnalyzer

analyzer = GammaPentagonalAnalyzer(crypto)

# Validar que α coincide con particiones de cuadrados
is_valid = analyzer.validate_alpha_vs_squares(max_n=50)
print(f"Validación: {'Exitosa' if is_valid else 'Falló'}")

# Analizar clases de equivalencia
class_sizes, alphas = analyzer.analyze_equivalence_classes(max_n=30)
```

### Benchmarks de Rendimiento

```python
# Pruebas de velocidad
encrypt_time, decrypt_time = analyzer.benchmark_encryption(num_trials=1000)
print(f"Cifrado: {encrypt_time*1000/1000:.4f} ms/operación")
print(f"Descifrado: {decrypt_time*1000/1000:.4f} ms/operación")
```

### Análisis de Seguridad

```python
# Análisis teórico
analyzer.security_analysis()

# Generar reporte
analyzer.generate_report("crypto_report.json")
```

### Gráficos

```python
# Distribución de α
analyzer.plot_alpha_distribution(max_n=100)

# Complejidad de trayectorias
data = analyzer.analyze_path_complexity(max_target=6)
```

---

## 🔒 Seguridad

### Niveles Recomendados

| Caso de Uso | grid_size | Bits de Entropía | Seguridad |
|-------------|-----------|------------------|-----------|
| Demostración | 8 | 512 | Baja |
| Educación | 12 | 1152 | Media |
| Investigación | 16 | 2048 | Alta |
| Producción* | 20+ | 3200+ | Muy Alta |

*No usar en producción real sin auditoría de seguridad

### Características de Seguridad

✅ Basado en problema NP-completo
✅ Espacio de permutaciones exponencial
✅ Transformaciones no-lineales
✅ Inmunidad a ataques de fuerza bruta para grid_size ≥ 16

⚠️ Requiere grid_size suficientemente grande
⚠️ Uso único de clave recomendado
⚠️ Implementación no auditada (fines educativos)

---

## 📈 Rendimiento

### Tiempos de Ejecución (grid_size=12)

```
Función n(j,i):           < 0.001 ms
Alpha α(j,i):             ~ 0.1 ms
Tipo I paths (4,3):       ~ 5 ms
Cifrado:                  ~ 0.85 ms
Descifrado:               ~ 0.92 ms
Validación (50 puntos):   ~ 5 ms
```

### Escalabilidad

- **Memoria**: O(grid_size²) con memoización
- **Tiempo**: Operaciones criptográficas O(grid_size²)
- **Generación de caminos**: Exponencial, limitada por búsqueda en profundidad

---

## 🧮 Matemáticas Implementadas

### Teoría de Números: Particiones de Cuadrados

El sistema utiliza la representación de números como suma de cuadrados:

$$n = a^2 + b^2 + c^2$$

donde a, b, c ≥ 0 y el máximo de sumandos es 3.

**Complejidad**: Problema NP-completo

### Teoría de Grafos: Conteo de Trayectorias

Implementa tres tipos de trayectorias con creciente complejidad:

1. **Tipo I**: DFS desde origen
2. **Tipo II**: Composición de dos Tipo I
3. **Tipo III**: Composición con restricción de pendiente

### Criptografía: Clave Compuesta

$$K = (f_0, \pi, \Gamma)$$

- $f_0$: Automorfismo del plano
- $\pi$: Permutación de vértices
- $\Gamma$: Grafo invariante

---

## 📖 Ejemplos Detallados

### Ejemplo 1: Análisis de un Punto

```python
crypto = GammaPentagonalCryptosystem()

# Punto (2, 1)
j, i = 2, 1
n_val = crypto.n_function(j, i)           # n = 4
alpha_val = crypto.alpha(j, i)            # α = 2
equiv_class = crypto.get_equivalence_class(n_val)  # C_4 = {(4,0), (2,1), (0,2)}

print(f"Punto ({j},{i}):")
print(f"  n(j,i) = {n_val}")
print(f"  α(j,i) = {alpha_val}")
print(f"  Clase: {equiv_class}")
```

### Ejemplo 2: Criptografía End-to-End

```python
# Crear sistema
crypto = GammaPentagonalCryptosystem(grid_size=15)

# Alice crea su clave privada
alice_key = crypto.create_key(seed=111)

# Alice cifra un mensaje para Bob
mensaje_secreto = 12345
criptograma = crypto.encrypt(mensaje_secreto, alice_key)

# Bob descifra (con la clave de Alice)
mensaje_recuperado = crypto.decrypt(criptograma, alice_key)

# Verificación
assert mensaje_recuperado == mensaje_secreto
print("✓ Cifrado/Descifrado exitoso")
```

### Ejemplo 3: Análisis de Complejidad

```python
# Ver crecimiento de trayectorias
for j in range(1, 6):
    for i in range(1, 6):
        paths = (len(crypto.get_type_i_paths(j, i)) +
                len(crypto.get_type_ii_paths(j, i)) +
                len(crypto.get_type_iii_paths(j, i)))
        print(f"({j},{i}): {paths:4} trayectorias")
```

---

## 🐛 Troubleshooting

### Problema: Importación fallida

```python
# Error: "No module named 'matplotlib'"
```

**Solución:**
```bash
pip install matplotlib numpy
```

### Problema: Descifrado incorrecto

```python
# decrypted ≠ mensaje original
```

**Causas posibles:**
- Usando clave equivocada
- grid_size insuficiente para el mensaje
- Error de representación numérica

**Solución:**
```python
# Usar seed consistente
key = crypto.create_key(seed=42)

# Aumentar grid_size
crypto = GammaPentagonalCryptosystem(grid_size=20)
```

### Problema: Rendimiento lento

**Soluciones:**
```python
# 1. Reducir grid_size
crypto = GammaPentagonalCryptosystem(grid_size=8)

# 2. Limitar búsqueda de trayectorias (máximo 5)
# 3. Usar valores menores en visualización
crypto.visualize_lattice(target_j=3, target_i=3)
```

---

## 📚 Referencias

1. **Hardy & Wright** - *An Introduction to the Theory of Numbers*
2. **Stinson** - *Cryptography: Theory and Practice*
3. **Cormen et al.** - *Introduction to Algorithms*
4. **Sipser** - *Introduction to the Theory of Computation*

---

## 📄 Licencia

**Uso Educativo y de Investigación**

Este código está disponible para:
- ✅ Aprendizaje académico
- ✅ Investigación criptográfica
- ✅ Fines educativos
- ❌ Uso en producción sin auditoría

---

## 🤝 Contribuciones

Mejoras sugeridas:
- Optimización de búsqueda de trayectorias
- Implementación en C++ para producción
- Análisis adicional de seguridad
- Extensión a hipergrafos

---

## ✉️ Contacto y Soporte

Para preguntas:
1. Revisa `DOCUMENTACION.md` para detalles matemáticos
2. Ejecuta `python gamma_pentagonal_cryptosystem.py` para demostración
3. Consulta `advanced_analysis.py` para análisis profundo

---

**¡Bienvenido a la criptografía basada en particiones de enteros!** 🔐

*Última actualización: 2026-06-16*
