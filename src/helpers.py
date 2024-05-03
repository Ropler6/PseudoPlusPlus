

class Identifier:
    def __init__(self, name: str, type: str) -> None:
        self.name = name
        self.type = type

class Counter:
    def __init__(self) -> None:
        self.required_stops = 0
        self.required_loop_enders = 0
        self.stops = 0
        self.loop_enders = 0
        self.current_line = 0
        self.identifiers: list[Identifier] = []


KEYWORDS = {
    # I/O
    "citeste": "cin>>",
    "<-": "=",
    "scrie": "cout<<",

    # loops
    "cat": "",
    "timp": "while (",
    "executa": "){\n",
    "repeta": "do {\n",
    "pana": "",
    "cand": "while (",
    "pentru": "for (",
    "iesi": "break",

    # conditional
    "daca": "if (",
    "atunci": "){\n",
    "altfel": "}else{\n",

    # operator
    "[": "(int)(",
    "]": ")",
    "=": "==",
    "!=": "!=",
    "si": "&&",
    "sau": "||",

    # data type
    "natural": "unsigned int",
    "real": "float",
    "intreg": "int",
    "sir": "string",
    "caracter": "char",

    # other
    "(": "(",
    ")": ")",

    # stop
    "stop": "}\n",
}

OPERATORS = {"[", "]", "(", ")", "+", "-", "/", "*", "%", "si", "sau", "=", "<-", ">", "<", ">=", "<=", "!=", "!"}
STRUCTURE_KEYWORDS = {"cat", "timp", "executa", "repeta", "pana", "cand", "daca", "atunci", "altfel",
                      "citeste", "scrie", "pentru", "iesi", "stop"}
DATA_TYPES = {"natural", "intreg", "real", "sir", "caracter"}
RESERVED_KEYWORDS = set.union(STRUCTURE_KEYWORDS, DATA_TYPES)

class UnknownTokenError(Exception):
    """Raise when the processer encounters an unknown token"""

class UnexpectedKeywordError(Exception):
    """Raise when a keyword is used improperly"""

class MissingKeywordError(Exception):
    """Raise when a keyword is missing in a structure"""

class UnexpectedOperatorError(Exception):
    """Raise when an operator is used in a wrong context"""

class MissingIdentifierError(Exception):
    """Raise when an identifier is expected but is missing in code"""

class MissingLiteralError(Exception):
    """Raise when a literal is expected but is missing in code"""

class MissingParenthesisError(Exception):
    """Raise when a parenthesis or a bracket is missing"""


def add_character_at(character: str, string: str, position: int) -> str:
    """
    Adds the given `character` at the given `position` and returns the new string
    """


    return string[:position] + character + string[position:]


def type_of(value: str, counter: Counter):
    """
    Determines the type of `value` and returns it as a string
    """

    if len(value) == 0:
        return "necunoscut"

    if value[0] == "\"" and value[-1] == "\"":
        return "sir"

    for x in counter.identifiers:
        if x.name == value:
            return "identificator"

    if value in OPERATORS:
        return "operator"
    
    if value in RESERVED_KEYWORDS:
        return "keyword"

    value = value.replace(" ", "")

    try:
        value = int(value)
        return "intreg"
    except ValueError:
        try:
            value = float(value)
            return "real"
        except ValueError:
            return "necunoscut"


def check_for_errors(tokens: list[str], result: str, counter: Counter, sep: str = " ", *, operators_allowed: bool = False, reserved_allowed: bool = False,
                      identifiers_allowed: bool = False, literals_allowed: bool = False) -> str:
    """Checks `tokens` for illegal tokens (specified in the params) and throws errors accordingly
    
    Returns the processed tokens added to `result`"""

    parentheses = 0 # ()
    brackets = 0 # []

    for token in tokens:
        if type_of(token, counter) == "necunoscut":
            raise UnknownTokenError(f"{token} on line {counter.current_line} (2101)")

        if not reserved_allowed:
            if token in RESERVED_KEYWORDS:
                raise UnexpectedKeywordError(f"{token} on line {counter.current_line} (2102)")
        else:
            result += KEYWORDS[token] + sep
            continue

        if not operators_allowed:
            if token in OPERATORS:
                raise UnexpectedOperatorError(f"{token} on line {counter.current_line} (2103)")
        else:
            if token in OPERATORS:
                if token in ("(", ")"):
                    parentheses += 1
                if token in ("[", "]"):
                    brackets += 1
                result += f"{KEYWORDS[token] if KEYWORDS.get(token) is not None else token}" + sep
                continue
        
        if not literals_allowed:
            if type_of(token, counter) not in ("real", "intreg"):
                raise UnknownTokenError(f"{token} on line {counter.current_line} (2104)")
        else:
            if type_of(token, counter) != "identificator":
                result += token + sep
                continue
        
        if not identifiers_allowed:
            if is_identifier(token, counter):
                raise UnknownTokenError(f"{token} on line {counter.current_line} (2105)")
        else:
            if not is_identifier(token, counter):
                raise UnknownTokenError(f"{token} on line {counter.current_line} (2106)")
            
            result += token + sep
            continue

    if brackets % 2 != 0:
        raise MissingParenthesisError(f"on line {counter.current_line} (2107)")

    if parentheses % 2 != 0:
        raise MissingParenthesisError(f"on line {counter.current_line} (2108)")

    return result


def check_for_operators(line: str, pos: int, counter: Counter, omit: set[str] = set()):
    if line[pos] in OPERATORS - omit:
        raise UnexpectedOperatorError(f"{line[pos]} on line {counter.current_line} (2201)")


def is_identifier(name: str, counter: Counter):
    for x in counter.identifiers:
        if x.name == name:
            return True

    return False


def get_identifier_type(name: str, counter: Counter):
    for x in counter.identifiers:
        if x.name == name:
            return x.type

    raise MissingIdentifierError(f"Line {counter.current_line} (2301)")
