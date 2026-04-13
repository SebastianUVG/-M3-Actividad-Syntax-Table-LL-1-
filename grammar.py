"""
Representacion de gramaticas libres de contexto.
Maneja el analisis y almacenamiento de producciones de la gramatica.
"""

class Grammar:
    """
    Representa una gramatica libre de contexto (CFG).

    Una gramatica se define como:
    - No-terminales: simbolos que tienen producciones
    - Terminales: simbolos que no tienen producciones
    - Producciones: reglas como A -> α | β | ...
    - Simbolo inicial: el no-terminal inicial
    """

    def __init__(self, start_symbol=None):
        """
        Inicializa una nueva gramatica.

        Args:
            start_symbol: El simbolo inicial de la gramatica
        """
        self.productions = {}  # {no_terminal: [produccion1, produccion2, ...]}
        self.non_terminals = set()
        self.terminals = set()
        self.start_symbol = start_symbol
        self.epsilon = 'eps'

    

    def add_production_explicit(self, non_terminal, production_list):
        """
        Anade produccion con lista explicita de alternativas.

        Args:
            non_terminal: El no-terminal del lado izquierdo
            production_list: Lista de producciones (cada produccion como una cadena)
        """
        if non_terminal not in self.productions:
            self.productions[non_terminal] = []

        for prod in production_list:
            self.productions[non_terminal].append(prod.strip())

        self.non_terminals.add(non_terminal)

        if self.start_symbol is None:
            self.start_symbol = non_terminal

    def extract_terminals(self):
        """Extrae todos los terminales de la gramatica."""
        self.terminals.clear()

        for non_terminal, productions in self.productions.items():
            for production in productions:
                if production != self.epsilon:  # epsilon no es un terminal
                    # Divide la produccion en simbolos
                    for i, char in enumerate(production):
                        symbol = self._extract_symbol_at(production, i)
                        if symbol and symbol != self.epsilon:
                            # Si no es un no-terminal conocido, es un terminal
                            if symbol not in self.non_terminals:
                                self.terminals.add(symbol)

    def _extract_symbol_at(self, production, index):
        """Extrae un simbolo de una produccion en un indice dado."""
        if index >= len(production):
            return None

        # Simbolos de multiples caracteres
        if production[index:index+3] == 'eps':
            return 'eps'

        # Verifica no-terminales de multiples caracteres terminados con '
        if index < len(production) - 1 and production[index + 1] == "'":
            return production[index:index + 2]

        return production[index]

    def get_all_symbols(self, production):
        """
        Divide una produccion en simbolos individuales.

        Maneja simbolos de multiples caracteres separados por espacios.

        Args:
            production: Una cadena de produccion como "T E'" o "id"

        Returns:
            Lista de simbolos
        """
        if production == self.epsilon:
            return [self.epsilon]

        # Divide por espacios - los simbolos deben estar separados por espacios
        symbols = production.split()

        # Maneja caso donde simbolos no estan separados por espacios (compatibilidad hacia atras)
        if len(symbols) == 1 and len(production) > 1:
            # Formato antiguo: "T E'" - intenta dividirlo
            result = []
            i = 0
            while i < len(production):
                if production[i:i+3] == 'eps':
                    result.append('eps')
                    i += 3
                elif i < len(production) - 1 and production[i + 1] == "'":
                    result.append(production[i:i + 2])
                    i += 2
                else:
                    result.append(production[i])
                    i += 1
            return result

        return symbols

    def display(self):
        """Muestra la gramatica en un formato legible."""
        print("\n" + "="*60)
        print("DEFINICION DE GRAMATICA")
        print("="*60)
        print(f"Simbolo inicial: {self.start_symbol}\n")

        for non_terminal in sorted(self.productions.keys()):
            productions = self.productions[non_terminal]
            print(f"{non_terminal} -> {' | '.join(productions)}")

        print("\n" + "="*60)


def create_arithmetic_grammar():
    """Crea la gramatica de expresiones aritmeticas de la actividad."""
    grammar = Grammar()
    grammar.add_production_explicit('E', ["T E'"])
    grammar.add_production_explicit("E'", ["+ T E'", "eps"])
    grammar.add_production_explicit('T', ["F T'"])
    grammar.add_production_explicit("T'", ["* F T'", "eps"])
    grammar.add_production_explicit('F', ["( E )", "id"])
    return grammar


def create_statements_grammar():
    """Crea una gramatica para expresiones booleanas con AND y OR."""
    grammar = Grammar()
    grammar.add_production_explicit('E', ["T E'"])
    grammar.add_production_explicit("E'", ["or T E'", "eps"])
    grammar.add_production_explicit('T', ["F T'"])
    grammar.add_production_explicit("T'", ["and F T'", "eps"])
    grammar.add_production_explicit('F', ["true", "false", "( E )"])
    return grammar


def create_functions_grammar():
    """Crea una gramatica para listas de numeros."""
    grammar = Grammar()
    grammar.add_production_explicit('L', ["num L'"])
    grammar.add_production_explicit("L'", [", num L'", "eps"])
    return grammar
