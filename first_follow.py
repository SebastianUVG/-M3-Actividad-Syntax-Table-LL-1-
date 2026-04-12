"""
Calculo de conjuntos FIRST y FOLLOW para gramaticas libres de contexto.

FIRST(X):
- Conjunto de terminales que pueden aparecer al inicio de cadenas derivadas de X
- Para un no-terminal, incluye todos los terminales de los primeros simbolos de sus producciones
- Incluye epsilon si la produccion puede derivar epsilon

FOLLOW(A):
- Conjunto de terminales que pueden aparecer inmediatamente despues del no-terminal A en alguna forma sentencial
- Utiliza conjuntos FIRST para el calculo
- Incluye $ (fin de entrada) para el simbolo inicial
"""


class FirstFollowAnalyzer:
    """Calcula conjuntos FIRST y FOLLOW para gramaticas libres de contexto."""

    def __init__(self, grammar):
        """
        Inicializa el analizador.

        Args:
            grammar: Objeto Grammar
        """
        self.grammar = grammar
        self.first_sets = {}
        self.follow_sets = {}
        self.epsilon = 'eps'
        self.end_marker = '$'

    def calculate_first(self):
        """
        Calcula conjuntos FIRST para todos los no-terminales en la gramatica.

        Algoritmo:
        1. Inicializa todos los conjuntos FIRST como vacios
        2. Para cada no-terminal, encuentra los primeros simbolos de sus producciones
        3. Itera hasta que no haya cambios (punto fijo)
        """
        # Inicializa conjuntos FIRST
        for non_terminal in self.grammar.non_terminals:
            self.first_sets[non_terminal] = set()

        # Itera hasta convergencia
        changed = True
        while changed:
            changed = False

            for non_terminal, productions in self.grammar.productions.items():
                for production in productions:
                    # Obtiene simbolos en esta produccion
                    symbols = self.grammar.get_all_symbols(production)

                    # Calcula FIRST de esta produccion
                    first_of_production = self._first_of_sequence(symbols)

                    # Anade a FIRST(no_terminal)
                    old_size = len(self.first_sets[non_terminal])
                    self.first_sets[non_terminal].update(first_of_production)

                    if len(self.first_sets[non_terminal]) > old_size:
                        changed = True

        return self.first_sets

    def _first_of_sequence(self, symbols):
        """
        Calcula FIRST de una secuencia de simbolos.

        Args:
            symbols: Lista de simbolos

        Returns:
            Conjunto de terminales que pueden aparecer al inicio
        """
        first_set = set()
        all_can_be_epsilon = True

        for symbol in symbols:
            if symbol == self.epsilon:
                first_set.add(self.epsilon)
            elif symbol in self.grammar.non_terminals:
                # Anade FIRST(simbolo) - epsilon
                first_of_symbol = self.first_sets.get(symbol, set()).copy()
                first_set.update(first_of_symbol - {self.epsilon})

                # Si el simbolo no puede derivar epsilon, detente
                if self.epsilon not in self.first_sets.get(symbol, set()):
                    all_can_be_epsilon = False
                    break
            else:
                # Es un terminal
                first_set.add(symbol)
                all_can_be_epsilon = False
                break

        # Si todos los simbolos pueden derivar epsilon, añade epsilon
        if all_can_be_epsilon:
            first_set.add(self.epsilon)

        return first_set

    def calculate_follow(self):
        """
        Calcula conjuntos FOLLOW para todos los no-terminales en la gramatica.

        Algoritmo:
        1. Inicializa conjuntos FOLLOW como vacios, excepto simbolo inicial obtiene {$}
        2. Para cada produccion A -> α, calcula FOLLOW de cada simbolo
        3. Itera hasta que no haya cambios (punto fijo)
        """
        # Inicializa conjuntos FOLLOW
        for non_terminal in self.grammar.non_terminals:
            self.follow_sets[non_terminal] = set()

        # Simbolo inicial siempre tiene $ en su conjunto follow
        if self.grammar.start_symbol:
            self.follow_sets[self.grammar.start_symbol].add(self.end_marker)

        # Itera hasta convergencia
        changed = True
        while changed:
            changed = False

            for non_terminal, productions in self.grammar.productions.items():
                for production in productions:
                    symbols = self.grammar.get_all_symbols(production)

                    # Procesa cada simbolo en la produccion
                    for i, symbol in enumerate(symbols):
                        if symbol == self.epsilon:
                            continue

                        if symbol in self.grammar.non_terminals:
                            # Obtiene simbolos que siguen a este
                            following_symbols = symbols[i + 1:]

                            # Calcula FIRST de simbolos que siguen
                            if following_symbols:
                                first_of_following = self._first_of_sequence(following_symbols)
                                first_of_following_no_eps = first_of_following - {self.epsilon}

                                old_size = len(self.follow_sets[symbol])
                                self.follow_sets[symbol].update(first_of_following_no_eps)

                                # Si simbolos que siguen pueden derivar epsilon, anade FOLLOW(A)
                                if self.epsilon in first_of_following:
                                    self.follow_sets[symbol].update(self.follow_sets[non_terminal])

                                if len(self.follow_sets[symbol]) > old_size:
                                    changed = True
                            else:
                                # No hay simbolos despues de este, anade FOLLOW(A)
                                old_size = len(self.follow_sets[symbol])
                                self.follow_sets[symbol].update(self.follow_sets[non_terminal])

                                if len(self.follow_sets[symbol]) > old_size:
                                    changed = True

        return self.follow_sets

    def display_first_follow(self):
        """Muestra conjuntos FIRST y FOLLOW en un formato legible."""
        print("\n" + "="*80)
        print("CONJUNTOS FIRST Y FOLLOW")
        print("="*80 + "\n")

        print("CONJUNTOS FIRST:")
        print("-" * 40)
        for non_terminal in sorted(self.first_sets.keys()):
            first_set = self.first_sets[non_terminal]
            formatted_set = sorted([s for s in first_set if s != self.epsilon])
            if self.epsilon in first_set:
                formatted_set.append(self.epsilon)
            print(f"  FIRST({non_terminal:3}) = {set(formatted_set)}")

        print("\nCONJUNTOS FOLLOW:")
        print("-" * 40)
        for non_terminal in sorted(self.follow_sets.keys()):
            follow_set = self.follow_sets[non_terminal]
            formatted_set = sorted([s for s in follow_set if s != self.end_marker])
            if self.end_marker in follow_set:
                formatted_set.append(self.end_marker)
            print(f"  FOLLOW({non_terminal:3}) = {set(formatted_set)}")

        print("\n" + "="*80)
