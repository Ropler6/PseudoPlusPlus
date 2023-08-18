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


def process_user_input(line: str):
    pass


def process_user_output(line: str):
    pass

required_stops = 0 # the amount of stops required to close all loops/if statements
required_loop_enders = 0 # the amount of "cat timp" required to close all repeta-loops
def process_line(line: str):
    segments = line.split(";")
    if len(segments) > 1: #if there are more instructions, process them separately
        result = ""
        for segment in segments:
            result += process_line(segment)

        return result

    tokens = segments[0].strip("\n").split()
    result = ""
    global required_stops, required_loop_enders
    requires_semicolon = True

    if len(tokens) == 0:
        return ""

    if tokens[0] == "citeste":
        # return process_user_input(segments[0])
        pass
    elif tokens[0] == "scrie":
        # return process_user_output(segments[0])
        pass
    elif tokens[0] in ["daca", "cat", ]:
        required_stops += 1
        requires_semicolon = False
    elif tokens[0] == "repeta":
        required_loop_enders += 1
    elif tokens[0] == "stop":
        required_stops -= 1
        requires_semicolon = False

    for token in tokens: #TODO: error-handling
        if keywords.get(token) is not None:
            result += keywords[token]
        else:
            result += token

    if requires_semicolon:
        result += ";"

    return result + "\n"

# Reset the rest file
with open("./temp.txt", "w+") as g:
    g.write("")

# Add spaces to the file and put the results in a temp file
with open("./main.pc") as f:
    for line in f: # go line by line
        i = 0
        while i < len(line): # processing the current line
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
        with open("./temp.txt", "a") as g:
            g.write(line)

with open("./test.cpp", "w") as g:
    g.write("")

# TODO: move this in the for-loop above
with open("./temp.txt") as f:
    with open("./test.cpp", "a") as g:
        for line in f:
            processed_line = process_line(line)
            g.write(processed_line)
