"""Safe arithmetic calculator tool."""

import ast
import operator


TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Evaluate a simple arithmetic expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": (
                        "Arithmetic expression, for example '2 + 3 * 4'."
                    ),
                },
            },
            "required": ["expression"],
        },
    },
}

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression):
    """Evaluate a simple arithmetic expression and return the result.

    >>> calculate('2 + 3 * 4')
    '14'
    >>> calculate('(10 - 4) / 2')
    '3.0'
    >>> calculate('__import__("os").system("pwd")')
    'error: unsupported expression'
    >>> calculate('2 +')
    'error: invalid expression'
    """
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        return "error: invalid expression"

    try:
        return str(_eval_node(tree.body))
    except (TypeError, ValueError, ZeroDivisionError) as error:
        return f"error: {error}"


def _eval_node(node):
    """Evaluate one AST node from a safe arithmetic expression.

    >>> _eval_node(ast.parse('2 ** 3', mode='eval').body)
    8
    >>> _eval_node(ast.parse('-5', mode='eval').body)
    -5
    """
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](
            _eval_node(node.left),
            _eval_node(node.right),
        )
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](_eval_node(node.operand))
    raise ValueError("unsupported expression")
