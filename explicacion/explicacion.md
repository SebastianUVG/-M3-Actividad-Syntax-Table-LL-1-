```
CALCULO PASO A PASO DE CONJUNTOS FIRST Y FOLLOW

PASO 1: Definicion de Gramatica

DEFINICION DE GRAMATICA

Simbolo inicial: E

E -> T E'
E' -> + T E' | eps
F -> ( E ) | id
T -> F T'
T' -> * F T' | eps



Desglose de producciones:

E:
  T E'       -> ['T', "E'"]

E':
  + T E'     -> ['+', 'T', "E'"]
  eps        -> ['eps']

F:
  ( E )      -> ['(', 'E', ')']
  id         -> ['i', 'd']

T:
  F T'       -> ['F', "T'"]

T':
  * F T'     -> ['*', 'F', "T'"]
  eps        -> ['eps']


PASO 2: Calculo de Conjuntos FIRST (Iteracion de Punto Fijo)

Algoritmo:
  1. Inicializa todos los FIRST(A) = {} para cada no-terminal A
  2. Repite hasta que no haya cambios:
     - Para cada produccion A -> X1X2...Xn:
       - Para i = 1 a n:
         - Anade FIRST(Xi) - {eps} a FIRST(A)
         - Si eps no esta en FIRST(Xi), detente
       - Si todos los Xi pueden derivar eps, anade eps a FIRST(A)

Calculando...

Resultado:
  FIRST(E  ) = {'i', '('}
  FIRST(E' ) = {'+', 'eps'}
  FIRST(F  ) = {'i', '('}
  FIRST(T  ) = {'(', 'i'}
  FIRST(T' ) = {'eps', '*'}

Analisis:
  - Los terminales aparecen en conjuntos FIRST porque inician producciones directamente
  - 'eps' aparece cuando un no-terminal puede derivar epsilon
    * E' puede estar vacio, entonces E' -> eps causa FIRST(E') = {+, eps}
    * T' puede estar vacio, entonces T' -> eps causa FIRST(T') = {*, eps}
  - Ningun no-terminal tiene 'eps' directamente como inicio de produccion


PASO 3: Calculo de Conjuntos FOLLOW (Usando conjuntos FIRST)


Algoritmo:
  1. Inicializa:
     - FOLLOW(S) = {$} donde S es el simbolo inicial
     - FOLLOW(A) = {} para todos los otros no-terminales
  2. Repite hasta que no haya cambios:
     - Para cada produccion A -> aBb:
       - Anade FIRST(b) - {eps} a FOLLOW(B)
       - Si eps en FIRST(b), anade FOLLOW(A) a FOLLOW(B)

Calculando...

Resultado:
  FOLLOW(E  ) = {'$', ')'}
  FOLLOW(E' ) = {'$', ')'}
  FOLLOW(F  ) = {'+', ')', '$', '*'}
  FOLLOW(T  ) = {'+', '$', ')'}
  FOLLOW(T' ) = {'+', '$', ')'}


PASO 4: Analisis Detallado


Por que E tiene FOLLOW(E) = {), $}?
  - E aparece en: F -> ( E ) y E' (fin de E -> T E')
  - En F -> ( E ): el simbolo despues de E es )
  - En nivel superior: E es el inicio, entonces $ (fin de entrada) lo sigue

Por que T tiene FOLLOW(T) = {), +, $}?
  - T aparece en: E -> T E'
  - Despues de T viene E'
  - FIRST(E') = {+, eps}, entonces + esta en FOLLOW(T)
  - Como eps en FIRST(E'), FOLLOW(E) tambien esta en FOLLOW(T)
  - FOLLOW(E) = {), $}, entonces FOLLOW(T) incluye ), $
  - Final: FOLLOW(T) = {+, ), $}

Por que F tiene FOLLOW(F) = {), *, +, $}?
  - F aparece en: T -> F T'
  - Despues de F viene T'
  - FIRST(T') = {*, eps}, entonces * esta en FOLLOW(F)
  - Como eps en FIRST(T'), FOLLOW(T) tambien esta en FOLLOW(F)
  - FOLLOW(T) = {), +, $}, entonces FOLLOW(F) incluye ), +, $
  - Final: FOLLOW(F) = {*, ), +, $}

Por que E' y T' tienen epsilon?
  - E' -> +T E' | eps: E' puede ser epsilon (vacio)
  - T' -> *F T' | eps: T' puede ser epsilon (vacio)
  - Estos se usan para manejar operaciones opcionales
  - E = T(E') significa: expresion = termino, posiblemente seguido por +termino
  - Esto evita recursion izquierda que romperia el analisis LL(1)


PASO 5: Aplicacion al Analisis


Los conjuntos FIRST se usan para:
  - Decidir cual produccion usar cuando se ve un terminal
  - Al analizar E y ver 'id' o '(': usar E -> T E'
  - Al analizar E' y ver '+': usar E' -> + T E'
  - Al analizar E' y ver ')' o '$': usar E' -> eps

Los conjuntos FOLLOW se usan para:
  - Decidir cual produccion cuando tenemos producciones epsilon
  - Al analizar E' y ver ')' (que esta en FOLLOW(E')): usar E' -> eps
  - Esto permite al analizador omitir operaciones opcionales elegantemente


```
