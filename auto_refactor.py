# auto_refactor.py
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def auto_refactor_code(code):
    """
    Refactor Python code:
    - Remove trailing spaces
    - Standardize indentation to 4 spaces
    - Replace print() with logging.info()
    """
    # Remove trailing whitespaces
    code = re.sub(r'[ \t]+$', '', code, flags=re.MULTILINE)

    # Standardize indentation (naive 4 spaces)
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
    new_lines = [re.sub(r'print\((.*)\)', r'logging.info(\1)', l) for l in new_lines]

    return "\n".join(new_lines)