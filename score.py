# score.py

def calculate_score(actual_issues):
    """
    Calculate code score.
    - actual_issues: list of real problems (PEP8 violations, syntax errors)
    Returns: score (0-100)
    """
    # If no real issues → perfect score
    if not actual_issues or any("No major issues found" in issue for issue in actual_issues):
        return 100

    # Deduct 10 points per real issue, minimum 50
    return max(100 - len(actual_issues) * 10, 50)

def check_modularity(code):
    """
    Check for long functions (>50 lines) and return warnings.
    Warnings do NOT affect score.
    """
    warnings = []
    functions = code.split("def ")
    for f in functions[1:]:
        lines = f.splitlines()
        if len(lines) > 50:  # threshold increased to ignore normal scripts
            fname = lines[0].split("(")[0].strip()
            warnings.append(f"Function '{fname}' is very long. Consider modularizing.")
    return warnings
