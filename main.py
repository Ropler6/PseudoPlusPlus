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
    "altfel": "}else ",

    # operator
    "[": "(int)(",
    "]": ")",
    "=": "==",
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

# TODO: add error-handling
def process_user_output(line: str):
    line = line.strip()
    line = line[6:] # remove "scrie" from the line
    tokens = line.split(",")
    tokens[-1] = tokens[-1].strip("\n")
    tokens = [x.strip(" ") for x in tokens] # removing unnecesary spaces

    result = "cout<<"

    for token in tokens: # adding reading syntax for each token
        result += f"{token}<<"

    result = result[:-2] # removing extra "<<" from the end
    result += ";\n" # finishing the line

    return result

# TODO: add error-handling
def process_user_input(line: str):
    line = line.strip()
    line = line[8:] # remove "citeste" from the line
    tokens = line.split(",")
    tokens = [x.strip(" ") for x in tokens] # removing unnecesary spaces

    # the last token and the data type
    temp = tokens[-1].strip().split(" ") # [variable, '(', type, ')']
    tokens[-1] = temp[0] # the last token
    data_type = temp[2] # the data type

    result = ""
    result += keywords[data_type] + " " # the data type of the variables

    for token in tokens: #declaring the variables and saving them for later usage
        result += f"{token},"
        identifiers.append(Identifier(token, data_type))

    result = result[:-1] + ";\n" # finishing the line
    result += "cin>>"

    for token in tokens: # adding reading syntax for each token
        result += f"{token}>>"

    result = result[:-2] # removing extra ">>" from the end
    result += ";\n" # finishing the line

    return result


def process_while_structure(line: str):
    """
    Determines whether the "cat timp" is the start of a while-loop
    or the end of a repeat-while loop and processes the code accordingly
    """

    line = line.strip()
    tokens = line.split()
    result = ""
    if tokens[-1] == "executa": # while-loop
        for token in tokens:
            if keywords.get(token) is not None:
                result += keywords[token]
            else:
                result += token

        return result
    else: # end of repeat-while loop
        result = "} while("
        tokens = tokens[2:] # remove "cat" & "timp"
        for token in tokens:
            if keywords.get(token) is not None:
                result += keywords[token]
            else:
                result += token

        result += ");"        
        return result


def process_repeat_until(line: str):
    line = line.strip()
    result = "} while (!(" # negate the condition(s)
    line = line[10:] # remove "pana cand "
    tokens = line.split()

    for token in tokens:
        if keywords.get(token) is not None:
            result += keywords[token]
        else:
            result += token

    result += "));\n"
    return result


required_stops = 0 # the amount of stops required to close all loops/if statements
required_loop_enders = 0 # the amount of "cat timp" required to close all repeta-loops
def process_line(line: str):
    line = line.strip()
    segments = line.split(";")
    if len(segments) > 1: #if there are more instructions, process them separately
        result = ""
        for segment in segments:
            result += process_line(segment)

        return result

    tokens = segments[0].strip("\n").split()
    result = ""
    global required_stops, required_loop_enders
    required_end = ";"

    if len(tokens) == 0:
        return ""
    

    if tokens[0] == "citeste":
        return process_user_input(segments[0])
    
    elif tokens[0] == "scrie":
        return process_user_output(segments[0])
    
    elif tokens[0] == "daca":
        required_stops += 1
        required_end = ""

    elif tokens[0] == "cat":
        required_stops += 1
        return process_while_structure(segments[0])
    
    elif tokens[0] == "repeta":
        required_loop_enders += 1
        required_end = ""

    elif tokens[0] == "stop":
        required_stops -= 1
        required_end = ""

    elif tokens[0] == "pana":
        required_loop_enders -= 1
        return process_repeat_until(segments[0])
    
    elif tokens[0] == "altfel":
        if "daca" in tokens:
            required_end = ""
        else:
            required_end = "{"

    for token in tokens: #TODO: error-handling
        if keywords.get(token) is not None:
            result += keywords[token]
        else:
            result += token

    result += required_end

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
    g.write("#include <iostream>\nusing namespace std;\nint main(){")

# TODO: move this in the for-loop above
with open("./temp.txt") as f:
    with open("./test.cpp", "a") as g:
        for line in f:
            processed_line = process_line(line)
            g.write(processed_line)
        g.write("return 0;\n}\n")
