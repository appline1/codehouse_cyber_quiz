from rapidfuzz import fuzz

def is_fuzzy_match(a: str, b: str, threshold: int = 80) -> bool:
    return fuzz.ratio(a.strip().lower(), b.strip().lower()) >= threshold
