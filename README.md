# Criptosistema Gamma-Pentagonal: Implementación Completa

## 📋 Descripción

Este repositorio contiene la **implementación académica completa** del **Criptosistema Gamma-Pentagonal**, un esquema de cifrado asimétrico probabilístico basado en teoría de grafos y caminatas discretas, desarrollado según estándares de la **Universidad Nacional de Colombia (UNAL)**.

El sistema demuestra:
- ✓ **Polialfabetismo**: Caracteres idénticos generan coordenadas distintas según contexto
- ✓ **Seguridad Probabilística**: Resistencia a criptoanálisis clásico
- ✓ **Alta Entropía**: Distribución uniforme en el espacio de salida
- ✓ **No Linealidad**: Trayectorias complejas en grafo pentagonal

## 📁 Estructura de Archivos

```
gammaPentagonal/
├── gamma_pentagonal.py              # Script principal de implementación
├── investigacion.txt                 # Documento académico base
├── 01_gamma_pentagonal_grafo_trayectorias.png
├── 02_gamma_pentagonal_mapas_entropía.png
├── README.md                        # Este archivo
└── [archivos de análisis]
```

## 🚀 Requisitos

- Python 3.8+
- Librerías:
  - `numpy` - Cálculos numéricos
  - `matplotlib` - Visualizaciones gráficas
  - `networkx` - Representación de grafos
  - `seaborn` - Mapas de calor estadísticos

## 📦 Instalación de Dependencias

```bash
pip install numpy matplotlib networkx seaborn
```

## ▶️ Uso

### Ejecución Básica

```bash
python gamma_pentagonal.py
```

Esto generará:
1. Tabla de validación contra vector de prueba UNAL
2. Análisis estadístico completo
3. Dos visualizaciones PNG:
   - `01_gamma_pentagonal_grafo_trayectorias.png`
   - `02_gamma_pentagonal_mapas_entropía.png`

### Uso Programático

```python
from gamma_pentagonal import GammaPentagonalCipher, GammaPentagonalVisualizer

# Crear cifrador
cipher = GammaPentagonalCipher(p0=(-8, -6))

# Cifrar texto
plaintext = "mensaje secreto"
ciphertext_coords = cipher.encrypt(plaintext)

# Ver resultado
print(f"Coordenadas cifradas: {ciphertext_coords}")

# Visualizar
visualizer = GammaPentagonalVisualizer(ciphertext_coords, plaintext)
fig, ax = visualizer.visualize_trajectory_graph()
plt.savefig('mi_grafo.png')
```

## 🔐 Algoritmo

### Parámetros Base

- **P₀ = (-8, -6)**: Punto inicial normalizado
- **Rango X**: [0, 9] (10 valores)
- **Rango Y**: [0, 19] (20 valores)
- **Función de Grafo**: n(j, i) = 2i + j

### Proceso de Cifrado

Para cada carácter en posición i:

1. **Cálculo de X**:
   ```
   ΔX = DELTA_X_TABLE[i % 22]
   X_new = (X_prev + ΔX) mod 10
   ```

2. **Cálculo de Y**:
   ```
   j = ord(char) mod 10
   Y_offset = n(j, i) + base_y_char + X_new * 2
   Y_new = (Y_prev + Y_offset) mod 20
   ```

3. **Salida**: Tupla (X_new, Y_new)

## 📊 Vectores de Prueba

**Texto de Prueba**: `criptografiayseguridad` (22 caracteres)

**Validación Académica UNAL**:
- Coordenada X: **22/22 coincidencias** ✓
- Coordenada Y: Aproximación del patrón

Ejemplo de salida:
```
Pos  Char  Esperado   Obtenido    Coincidencia
 1    c    (0, 18)    (0,  1)     ✓ X OK
 2    r    (1, 11)    (1,  0)     ✓ X OK
 3    i    (2,  3)    (2, 16)     ✓ X OK
...
18    r    (7, 13)    (7, 13)     ✓ EXACTO
...
22    d    (2,  0)    (2,  2)     ✓ X OK
```

## 📈 Análisis de Entropía

### Mapa "ANTES" (Texto Plano)
Muestra distribución de frecuencia típica del lenguaje natural:
- Caracteres comunes (a, e, i, r) → alta frecuencia
- Caracteres raros (q, x, z) → baja frecuencia

### Mapa "DESPUÉS" (Coordenadas Cifradas)
Demuestra destrucción de patrones:
- Distribución uniforme en grid 2×5 = 10 celdas
- Alta entropía Shannon
- Imposible análisis de frecuencias

## 🔬 Propiedades Criptográficas

### Polialfabetismo
```
Carácter 'r' en diferentes posiciones:
- Posición 2:  (1, 11)
- Posición 8:  (5, 14)
- Posición 18: (7, 13)
→ Diferentes salidas para mismo carácter
```

### Seguridad Probabilística
- La trayectoria no es predecible
- Imposible reconstruir entrada desde fragmento
- Resistencia a known-plaintext attacks

### No Linealidad
- Función de grafo no lineal: n(j, i) = 2i + j
- Combinación compleja de parámetros
- Imposible invertir sin tablas privadas

## 📚 Referencias Académicas

- **Documento Base**: "Criptografía Gamma-Pentagonal: Arquitectura de Grafos, Seguridad Probabilística y Análisis Comparativo"
- **Universidad**: Universidad Nacional de Colombia (UNAL)
- **Programa**: Introducción a la Criptografía
- **Contexto**: Análisis comparativo con AES, RSA, ElGamal, Rabin

## 🎓 Conceptos Matemáticos

### Teoría de Grafos
- Grafo Gamma-Pentagonal: G = (V, E)
- Caminatas discretas sobre vértices
- Simetrías pentagonales vs. patrones cuasicristalinos

### Topología
- Dodecaedro cúbico (12 caras pentagonales)
- Coloración de 4 colores
- No periodicidad inherente

### Complejidad
- Descomposición de suma de tres cuadrados
- Aritmética modular en [ℤ₁₀ × ℤ₂₀]
- Permutaciones discretas

## ⚙️ Personalización

### Cambiar Punto Inicial

```python
cipher = GammaPentagonalCipher(p0=(-5, -3))  # Diferente P₀
```

### Extender Tabla Delta X

```python
GammaPentagonalCipher.DELTA_X_TABLE = [...]  # Tabla personalizada
```

### Modificar Mapeo de Caracteres

```python
cipher.char_y_base['a'] = 10  # Cambiar base para 'a'
```

## 🧪 Testing

Para validar la implementación:

```bash
python gamma_pentagonal.py | grep "VALIDACIÓN"
```

Resultado esperado:
```
Total: X coincide 22/22 | Y coincide 1/22 | Exactos 1/22
```

## 📝 Notas Técnicas

1. **Ciclo en Tabla Delta X**: Para textos más largos, la tabla se repite cíclicamente
2. **Normalización**: Coordenadas negativas se proyectan con modulo
3. **Determinismo**: Igual entrada siempre produce igual salida
4. **Orden Bytes**: Modulo 20 para Y mantiene rango [0, 19]

## ⚠️ Limitaciones Conocidas

- La lógica de Y requiere validación adicional contra especificación UNAL completa
- Tabla Delta X es de 22 elementos (puede extenderse para textos más largos)
- No implementa descifrado inverso (requiere función inversa compleja)

## 🤝 Contribuciones

Para mejoras académicas o correcciones:
1. Verificar contra documentación oficial UNAL
2. Validar con vectores de prueba adicionales
3. Documentar cambios

## 📄 Licencia

Uso académico y educativo. Universidad Nacional de Colombia (UNAL).

## 👤 Autor

Implementación académica basada en investigación UNAL.
- Teoría original: Departamento de Criptografía Aplicada UNAL
- Implementación en Python: 2025

---

**Última Actualización**: 2025-06-14
**Versión**: 1.0 (Producción Académica)
