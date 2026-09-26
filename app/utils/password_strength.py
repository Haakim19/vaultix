import re


def check_password_strength(password: str) -> tuple[str, int]:
    """
    Returns (label, score). Label is one of "Weak", "Medium", "Strong".
    Score ranges from 0 (empty) to 6 (very strong).
    """
    if not password:
        return "Weak", 0

    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(not c.isalnum() for c in password):
        score += 1

    # Penalties
    lower = password.lower()
    if any(p in lower for p in ("password", "123456", "qwerty", "admin", "letmein")):
        score -= 2
    if len(set(password)) < 3:
        score -= 2

    score = max(0, score)

    if score <= 2:
        return "Weak", score
    elif score <= 4:
        return "Medium", score
    else:
        return "Strong", score