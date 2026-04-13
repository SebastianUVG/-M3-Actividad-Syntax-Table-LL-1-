# Análisis de Conjuntos FIRST, FOLLOW y Tabla de Análisis Sintáctico Predictivo

## Descripción General de la Actividad

Esta actividad implementa los algoritmos de cálculo de conjuntos FIRST y FOLLOW para gramáticas libres de contexto (CFG), junto con la construcción de tablas de análisis sintáctico predictivo. Estos son algoritmos fundamentales en el diseño de compiladores y análisis sintáctico.

**Curso**: Diseño de Lenguajes de Programación  
**Actividad**: Actividad Práctica sobre FIRST, FOLLOW y Tablas de Análisis Sintáctico

---

## Estructura del Proyecto

```
.
├── grammar.py                              # Representación y definición de gramáticas
├── first_follow.py                         # Cálculo de conjuntos FIRST y FOLLOW
├── parsing_table.py                        # Construcción de tabla LL(1)
├── main.py                                 # Script de demostración
├────explicacion
├              ├─ explicacion.md           # Explicación de algoritmo
├              └─explicacion_tabla.md      # Explicacion de algoritmo de tabla
├── EXPLICACION_TABLA_ANALISIS.md           # Explicación de tabla de análisis predictivo
└── README.md                               # Este archivo
```

### Descripción de Módulos

#### `grammar.py`
- **Clase Grammar**: Representa una gramática libre de contexto con producciones
- **Métodos**:
  - `add_production()`: Añade producciones con soporte para epsilon
  - `extract_terminals()`: Identifica automáticamente todos los símbolos terminales
  - `get_all_symbols()`: Divide producciones en símbolos individuales
  - `display()`: Muestra la gramática en formato legible
- **Funciones auxiliares**: Gramáticas predefinidas para pruebas

#### `first_follow.py`
- **Clase FirstFollowAnalyzer**: Implementa el algoritmo principal
- **Algoritmo de cálculo FIRST**:
  - Para no-terminal A: recopila terminales del primer símbolo de cada producción
  - Si una producción puede derivar epsilon, lo incluye
  - Itera hasta alcanzar punto fijo
- **Algoritmo de cálculo FOLLOW**:
  - Comienza con $ en FOLLOW(símbolo_inicial)
  - Para cada producción A → αBβ: añade FIRST(β) - {eps} a FOLLOW(B)
  - Si ε ∈ FIRST(β): añade FOLLOW(A) a FOLLOW(B)
  - Itera hasta alcanzar punto fijo

#### `parsing_table.py`
- **Clase ParsingTable**: Construye tablas de análisis LL(1)
- **Algoritmo de construcción de tabla**:
  - Para cada producción A → α:
    - Para cada terminal a en FIRST(α): añade A → α a M[A,a]
    - Si ε ∈ FIRST(α): para cada b en FOLLOW(A), añade A → α a M[A,b]
- **Análisis LL(1)**:
  - Detecta conflictos (múltiples producciones en una entrada)
  - Reporta si la gramática es LL(1) sin conflictos

---

## Documentación de Explicación

### EXPLICACION_TABLA_ANALISIS.md

Este archivo contiene una explicación detallada y paso a paso sobre:

1. **¿Qué es la Tabla de Análisis Predictivo?**
   - Estructura (filas, columnas, entradas)
   - Propósito en análisis LL(1)

2. **Algoritmo de Construcción**
   - Pasos requeridos
   - Algoritmo principal
   - Detección de conflictos

3. **Ejemplo Paso a Paso**
   - Construcción completa de tabla para Expresiones Aritméticas
   - Cálculo de cada entrada
   - Tabla final

4. **Verificación de LL(1)**
   - Requisitos para ser LL(1)
   - Ejemplo de conflicto
   - Cómo identificar problemass

5. **Uso de la Tabla en Análisis**
   - Algoritmo de análisis predictivo
   - Ejemplo de ejecución paso a paso
   - Interpretación de resultados

6. **Resumen Visual**
   - Diagrama del proceso completo

---

## Detalles del Algoritmo

### Algoritmo FIRST

**Entrada**: Gramática G  
**Salida**: Conjuntos FIRST para todos los no-terminales

```
Algoritmo FIRST:
  Para cada no-terminal A:
    FIRST(A) = {}
  
  Repetir hasta que no haya cambios:
    Para cada produccion A -> X1X2...Xn:
      Para i = 1 a n:
        si X1 en FIRST(X1):
          FIRST(A) <- FIRST(A) union (FIRST(Xi) - {eps})
        si eps no en FIRST(Xi):
          romper
      si todos los Xi pueden derivar eps:
        FIRST(A) <- FIRST(A) union {eps}
```

### Algoritmo FOLLOW

**Entrada**: Gramática G con conjuntos FIRST ya calculados  
**Salida**: Conjuntos FOLLOW para todos los no-terminales

```
Algoritmo FOLLOW:
  FOLLOW(S) = {$}  donde S es simbolo inicial
  Para cada no-terminal A != S:
    FOLLOW(A) = {}
  
  Repetir hasta que no haya cambios:
    Para cada produccion A -> aBb:
      FOLLOW(B) <- FOLLOW(B) union (FIRST(b) - {eps})
      si eps en FIRST(b):
        FOLLOW(B) <- FOLLOW(B) union FOLLOW(A)
```

---

## Gramáticas Probadas

### Gramática 1: Expresiones Aritméticas (LL(1) ✓)

**Propósito**: Gramática clásica para expresiones aritméticas con precedencia de operadores.

**Definición**:
```
E  -> T E'
E' -> + T E' | eps
T  -> F T'
T' -> * F T' | eps
F  -> ( E ) | id
```

**Por qué se eligió**: 
- Ejemplo canónico en cursos de diseño de compiladores
- Demuestra cómo se resuelve el problema del operador flotante
- Muestra cómo manejar asociatividad y precedencia
- Comprobada como gramática LL(1)

**Características clave**:
- Formulación sin recursión izquierda, adecuada para análisis predictivo
- Maneja operaciones de adición y multiplicación
- Soporta paréntesis para agrupación
- Todas las producciones tienen conjuntos FIRST únicos

**Conjuntos FIRST**:
- FIRST(E) = {id, (}
- FIRST(E') = {+, eps}
- FIRST(T) = {id, (}
- FIRST(T') = {*, eps}
- FIRST(F) = {id, (}

**Conjuntos FOLLOW**:
- FOLLOW(E) = {), $}
- FOLLOW(E') = {), $}
- FOLLOW(T) = {), +, $}
- FOLLOW(T') = {), +, $}
- FOLLOW(F) = {), *, +, $}

---

### Gramática 2: Expresiones Booleanas (LL(1) ✓)

**Propósito**: Gramática para expresiones booleanas con operadores AND y OR, con estructura similar a la aritmética.

**Definición**:
```
E  -> T E'
E' -> or T E' | eps
T  -> F T'
T' -> and F T' | eps
F  -> true | false | ( E )
```

**Por qué se eligió**: 
- Refleja la estructura exacta de la gramática aritmética
- Demuestra cómo el mismo patrón funciona para diferentes dominios
- Ambos operadores (or/and) son binarios, con precedencia clara
- Gramática LL(1) comprobada sin conflictos

**Características clave**:
- OR tiene menor precedencia que AND (como + vs * en aritmética)
- Soporta paréntesis para agrupación
- Símbolos terminales limpios y simples

**Conjuntos FIRST**:
- FIRST(E) = {true, false, (}
- FIRST(E') = {or, eps}
- FIRST(T) = {true, false, (}
- FIRST(T') = {and, eps}
- FIRST(F) = {true, false, (}

**Conjuntos FOLLOW**:
- FOLLOW(E) = {), $}
- FOLLOW(E') = {), $}
- FOLLOW(T) = {or, ), $}
- FOLLOW(T') = {or, ), $}
- FOLLOW(F) = {and, or, ), $}

---

### Gramática 3: Listas de Números (LL(1) ✓)

**Propósito**: Gramática simple para listas de números separados por comas.

**Definición**:
```
L  -> num L'
L' -> , num L' | eps
```

**Por qué se eligió**:
- Gramática más simple posible (solo 2 no-terminales)
- Aplicación del mundo real: análisis de secuencias/arrays
- Demuestra producciones epsilon en contexto
- Perfecta para entender el uso de conjuntos FOLLOW

**Características clave**:
- Estructura lineal
- Epsilon para manejar cola vacía
- Operador terminal único (coma)

**Conjuntos FIRST**:
- FIRST(L) = {num}
- FIRST(L') = {,, eps}

**Conjuntos FOLLOW**:
- FOLLOW(L) = {$}
- FOLLOW(L') = {$}

---

## Resumen

Las tres gramáticas han sido probadas y analizadas:

| Gramática | Tipo | Estado LL(1) | Terminales | No-terminales |
|-----------|------|--------------|-----------|---------------|
| Expresiones Aritméticas | Operadores | LL(1) ✓ | id, +, *, (, ) | E, E', T, T', F |
| Expresiones Booleanas | Operadores | LL(1) ✓ | true, false, or, and, (, ) | E, E', T, T', F |
| Listas de Números | Secuencias | LL(1) ✓ | num, , | L, L' |

**Observaciones Clave**:
- Las tres gramáticas siguen el mismo patrón: estructura sin recursión izquierda
- Las producciones epsilon se usan estratégicamente para elementos opcionales
- Sin conflictos en ninguna gramática - todas son adecuadas para análisis LL(1)
- Complejidad decreciente (de 5 no-terminales a 2)

---

## Ejecución del Programa

### Requisitos Previos
- Python 3.7 o superior
- Sin dependencias externas

### Scripts Disponibles

**1. Análisis Principal** (Las 3 gramáticas con resultados)
```bash
python main.py
```

**2. Explicación Paso a Paso** (Tutorial educativo de FIRST/FOLLOW)
```bash
python explain.py
```

**3. Ejemplos** (5 ejemplos diferentes de análisis)
```bash
python examples.py
```

### Salida
Los programas mostrarán:
1. **Definición de Gramática**: Todas las producciones
2. **Conjuntos FIRST**: Símbolos que pueden iniciar cada no-terminal
3. **Conjuntos FOLLOW**: Símbolos que pueden seguir cada no-terminal
4. **Tabla de Análisis**: Tabla de análisis LL(1) predictivo (si aplica)
5. **Análisis LL(1)**: Si la gramática es LL(1) y dónde ocurren conflictos (si los hay)

---

## Detalles de Implementación

### Representación de Símbolos
- **Terminales**: Identificadores sensibles a mayúsculas (id, num, +, *, etc.)
- **No-terminales**: Variables que comienzan con letra, pueden incluir apóstrofes (E', T')
- **Producción Epsilon**: Representada como `eps`
- **Marcador de fin de entrada**: `$`

### Complejidad de Algoritmos
- **Cálculo FIRST**: O(n * m * r) donde n = no-terminales, m = producciones máximas por NT, r = longitud máxima de producción
- **Cálculo FOLLOW**: Similar a FIRST, depende del tamaño de la gramática
- **Construcción de tabla**: O(n * m * t) donde t = número de terminales

### Casos Especiales Manejados
- Producciones epsilon (creando no-terminales anulables)
- Múltiples producciones alternativas (A -> α | β | γ)
- Producciones recursivas (directas e indirectas)
- Terminales que aparecen en múltiples producciones
- Cadenas de no-terminales y clausura transitiva para epsilon

---

## Uso de Ejemplo

### Crear Gramáticas Personalizadas

```python
from grammar import Grammar
from first_follow import FirstFollowAnalyzer
from parsing_table import ParsingTable

# Crear una nueva gramática
g = Grammar()
g.add_production_explicit('S', ['a A b', 'b B a'])
g.add_production_explicit('A', ['eps', 'a'])
g.add_production_explicit('B', ['eps', 'b'])

# Extrae terminales
g.extract_terminals()
g.display()

# Calcula FIRST y FOLLOW
analyzer = FirstFollowAnalyzer(g)
analyzer.calculate_first()
analyzer.calculate_follow()
analyzer.display_first_follow()

# Construye tabla de análisis
table = ParsingTable(g, analyzer)
table.build_table()
table.display_table()
table.display_ll1_analysis()
```

---

## Documentación

### Decisiones de Diseño

1. **Iteración de punto fijo**: Utilizada para cálculos FIRST y FOLLOW porque:
   - Natural para manejar gramáticas recursivas
   - Fácil de implementar y verificar corrección
   - Rendimiento aceptable para gramáticas educativas

2. **Representación de Producciones como Cadenas**: 
   - Simple y legible
   - Fácil de analizar manualmente
   - Adecuada para gramáticas pequeñas a medianas

3. **Representación de Epsilon como 'eps'**:
   - Evita problemas Unicode en diferentes plataformas
   - Compatible con ASCII para todos los terminales

4. **Objetos Analizadores Separados**:
   - Separación clara de responsabilidades
   - Hacer código reutilizable y testeable

### Mejoras Potenciales

1. **Optimización de Gramática**: Eliminación de recursión izquierda y factorización izquierda
2. **Soporte para Gramáticas Grandes**: Usar entrada tokenizada para gramáticas complejas
3. **Generación de Árbol de Síntaxis**: Implementar analizador predictivo que construya árboles
4. **Recuperación de Errores**: Implementar estrategias de recuperación de errores
5. **Rendimiento**: Optimizar para gramáticas muy grandes

---

## Referencias

- **Teoría de Diseño de Compiladores**: 
  - Aho, Lam, Sethi, Ullman - "Compilers: Principles, Techniques, and Tools" (Libro del Dragón)
  - Secciones sobre análisis sintáctico, gramáticas LL y análisis predictivo

- **Gramáticas LL(1)**:
  - Definición y propiedades
  - Condiciones para analizabilidad LL(1)
  - Transformación de gramáticas para LL(1)

- **Algoritmos de Análisis**:
  - Análisis descendente recursivo
  - Análisis predictivo dirigido por tabla
  - Manejo de errores y recuperación

---

## Autor y Fecha

- **Creado**: Abril 2026
- **Curso**: Diseño de Lenguajes de Programación
- **Estudiante**: SebastianUVG

---
