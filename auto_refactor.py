# auto_refactor.py
import re
import ast
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def split_long_function(func_node: ast.FunctionDef, max_lines=10):
    """Split a long function into smaller functions if longer than max_lines"""
    if len(func_node.body) <= max_lines:
        return [ast.unparse(func_node)]

    chunks = [func_node.body[i:i+max_lines] for i in range(0, len(func_node.body), max_lines)]
    new_functions = []

    for idx, chunk in enumerate(chunks):
        name = f"{func_node.name}_part{idx+1}"
        new_func = ast.FunctionDef(
            name=name,
            args=func_node.args,
            body=chunk,
            decorator_list=[]
        )
        new_functions.append(ast.unparse(new_func))

    return new_functions

def modularize_code(code: str) -> str:
    """Parse Python code and split long functions safely"""
    try:
        tree = ast.parse(code)
    except Exception as e:
        logging.error(f"AST parse failed: {e}")
        return code  # Return original if invalid Python

    refactored_parts = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            refactored_parts.extend(split_long_function(node))
        else:
            # Keep classes or other statements
            try:
                refactored_parts.append(ast.unparse(node))
            except Exception:
                refactored_parts.append(code)  # fallback
    return "\n\n".join(refactored_parts)

def auto_refactor_code(code):
    """Full refactor: modularize, fix indentation, replace print with logging"""
    # Remove trailing spaces
    code = re.sub(r'[ \t]+$', '', code, flags=re.MULTILINE)

    # Modularize
    code = modularize_code(code)

    # Fix indentation (naive 4 spaces)
    lines = code.splitlines()
    new_lines = []
    indent_level = 0
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("def ") or stripped.startswith("class "):
            indent_level = 0
        new_lines.append(" " * (indent_level * 4) + stripped)
        if stripped.endswith(":"):
            indent_level += 1

    # Replace print() with logging.info()
    def replace_print(match):
        return f'logging.info({match.group(1)})'

    new_lines = [re.sub(r'^\s*print\((.*)\)', replace_print, l) for l in new_lines]

    # Ensure logging import exists
    if 'import logging' not in "\n".join(new_lines):
        new_lines.insert(0, 'import logging')

    return "\n".join(new_lines)