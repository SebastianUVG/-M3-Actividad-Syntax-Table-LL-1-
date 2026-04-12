"""
Construccion de tabla de analisis sintactico predictivo para gramaticas LL(1).

La tabla de analisis M[A, a] contiene:
- La produccion A -> α a usar al analizar no-terminal A con terminal a
- Si M[A, a] es indefinido, es un error
- Si M[A, a] tiene conflictos (multiples entradas), la gramatica no es LL(1)

Algoritmo de construccion de tabla:
Para cada produccion A -> α:
    1. Para cada terminal a en FIRST(α), anade A -> α a M[A, a]
    2. Si ε en FIRST(α), para cada b en FOLLOW(A), anade A -> α a M[A, b]
    3. Si ε en FIRST(α) y $ en FOLLOW(A), anade A -> α a M[A, $]
"""

from collections import defaultdict


class ParsingTable:
    """Construye y administra tablas de analisis predictivo para gramaticas LL(1)."""

    def __init__(self, grammar, first_follow_analyzer):
        """
        Inicializa la tabla de analisis.

        Args:
            grammar: Objeto Grammar
            first_follow_analyzer: FirstFollowAnalyzer con conjuntos FIRST y FOLLOW calculados
        """
        self.grammar = grammar
        self.analyzer = first_follow_analyzer
        self.table = defaultdict(lambda: defaultdict(list))  # table[no_terminal][terminal]
        self.conflicts = []  # Lista de (no_terminal, terminal) donde ocurren conflictos
        self.is_ll1 = True
        self.all_terminals = set()
        self.epsilon = 'eps'
        self.end_marker = '$'

    def build_table(self):
        """
        Construye la tabla de analisis predictivo.

        Returns:
            Diccionario que representa la tabla de analisis
        """
        self._collect_terminals()

        # Para cada produccion
        for non_terminal, productions in self.grammar.productions.items():
            for production in productions:
                self._add_production_to_table(non_terminal, production)

        return dict(self.table)

    def _collect_terminals(self):
        """Recopila todos los terminales de los conjuntos FIRST y FOLLOW."""
        self.all_terminals.add(self.end_marker)

        for first_set in self.analyzer.first_sets.values():
            for terminal in first_set:
                if terminal != self.epsilon:
                    self.all_terminals.add(terminal)

        for follow_set in self.analyzer.follow_sets.values():
            self.all_terminals.update(follow_set)

    def _add_production_to_table(self, non_terminal, production):
        """
        Anade una produccion a la tabla de analisis siguiendo el algoritmo.

        Args:
            non_terminal: No-terminal del lado izquierdo
            production: Produccion del lado derecho
        """
        # Obtiene FIRST de la produccion
        symbols = self.grammar.get_all_symbols(production)
        first_of_prod = self.analyzer._first_of_sequence(symbols)

        # Anade entradas para terminales en FIRST(produccion) - {epsilon}
        for terminal in first_of_prod:
            if terminal != self.epsilon:
                self._add_entry(non_terminal, terminal, production)

        # Si epsilon en FIRST(produccion), anade entradas para FOLLOW(no_terminal)
        if self.epsilon in first_of_prod:
            for terminal in self.analyzer.follow_sets.get(non_terminal, set()):
                self._add_entry(non_terminal, terminal, production)

    def _add_entry(self, non_terminal, terminal, production):
        """
        Anade una entrada a la tabla, detectando conflictos.

        Args:
            non_terminal: Fila (no-terminal)
            terminal: Columna (terminal)
            production: Produccion a anadir
        """
        if production not in self.table[non_terminal][terminal]:
            if self.table[non_terminal][terminal]:
                # Conflicto detectado
                self.is_ll1 = False
                if (non_terminal, terminal) not in self.conflicts:
                    self.conflicts.append((non_terminal, terminal))

            self.table[non_terminal][terminal].append(production)

    def display_table(self):
        """Muestra la tabla de analisis en un formato legible."""
        print("\n" + "="*100)
        print("TABLA DE ANALISIS PREDICTIVO")
        print("="*100 + "\n")

        # Obtiene todos los no-terminales y terminales
        non_terminals = sorted(self.grammar.non_terminals)
        terminals = sorted(
            [t for t in self.all_terminals if t not in [self.epsilon]],
            key=lambda x: (x != self.end_marker, x)
        )

        # Imprime encabezado
        print(f"{'':10}", end='')
        for terminal in terminals:
            print(f"{terminal:15}", end='')
        print()
        print("-" * (10 + len(terminals) * 15))

        # Imprime filas de la tabla
        for non_terminal in non_terminals:
            print(f"{non_terminal:10}", end='')
            for terminal in terminals:
                entry = self.table[non_terminal].get(terminal, [])
                if entry:
                    entry_str = f"{non_terminal}->{entry[0]}"
                    if len(entry) > 1:
                        entry_str += " (CONFLICTO)"
                else:
                    entry_str = "error"
                print(f"{entry_str:15}", end='')
            print()

        print("\n" + "="*100)

    def display_ll1_analysis(self):
        """Muestra resultados del analisis LL(1)."""
        print("\n" + "="*80)
        print("ANALISIS LL(1)")
        print("="*80 + "\n")

        if self.is_ll1:
            print("[SI] Esta gramatica ES LL(1)")
            print("      Sin conflictos en la tabla de analisis.")
        else:
            print("[NO] Esta gramatica NO ES LL(1)")
            print(f"\n      Conflictos encontrados en {len(self.conflicts)} ubicacion(es):")
            for non_terminal, terminal in self.conflicts:
                productions = self.table[non_terminal][terminal]
                print(f"        [{non_terminal}, {terminal}]: {productions}")

        print("\n" + "="*80)

    def get_ll1_status(self):
        """Retorna estado LL(1) como una cadena simple."""
        return "LL(1)" if self.is_ll1 else "NO LL(1)"
