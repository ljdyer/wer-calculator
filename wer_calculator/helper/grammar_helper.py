# ====================
def sing_or_plural(word: str, number: int) -> str:
    """Add a plural s to the word if the number is not 1"""

    if number == 1:
        return word
    else:
        return word + 's'


# ====================
def is_or_are(number: int) -> str:
    """Return 'is' if the number is 1 or 'are' otherwise"""

    if number == 1:
        return 'is'
    else:
        return 'are'
