import helpers
from helpers import Counter

def preprocess_larrow(line: str, pos: int, counter: Counter):
    """
    Adds spaces around '<' (if required)
    Returns the modified line and the new position of the character 
    """
    

    if helpers.in_string_literal(line, pos): return line, pos

    if pos < len(line) - 1:
        helpers.check_for_operators(line, pos + 1, counter, {"-", "="})
    if pos > 0:
        helpers.check_for_operators(line, pos - 1, counter)
    
    if pos < len(line) - 1:
        if line[pos + 1] not in ("-", " ", "="):
            line = helpers.add_character_at(" ", line, pos + 1)

    if pos > 0:
        if line[pos - 1] != " ":
            line = helpers.add_character_at(" ", line, pos)
            pos += 1

    return line, pos


def preprocess_rarrow(line: str, pos: int, counter: Counter):
    """
    Adds spaces around '>' (if required)
    Returns the modified line and the new position of the character 
    """


    if helpers.in_string_literal(line, pos): return line, pos

    if pos < len(line) - 1:
        helpers.check_for_operators(line, pos + 1, counter, {"="})
    if pos > 0:
        helpers.check_for_operators(line, pos - 1, counter)

    if pos < len(line) - 1:
        if line[pos + 1] not in ("=", " '"):
            line = helpers.add_character_at(" ", line, pos + 1)

    if pos > 0:
        if line[pos - 1] != " ":
            line = helpers.add_character_at(" ", line, pos)
            pos += 1

    return line, pos


def preprocess_minus(line: str, pos: int, counter: Counter):
    """
    Adds spaces around the minus (if required)
    Returns the modified line and the new position of the character 
    """


    if helpers.in_string_literal(line, pos): return line, pos

    if pos < len(line) - 1:
        helpers.check_for_operators(line, pos + 1, counter)
    if pos > 0:
        helpers.check_for_operators(line, pos - 1, counter, {"<"})

    if pos < len(line) - 1:
        if line[pos + 1] != " ":
            line = helpers.add_character_at(" ", line, pos + 1)

    if pos > 0:
        if line[pos - 1] != "<" and line[pos - 1] != " ":
            line = helpers.add_character_at(" ", line, pos)
            pos += 1

    return line, pos


def preprocess_equals(line: str, pos: int, counter: Counter):
    """
    Adds spaces around the '=' (if required)
    Returns the modified line and the new position of the character
    """


    if helpers.in_string_literal(line, pos): return line, pos

    if pos < len(line) - 1:
        helpers.check_for_operators(line, pos + 1, counter)
    if pos > 0:
        helpers.check_for_operators(line, pos - 1, counter, {"!", "<", ">"})

    if pos > 0:
        if line[pos - 1] not in ("!", "<", ">"):
            line = helpers.add_character_at(" ", line, pos)
            pos += 1

    if pos < len(line) - 1:
        if line[pos + 1] != " ":
            line = helpers.add_character_at(" ", line, pos + 1)

    return line, pos


def preprocess_division(line: str, pos: int, counter: Counter):
    """
    Adds "1.0" before the `/` operator to allow for true division
    when the code is transpiled to C++
    """


    if helpers.in_string_literal(line, pos): return line, pos

    if pos < len(line) - 1:
        helpers.check_for_operators(line, pos + 1 , counter)
    if pos > 0:
        helpers.check_for_operators(line, pos - 1 , counter)

    line = helpers.add_character_at("* 1.0 ", line, pos)
    pos += 6

    return line, pos


def preprocess_arithmetic_operator(line: str, pos: int, counter: Counter):
    """
    Adds spaces around arithmetic operators: +*%[]=()
    Returns the modified line and the new position of the character 
    """


    if helpers.in_string_literal(line, pos): return line, pos

    if pos < len(line) - 1:
        helpers.check_for_operators(line, pos + 1, counter)
    if pos > 0:
        helpers.check_for_operators(line, pos - 1, counter)

    if pos < len(line) - 1:
        if line[pos + 1] != " ":
            line = helpers.add_character_at(" ", line, pos + 1)

    if pos > 0:
        if line[pos - 1] != " ":
            line = helpers.add_character_at(" ", line, pos)
            pos += 1

    return line, pos
