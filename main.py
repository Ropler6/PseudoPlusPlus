class Identifier:
    def __init__(self, name: str, type: str) -> None:
        self.name = name
        self.type = type


keywords = {
    # I/O
    "citeste": "cin>>",
    "<-": "=",
    "scrie": "cout<<",

    # loops
    "cat": "",
    "timp": "while (",
    "executa": "){",
    "repeta": "do {",
    "pana": "",
    "cand": "while (",
    "pentru": "for (",
    "iesi": "break",

    # conditional
    "daca": "if (",
    "atunci": "){",
    "altfel": "else{",

    # operator
    "[": "(int)(",
    "]": ")",
    "=": "==",
    "si": "&&",
    "sau": "||",

    # other
    "(": "(",
    ")": ")",

    # stop
    "stop": "}",
}

identifiers: list[Identifier] = []

def add_character_at(character: str, string: str, position: int) -> str:
    """
    Adds the given `character` at the given `position` and returns the new string
    """


    return string[:position] + character + string[position:]

def preprocess_larrow(line: str, pos: int):
    """
    Adds spaces around '<' (if required)
    Returns the modified line and the new position of the character 
    """
    if line[pos + 1] != "-" and line[pos + 1] != " ":
        line = add_character_at(" ", line, pos + 1)

    if line[pos - 1] != " ":
        line = add_character_at(" ", line, pos)
        pos += 1

    return line, pos

def preprocess_rarrow(line: str, pos: int):
    """
    Adds spaces around '>' (if required)
    Returns the modified line and the new position of the character 
    """


    if line[pos + 1] != "=" and line[pos + 1] != " ":
        line = add_character_at(" ", line, pos + 1)

    if line[pos - 1] != " ":
        line = add_character_at(" ", line, pos)
        pos += 1

    return line, pos


def preprocess_minus(line: str, pos: int):
    """
    Adds spaces around the minus (if required)
    Returns the modified line and the new position of the character 
    """


    if line[pos + 1] != " ":
        line = add_character_at(" ", line, pos + 1)

    if line[pos - 1] != "<" and line[pos - 1] != " ":
        line = add_character_at(" ", line, pos)
        pos += 1

    return line, pos

# TODO: handle += -= /= etc

def preprocess_arithmetic_operator(line: str, pos: int):
    """
    Adds spaces around arithmetic operators: +/*%[]=()
    Returns the modified line and the new position of the character 
    """


    if line[pos + 1] != " ":
        line = add_character_at(" ", line, pos + 1)

    if line[pos - 1] != " ":
        line = add_character_at(" ", line, pos)
        pos += 1    

    return line, pos


# Reset the rest file
with open("./test.cpp", "w") as g:
    g.write("")

with open("./main.pc") as f:
    for line in f: # go line by line
        i = 0
        while i < len(line): # processing the current line (adding spaces where needed)
                             # using a while-loop to properly have len(line) updated
            match line[i]:
                case "<":
                    line, i = preprocess_larrow(line, i)

                case "-":
                    line, i = preprocess_minus(line, i)

                case ">":
                    line, i = preprocess_rarrow(line, i)

                case "+" | "/" | "*" | "%" | "[" | "]" | "=" | "(" | ")":
                    line, i = preprocess_arithmetic_operator(line, i)
            i += 1

        # Write the processed line to the file
        with open("./test.cpp", "a") as g:
            g.write(line)

