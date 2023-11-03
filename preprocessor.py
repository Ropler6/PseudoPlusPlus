import helpers
from helpers import Counter

def preprocess_larrow(line: str, pos: int, counter: Counter):
    """
    Adds spaces around '<' (if required)
    Returns the modified line and the new position of the character 
    """
    
    helpers.check_for_operators(line, pos + 1, counter, {"-", "="})
    helpers.check_for_operators(line, pos - 1, counter)
    
    if line[pos + 1] not in ("-", " ", "="):
        line = helpers.add_character_at(" ", line, pos + 1)

    if line[pos - 1] != " ":
        line = helpers.add_character_at(" ", line, pos)
        pos += 1

    return line, pos


def preprocess_rarrow(line: str, pos: int, counter: Counter):
    """
    Adds spaces around '>' (if required)
    Returns the modified line and the new position of the character 
    """

    helpers.check_for_operators(line, pos + 1, counter, {"="})
    helpers.check_for_operators(line, pos - 1, counter)

    if line[pos + 1] not in ("=", " '"):
        line = helpers.add_character_at(" ", line, pos + 1)

    if line[pos - 1] != " ":
        line = helpers.add_character_at(" ", line, pos)
        pos += 1

    return line, pos


def preprocess_minus(line: str, pos: int, counter: Counter):
    """
    Adds spaces around the minus (if required)
    Returns the modified line and the new position of the character 
    """


    helpers.check_for_operators(line, pos + 1, counter)
    helpers.check_for_operators(line, pos - 1, counter, {"<"})

    if line[pos + 1] != " ":
        line = helpers.add_character_at(" ", line, pos + 1)

    if line[pos - 1] != "<" and line[pos - 1] != " ":
        line = helpers.add_character_at(" ", line, pos)
        pos += 1

    return line, pos


def preprocess_equals(line: str, pos: int, counter: Counter):
    """
    Adds spaces around the '=' (if required)
    Returns the modified line and the new position of the character
    """


    helpers.check_for_operators(line, pos + 1, counter)
    helpers.check_for_operators(line, pos - 1, counter, {"!", "<", ">"})

    if line[pos - 1] not in ("!", "<", ">"):
        line = helpers.add_character_at(" ", line, pos)
        pos += 1

    try:
        if line[pos + 1] != " ":
            line = helpers.add_character_at(" ", line, pos + 1)
    except IndexError:
        pass

    return line, pos


# TODO: handle += -= /= etc
# TODO: split ()[] from +*/%=
def preprocess_arithmetic_operator(line: str, pos: int, counter: Counter):
    """
    Adds spaces around arithmetic operators: +/*%[]=()
    Returns the modified line and the new position of the character 
    """


    helpers.check_for_operators(line, pos + 1, counter)
    helpers.check_for_operators(line, pos - 1, counter)

    try:
        if line[pos + 1] != " ":
            line = helpers.add_character_at(" ", line, pos + 1)
    except IndexError:
        pass

    try:
        if line[pos - 1] != " ":
            line = helpers.add_character_at(" ", line, pos)
            pos += 1
    except IndexError:
        pass

    return line, pos