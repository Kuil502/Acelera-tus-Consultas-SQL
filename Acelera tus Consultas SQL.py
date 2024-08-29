import sqlparse
from sqlparse.sql import Where, IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML
import re

def suggest_optimizations(query):
    # Parsear la consulta SQL
    parsed = sqlparse.parse(query)[0]

    optimizations = []

    # Sugerir la creación de índices
    def suggest_index(parsed):
        tables = []
        columns = []
        for token in parsed.tokens:
            if isinstance(token, IdentifierList):
                for identifier in token.get_identifiers():
                    columns.append(str(identifier))
            elif isinstance(token, Identifier):
                tables.append(str(token))
            elif token.ttype is Keyword and token.value.upper() == 'WHERE':
                where_clause = str(token.parent).split('WHERE')[-1].strip()
                columns_in_where = re.findall(r'(\w+)\s*=', where_clause)
                if columns_in_where:
                    for column in columns_in_where:
                        optimizations.append(f"Sugerencia: Considera crear un índice en la columna '{column}'.")

    # Sugerir el uso de JOIN en lugar de subconsultas
    def suggest_join_over_subquery(parsed):
        for token in parsed.tokens:
            if token.ttype is Keyword and token.value.upper() == 'SELECT':
                subqueries = re.findall(r'SELECT\s+\*\s+FROM\s+\((SELECT.+FROM.+)\)', str(parsed))
                if subqueries:
                    optimizations.append("Sugerencia: Considera usar JOIN en lugar de subconsultas para mejorar el rendimiento.")

    # Sugerir reorganización de operaciones
    def suggest_operation_reorganization(parsed):
        for token in parsed.tokens:
            if isinstance(token, Where):
                conditions = str(token).split('AND')
                if len(conditions) > 1:
                    optimizations.append("Sugerencia: Reorganiza las condiciones WHERE, colocando las más selectivas primero.")

    suggest_index(parsed)
    suggest_join_over_subquery(parsed)
    suggest_operation_reorganization(parsed)

    if optimizations:
        print("Optimizations Sugeridas:")
        for suggestion in optimizations:
            print(f"- {suggestion}")
    else:
        print("No se encontraron optimizaciones sugeridas.")

# Ejemplo de uso
query = """
SELECT *
FROM empleados
WHERE salario > 50000
AND departamento_id IN (SELECT id FROM departamentos WHERE nombre = 'Ventas');
"""

suggest_optimizations(query)
