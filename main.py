"""
Script principal de demostracion para analisis FIRST, FOLLOW y Tabla de Analisis Sintactico.

Este script demuestra la implementacion de:
1. Calculo de conjuntos FIRST
2. Calculo de conjuntos FOLLOW
3. Construccion de tabla de analisis predictivo
4. Analisis de gramatica LL(1)

Probado con tres gramaticas diferentes.
"""

from grammar import (Grammar, create_arithmetic_grammar,
                     create_statements_grammar, create_functions_grammar)
from first_follow import FirstFollowAnalyzer
from parsing_table import ParsingTable


def process_grammar(grammar, grammar_name):
    """
    Procesa una gramatica: calcula FIRST, FOLLOW, y construye tabla de analisis.

    Args:
        grammar: Objeto Grammar
        grammar_name: Nombre de la gramatica (para visualizacion)
    """
    print("\n\n")
    print("=" * 100)
    print(f" {grammar_name:^98} ")
    print("=" * 100)

    # Muestra gramatica
    grammar.extract_terminals()
    grammar.display()

    # Calcula FIRST y FOLLOW
    analyzer = FirstFollowAnalyzer(grammar)
    analyzer.calculate_first()
    analyzer.calculate_follow()
    analyzer.display_first_follow()

    # Construye y muestra tabla de analisis
    table = ParsingTable(grammar, analyzer)
    table.build_table()
    table.display_table()
    table.display_ll1_analysis()

    return analyzer, table


def main():
    """Ejecuta la demostracion principal."""
    print("\n")
    print("=" * 100)
    print("ANALISIS DE TABLA DE ANALISIS PREDICTIVO Y CONJUNTOS FIRST/FOLLOW".center(100))
    print("para Gramaticas Libres de Contexto".center(100))
    print("=" * 100)

    results = []

    # Gramatica 1: Expresiones Aritmeticas
    grammar1 = create_arithmetic_grammar()
    analyzer1, table1 = process_grammar(
        grammar1,
        "GRAMATICA 1: EXPRESIONES ARITMETICAS"
    )
    results.append(("Expresiones Aritmeticas", table1.get_ll1_status()))

    # Gramatica 2: Expresiones Booleanas
    grammar2 = create_statements_grammar()
    analyzer2, table2 = process_grammar(
        grammar2,
        "GRAMATICA 2: EXPRESIONES BOOLEANAS"
    )
    results.append(("Expresiones Booleanas", table2.get_ll1_status()))

    # Gramatica 3: Listas de Numeros
    grammar3 = create_functions_grammar()
    analyzer3, table3 = process_grammar(
        grammar3,
        "GRAMATICA 3: LISTAS DE NUMEROS"
    )
    results.append(("Listas de Numeros", table3.get_ll1_status()))

    # Resumen
    print("\n\n")
    print("=" * 100)
    print("RESUMEN DE RESULTADOS".center(100))
    print("=" * 100 + "\n")

    for grammar_name, ll1_status in results:
        status_symbol = "[SI]" if ll1_status == "LL(1)" else "[NO]"
        print(f"  {status_symbol} {grammar_name:40} -> {ll1_status}")

    print("\n" + "=" * 100 + "\n")


if __name__ != "__main__":
    # Esta linea asegura que el script se ejecute cuando se importa como modulo
    main()

# Llama main directamente para ejecucion
main()
