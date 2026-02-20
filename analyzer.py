def analyze_code(code):
    issues = []

    if not code.strip():
        issues.append("Code is empty.")

    if "==" in code and "True" in code:
        issues.append("Avoid comparing with True directly.")

    if "print(" in code:
        issues.append("Avoid print statements in production.")

    if len(code) > 300:
        issues.append("Code is too long. Consider modularizing.")

    if not issues:
        issues.append("No major issues found. Good job!")

    return issues

