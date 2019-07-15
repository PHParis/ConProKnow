from re import compile


def keep_alphanumeric_only(s: str) -> str:
    """Return the same string but with only its alphanumeric caracters."""
    pattern = compile('[\W_]+')
    return pattern.sub('', s)
