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
    return string[:position] + character + string[position:]

def preprocess_larrow(line: str, pos: int):
    if line[pos + 1] != "-" and line[pos + 1] != " ":
        line = add_character_at(" ", line, pos + 1)

    if line[pos - 1] != " ":
        line = add_character_at(" ", line, pos)
        pos += 1

    return line

def preprocess_rarrow(line: str, pos: int):
    if line[pos + 1] != "=" and line[pos + 1] != " ":
        line = add_character_at(" ", line, pos + 1)

    if line[pos - 1] != " ":
        line = add_character_at(" ", line, pos)
        pos += 1

    return line

def preprocess_minus(line: str, pos: int):
    if line[pos - 1] != "<" and line[pos - 1] != " ":
        line = add_character_at(" ", line, pos)
        pos += 1

    if line[pos + 1] != " ":
        line = add_character_at(" ", line, pos + 1)

    return line

# TODO: handle += -= /= etc
def preprocessArithmeticOperator(line: str, pos: int):
    if line[pos - 1] != " ":
        line = add_character_at(" ", line, pos)
        pos += 1
    
    if line[pos + 1] != " ":
        line = add_character_at(" ", line, pos + 1)

    return line


with open("./main.pc") as f:
    output = "#include <iostream>\nusing namespace std;\nint main()\n{\n"

    for line in f: # go line by line
        processed_line = ""
        for pos, char in enumerate(line): # processing the current line (adding spaces where needed)
            match char:
                case "<":
                    processed_line = preprocess_larrow(line, pos)
                    break

                case "-":
                    processed_line = preprocess_minus(line, pos)
                    break

                case ">":
                    processed_line = preprocess_rarrow(line, pos)
                    break

                case "+" | "/" | "*" | "%" | "[" | "]" | "=" | "(" | ")":
                    processed_line = preprocessArithmeticOperator(line, pos)
                    break

        with open("./test.cpp", "a") as g:
            g.write(processed_line)

