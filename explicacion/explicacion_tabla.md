# Explicación de la Tabla de Análisis Sintáctico Predictivo

## ¿Qué es la Tabla de Análisis Predictivo?

La tabla de análisis predictivo es una estructura de datos que se utiliza en el análisis sintáctico **LL(1)** para automatizar la decisión de qué producción usar al analizar una gramática.

**Estructura:**
- **Filas**: No-terminales (A, B, C, etc.)
- **Columnas**: Terminales (a, b, +, *, etc.) + símbolo fin ($)
- **Entradas**: Producciones a usar (ej: A → α)

```
        a       b       $
A   A→aB    A→bC    error
B   error   B→b     B→ε
```

---

## Algoritmo de Construcción

### Paso 1: Entrada Requerida

Necesitas tener calculados previamente:
- Conjuntos **FIRST** de todos los no-terminales
- Conjuntos **FOLLOW** de todos los no-terminales

### Paso 2: Algoritmo Principal

Para cada producción **A → α** en la gramática:

```
1. Calcula FIRST(α)
   
2. Para cada terminal a en FIRST(α):
   - Si a ≠ ε:
     Anade A → α a la entrada M[A, a]
   
3. Si ε ∈ FIRST(α):
   - Para cada terminal b en FOLLOW(A):
     Anade A → α a la entrada M[A, b]
```

### Paso 3: Detección de Conflictos

- Si una entrada M[A, a] tiene **más de una producción** → **CONFLICTO**
- Si hay conflictos → La gramática **NO es LL(1)**
- Si NO hay conflictos → La gramática **ES LL(1)**

---

## Ejemplo Paso a Paso: Expresiones Aritméticas

### Gramática
```
E  → T E'
E' → + T E' | ε
T  → F T'
T' → * F T' | ε
F  → ( E ) | id
```

### Conjuntos FIRST y FOLLOW (Ya Calculados)

**FIRST:**
- FIRST(E) = {(, id}
- FIRST(E') = {+, ε}
- FIRST(T) = {(, id}
- FIRST(T') = {*, ε}
- FIRST(F) = {(, id}

**FOLLOW:**
- FOLLOW(E) = {), $}
- FOLLOW(E') = {), $}
- FOLLOW(T) = {+, ), $}
- FOLLOW(T') = {+, ), $}
- FOLLOW(F) = {*, +, ), $}

### Construcción de la Tabla

#### Producción 1: **E → T E'**

1. FIRST(T E') = FIRST(T) = {(, id}
2. Anade E → T E' a:
   - M[E, (]
   - M[E, id]

**Resultado:**
```
        (           )       *       +       id      $
...
E   E→TE'                              E→TE'
...
```

#### Producción 2: **E' → + T E'**

1. FIRST(+ T E') = {+}
2. Anade E' → + T E' a:
   - M[E', +]

**Resultado:**
```
        (       )       *       +       id      $
...
E'                      E'→+TE'
```

#### Producción 3: **E' → ε**

1. FIRST(ε) = {ε}
2. ε ∈ FIRST(ε) → Anade E' → ε a FOLLOW(E') = {), $}
3. Anade E' → ε a:
   - M[E', )]
   - M[E', $]

**Resultado:**
```
        (       )       *       +       id      $
...
E'              E'→ε            E'→+TE'         E'→ε
```

#### Producción 4: **T → F T'**

1. FIRST(F T') = FIRST(F) = {(, id}
2. Anade T → F T' a:
   - M[T, (]
   - M[T, id]

**Resultado:**
```
        (           )       *       +       id      $
...
T   T→FT'                              T→FT'
```

#### Producción 5: **T' → * F T'**

1. FIRST(* F T') = {*}
2. Anade T' → * F T' a:
   - M[T', *]

**Resultado:**
```
        (       )       *       +       id      $
...
T'              T'→*FT'
```

#### Producción 6: **T' → ε**

1. FIRST(ε) = {ε}
2. ε ∈ FIRST(ε) → Anade T' → ε a FOLLOW(T') = {+, ), $}
3. Anade T' → ε a:
   - M[T', +]
   - M[T', )]
   - M[T', $]

**Resultado:**
```
        (       )       *       +       id      $
...
T'              T'→ε        T'→ε    T'→ε
```

#### Producción 7: **F → ( E )**

1. FIRST(( E )) = {(}
2. Anade F → ( E ) a:
   - M[F, (]

**Resultado:**
```
        (               )       *       +       id      $
...
F   F→(E)                                  
```

#### Producción 8: **F → id**

1. FIRST(id) = {id}
2. Anade F → id a:
   - M[F, id]

**Resultado:**
```
        (       )       *       +       id      $
...
F   F→(E)                       F→id
```

### Tabla Final Completa

```
        (           )       *           +       id      $
E   E→TE'       error   error       error   E→TE'   error
E'  error       E'→ε     error       E'→+TE' error   E'→ε
T   T→FT'       error   error       error   T→FT'   error
T'  error       T'→ε     T'→*FT'     T'→ε    error   T'→ε
F   F→(E)       error   error       error   F→id    error
```

---

## Verificación de LL(1)

Para que una gramática sea **LL(1)**:

```
Requisito: Cada entrada M[A, a] tiene como máximo 1 producción
```

### Verificación en el Ejemplo

Revisamos cada entrada:
- ✓ M[E, (] = {E → TE'}  (1 producción)
- ✓ M[E, id] = {E → TE'}  (1 producción)
- ✓ M[E', )] = {E' → ε}  (1 producción)
- ✓ M[E', +] = {E' → +TE'}  (1 producción)
- ✓ M[E', $] = {E' → ε}  (1 producción)
- (y todas las demás...)

**Resultado: SIN CONFLICTOS → LA GRAMÁTICA ES LL(1)** ✓

---

## Ejemplo de Conflicto (Gramática NO LL(1))

### Gramática con Conflicto

```
E → T | T + E
```

Supongamos FIRST(T) = {a} y FOLLOW(E) = {$}

**Producciones:**

1. **E → T**
   - FIRST(T) = {a} → M[E, a] = E → T

2. **E → T + E**
   - FIRST(T + E) = {a} → M[E, a] = E → T + E

**Resultado:**
```
M[E, a] = {E → T, E → T + E}  ← CONFLICTO! (2 producciones)
```

**Conclusión: NO es LL(1)** ✗

---

## Uso de la Tabla en Análisis Sintáctico

Una vez construida, la tabla se usa así:

### Algoritmo de Análisis Predictivo

```
Stack = [E, $]          (E es no-terminal inicial)
Entrada = "id + id $"
Posicion = 0            (señala 'id')

Mientras Stack no esté vacío:
    Cima = Stack.pop()
    
    Si Cima es terminal:
        Si Cima == Entrada[Posicion]:
            Avanza Posicion
        Sino:
            ERROR
    
    Si Cima es no-terminal:
        Terminal_Actual = Entrada[Posicion]
        Produccion = M[Cima, Terminal_Actual]
        
        Si Produccion existe:
            Push(Produccion en Stack)
        Sino:
            ERROR
```

### Ejemplo de Ejecución

```
Entrada: id + id $

Paso 1: Stack=[E,$], Lee 'id'
        M[E, id] = E → TE'
        Stack=[TE',$]

Paso 2: Stack=[TE',$], Lee 'id'
        M[T, id] = T → FT'
        Stack=[FT'E',$]

Paso 3: Stack=[FT'E',$], Lee 'id'
        M[F, id] = F → id
        Stack=[idT'E',$]

Paso 4: Stack=[idT'E',$], Lee 'id'
        Cima='id', terminal == entrada → advance
        Stack=[T'E',$], Lee '+'

Paso 5: Stack=[T'E',$], Lee '+'
        M[T', +] = T' → ε
        Stack=[E',$]

... (continúa hasta aceptar o rechazar)
```

---

## Tablas de Análisis en Este Proyecto

### Características Especiales

1. **Sin Conflictos**: Las 3 gramáticas usadas son todas LL(1)
2. **Formato Legible**: La salida muestra claramente cada entrada
3. **Detección Automática**: El programa detecta automáticamente si es LL(1)

### Cómo Interpretar la Salida

```
          $              (              )              *              +              id             
E         error          E->T E'        error          error          error          E->T E'        
E'        E'->eps        error          E'->eps        error          E'->+ T E'     error          
```

**Lectura:**
- Fila E, Columna ( → Producción: E → T E'
- Fila E', Columna + → Producción: E' → + T E'
- Fila E', Columna $ → Producción: E' → ε (epsilon)
- Fila E, Columna ) → error (no hay producción válida aquí)

---

## Resumen del Proceso

```
┌─────────────────────────────────────┐
│  Gramática Original                 │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│  1. Calcular FIRST                  │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│  2. Calcular FOLLOW                 │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│  3. Para cada producción:           │
│     - Si a en FIRST(α): M[A,a]=α   │
│     - Si ε en FIRST(α):            │
│       Para cada b en FOLLOW(A):    │
│       M[A,b] = α                   │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│  4. Verificar conflictos            │
│     ¿Hay M[A,a] con >1 producción? │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┐
        ↓             ↓
    [NO]          [SÍ]
    LL(1)         NO LL(1)
```

---

## Conclusión

La tabla de análisis predictivo es el corazón del análisis LL(1). Convierte el cálculo abstracto de FIRST y FOLLOW en una estructura concreta que puede ser usada por un analizador syntáctico automático.

**Ventajas:**
- Determina automáticamente qué regla usar
- Detecta ambigüedades en la gramática
- Permite análisis eficiente en una sola pasada

**Limitaciones:**
- Solo funciona con gramáticas LL(1) sin conflictos
- Requiere calcular previamente FIRST y FOLLOW
- No puede manejar todas las gramáticas libres de contexto
