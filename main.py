class Identifier:
    def __init__(self, name: str, type: str) -> None:
        self.name = name
        self.type = type


KEYWORDS = {
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
    "altfel": "}else{ ",

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
    "stop": "}",
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

class StopsError(Exception):
    """Raise when there are not enough/too many structure terminators"""

identifiers: list[Identifier] = []
required_stops = 0 # the amount of stops required to close all loops/if statements
required_loop_enders = 0 # the amount of "cat timp" required to close all repeta-loops
stops = 0 # the amount of stops present in code
loop_enders = 0 # the amount of amount of loop closers present in code
current_line = 0 # the line which the program is currently processing

#? HELPER FUNCTIONS
def add_character_at(character: str, string: str, position: int) -> str:
    """
    Adds the given `character` at the given `position` and returns the new string
    """


    return string[:position] + character + string[position:]


def type_of(value: str):
    """
    Determines the type of `value` and returns it as a string
    """

    if value[0] == "\"" and value[-1] == "\"":
        return "sir"

    for x in identifiers:
        if x.name == value:
            return "identificator"

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


def check_for_errors(tokens: list[str], result: str, sep: str = " ", *, operators_allowed: bool = False, reserved_allowed: bool = False,
                      identifiers_allowed: bool = False, literals_allowed: bool = False) -> str:
    """Checks `tokens` for illegal tokens (specified in the params) and throws errors accordingly
    
    Returns the processed tokens added to `result`"""

    for token in tokens:
        if not reserved_allowed:
            if token in RESERVED_KEYWORDS:
                raise UnexpectedKeywordError(f"{token} on line {current_line}")
        else:
            result += KEYWORDS[token] + sep
            continue

        if not operators_allowed:
            if token in OPERATORS:
                raise UnexpectedOperatorError(f"{token} on line {current_line}")
        else:
            if token in OPERATORS:
                result += f"{KEYWORDS[token] if KEYWORDS.get(token) is not None else token}" + sep
                continue
        
        if not literals_allowed:
            if type_of(token) not in ("real", "intreg"):
                raise UnknownTokenError(f"{token} on line {current_line}")
        else:
            if type_of(token) != "identificator":
                result += token + sep
                continue
        
        if not identifiers_allowed:
            if is_identifier(token):
                raise UnknownTokenError(f"{token} on line {current_line}")
        else:
            if not is_identifier(token):
                raise UnknownTokenError(f"{token} on line {current_line}")
            
            result += token + sep
            continue

    return result


def is_identifier(name: str):
    for x in identifiers:
        if x.name == name:
            return True

    return False


def get_identifier_type(name: str):
    for x in identifiers:
        if x.name == name:
            return x.type

    raise MissingIdentifierError(f"Line {current_line}")


#? PREPROCESSING FUNCTIONS
def preprocess_larrow(line: str, pos: int):
    """
    Adds spaces around '<' (if required)
    Returns the modified line and the new position of the character 
    """
    if line[pos + 1] not in ("-", " ", "="):
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


    if line[pos + 1] not in ("=", " '"):
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


def preprocess_equals(line: str, pos: int):
    """
    Adds spaces around the '=' (if required)
    Returns the modified line and the new position of the character
    """

    if line[pos - 1] not in ("!", "<", ">"):
        line = add_character_at(" ", line, pos)
        pos += 1

    try:
        if line[pos + 1] != " ":
            line = add_character_at(" ", line, pos + 1)
    except IndexError:
        pass

    return line, pos


# TODO: handle += -= /= etc
# TODO: split ()[] from +*/%=
def preprocess_arithmetic_operator(line: str, pos: int):
    """
    Adds spaces around arithmetic operators: +/*%[]=()
    Returns the modified line and the new position of the character 
    """


    try:
        if line[pos + 1] != " ":
            line = add_character_at(" ", line, pos + 1)
    except IndexError:
        pass

    try:
        if line[pos - 1] != " ":
            line = add_character_at(" ", line, pos)
            pos += 1
    except IndexError:
        pass

    return line, pos


#? PROCESSING FUNCTIONS
def process_user_output(line: str):
    line = line.strip()
    line = line[6:] # remove "scrie" from the line
    tokens = line.split(",")

    if len(tokens) == 0:
        raise MissingIdentifierError(f"Line {current_line}")

    tokens[-1] = tokens[-1].strip("\n")
    tokens = [x.strip(" ") for x in tokens] # removing unnecesary spaces

    result = "cout<<"

    result = check_for_errors(tokens, result, "<<",
                              operators_allowed=True,
                              identifiers_allowed=True,
                              literals_allowed=True)

    result = result[:-2] # removing extra "<<" from the end
    result += ";\n" # finishing the line

    return result


def process_user_input(line: str):
    line = line.strip()
    line = line[8:] # remove "citeste" from the line
    line, _, data_type = line.partition("(")

    if len(data_type) == 0: # if the type (or paranthesis) is missing
        raise MissingKeywordError(f"Missing '(' or the data type on line {current_line}")
    
    if data_type[-1] != ")":
        raise MissingKeywordError(f"Missing ')' on line {current_line}")

    data_type = data_type[:-1].strip() # remove the ")"
    tokens = line.split(",")
    tokens = [x.strip(" ") for x in tokens] # removing unnecesary spaces

    if len(tokens) == 0: # if there are no variables being read
        raise MissingIdentifierError(f"Line {current_line}")

    result = ""
    result += KEYWORDS[data_type] + " " # the data type of the variables

    for token in tokens: #declaring the variables and saving them for later usage
        
        result += f"{token},"
        identifiers.append(Identifier(token, data_type))

        # check for literals/operators/reserved keywords
        if type_of(token) in ("intreg", "real"):
            raise UnknownTokenError(f"{token} on line {current_line}")
        
        if token in OPERATORS:
            raise UnexpectedOperatorError(f"{token} on line {current_line}")
        
        if token in RESERVED_KEYWORDS:
            raise UnexpectedKeywordError(f"{token} on line {current_line}")

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
    or the end of a repeat-while loop and processes the code accordingly.
    It splits the line into multiple lines after "executa" and processes them
    separately.
    """

    global loop_enders, required_stops

    line = line.strip()
    result = ""
    exe_index = line.find("executa")
    if exe_index != -1: # while-loop
        required_stops += 1
        while_loop, _, other = line.partition("executa")
        tokens = while_loop.split()
        result += "while ("
        
        if tokens[0] != "cat" or tokens[1] != "timp":
            raise MissingKeywordError(f"Line {current_line}")
            
        tokens = tokens[2:] # remove "cat" & "timp"
        
        result = check_for_errors(tokens, result, operators_allowed=True,
                                              identifiers_allowed=True,
                                              literals_allowed=True)
        
        result += KEYWORDS["executa"]

        processed_subline = ""
        if len(other):
            processed_subline = process_line(other)

        return result + processed_subline
    else: # end of repeat-while loop
        loop_enders += 1
        result = "} while("
        tokens = line.split()
        
        if tokens[0] != "cat" or tokens[1] != "timp":
            raise MissingKeywordError(f"Line {current_line}")
        
        tokens = tokens[2:] # remove "cat" & "timp"
        
        result = check_for_errors(tokens, result, operators_allowed=True,
                                              identifiers_allowed=True,
                                              literals_allowed=True)

        result += ");"        
        return result


def process_repeat_until(line: str):
    line = line.strip()
    result = "} while (!(" # negate the condition(s)
    line = line[10:] # remove "pana cand "
    tokens = line.split()

    result = check_for_errors(tokens, result, operators_allowed=True,
                                              identifiers_allowed=True,
                                              literals_allowed=True)

    result += "));\n"
    return result


def process_for_loop(line: str):
    line = line.strip()

    if line[-7:] not in ("executa", "executa;"):
        raise MissingKeywordError(f"\"executa\" on line {current_line}")

    line = line[7:-8] # remove "pentru" & "executa"
    result = "for ("
    tokens = line.split(",")

    identifier, op, init_value = tokens[0].partition("<-") # the declaration of the iterator variable (ex: "i <- 1")
    identifier = identifier.strip()
    init_value = init_value.strip()
    bound = tokens[1].strip() # the value at which the for-loop ends
    
    if len(tokens) > 3:
        raise UnknownTokenError(f"{tokens[3:]} on line {current_line}")
    
    if len(op) == 0:
        raise MissingKeywordError(f"\"<-\" on line {current_line}")
    
    if len(init_value) == 0:
        raise MissingLiteralError(f"Line {current_line}")
        
    if len(identifier) == 0:
        raise MissingIdentifierError(f"Line {current_line}")

    if type_of(identifier) in ("intreg", "real"):
        raise UnknownTokenError(f"{identifier} on line {current_line}") 

    if init_value in RESERVED_KEYWORDS:
        raise UnexpectedKeywordError(f"{init_value} on line {current_line}")
    
    if init_value in OPERATORS:
        raise UnexpectedOperatorError(f"{init_value} on line {current_line}")
    
    if bound in RESERVED_KEYWORDS:
        raise UnexpectedKeywordError(f"{bound} on line {current_line}")
    
    if bound in OPERATORS:
        raise UnexpectedOperatorError(f"{bound} on line {current_line}")

    if type_of(init_value) == "identificator":
        iterator = Identifier(identifier, get_identifier_type(init_value))
    else:
        iterator = Identifier(identifier, type_of(init_value))

    if not is_identifier(iterator.name):
        if iterator.type != "necunoscut":
            result += f"{KEYWORDS[iterator.type]} {iterator.name} = {init_value}; "
        else:
            raise UnknownTokenError(f"{iterator.name} on line {current_line}")
    else:
        result += f"{iterator.name} = {init_value}; "

    increment = tokens[2].replace(" ", "") # removing all spaces added by the preprocessor (or already existing)

    
    # if the increment is an identifier, put the processed sign ("<=" or ">=")
    # depending on whether or not it has a '-' preceding it
    if is_identifier(increment) or is_identifier(increment[1:]):
        if increment[0] == "-":
            result += f"{iterator.name} >= {bound}; {iterator.name} += {increment})" + "{"
        else:
            result += f"{iterator.name} <= {bound}; {iterator.name} += {increment})" + "{"

        return result

    # if the increment is a number literal, set the sign (">=" or "<=") accordingly
    if type_of(increment) in ("real", "intreg"):
        if float(increment) > 0:
            result += f"{iterator.name} <= {bound}; {iterator.name} += {increment})" + "{"
        else:
            result += f"{iterator.name} >= {bound}; {iterator.name} += {increment})" + "{"
    elif type_of(increment) == "caracter":
        result += f"{iterator.name} <= {bound}; {iterator.name} += {increment})" + "{"
    else: # if the increment is a string
        raise UnknownTokenError(f"{increment} on line {current_line}")

    return result


#TODO: support for strings
def process_assignment(line: str):
    line = line.strip()
    result = ""
    tokens = line.split()

    if not is_identifier(tokens[0]): # variable declaration
        result += "float "
        identifiers.append(Identifier(tokens[0], "real"))

    result += tokens[0] + "="
    tokens = tokens[2:]

    result = check_for_errors(tokens, result, operators_allowed=True,
                                              identifiers_allowed=True,
                                              literals_allowed=True)

    return result + ";"


def process_if_statement(line: str):
    line = line.strip()
    result = ""
    tokens = line.split()
    if tokens[-1] not in ("atunci", "atunci;"):
        raise MissingKeywordError(f"\"atunci\" on line {current_line}")
    
    result = KEYWORDS[tokens[0]] # "daca"
    tokens = tokens[1:-1] # removed "daca" & "atunci;"

    result = check_for_errors(tokens, result, operators_allowed=True,
                                              identifiers_allowed=True,
                                              literals_allowed=True)

    return result + KEYWORDS["atunci"]


def process_line(line: str):
    line = line.strip()
    if len(line) == 0: return ""

    segments = line.split(";")
    if len(segments) > 1: #if there are more instructions, process them separately
        result = ""
        for segment in segments:
            result += process_line(segment)

        return result

    tokens = segments[0].strip("\n").split()
    result = ""
    global required_stops, required_loop_enders, loop_enders, stops
    required_end = ";"

    if tokens[0] == "citeste":
        return process_user_input(segments[0])
    
    elif tokens[0] == "scrie":
        return process_user_output(segments[0])
    
    elif tokens[0] == "daca":
        required_stops += 1
        return process_if_statement(segments[0])

    elif tokens[0] == "cat":
        return process_while_structure(segments[0])
    
    elif tokens[0] == "repeta":
        required_loop_enders += 1
        return KEYWORDS["repeta"]

    elif tokens[0] == "stop":
        stops += 1
        return KEYWORDS["stop"]

    elif tokens[0] == "pana":
        loop_enders += 1
        return process_repeat_until(segments[0])
    
    elif tokens[0] == "pentru":
        required_stops += 1
        return process_for_loop(segments[0])
    
    elif tokens[0] == "altfel":
        return KEYWORDS["altfel"]

    elif len(tokens) > 1:
        if tokens[1] == "<-":
            return process_assignment(segments[0])
        
    else:
        raise UnknownTokenError(f"{segments[0]} on line {current_line}")

    for token in tokens: #TODO: error-handling
        if KEYWORDS.get(token) is not None:
            raise UnexpectedKeywordError(f"{token} on line {current_line}")
        else:
            result += token + " "

    result += required_end

    return result + "\n"

# the output file
g = open("./test.cpp", "w+")
g.write("#include <iostream>\nusing namespace std;\nint main(){")

# processing the code and outputting it
with open("./main.pc") as f:
    for line in f: # go line by line

        line = line.strip()
        pos = 0 # the position which it's currently at
        tokens = line.split()
        for token in tokens: # adding ";" after/before each relevant keyword
            pos += len(token) + 1 # the +1 is to compensate for the space (separator)
            if token in ("altfel", "atunci", "executa", "repeta"): # add ';' after the keywords
                line = add_character_at(";", line, pos - 1)
                pos += 1
            elif token in ("stop", "citeste", "scrie"): # add ';' before the keywords
                line = add_character_at(";", line, pos - len(token) - 1)
                pos += 1

        line += "\n" # adding it back (removed above)

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

                case "=":
                    line, i = preprocess_equals(line, i)

                case "+" | "/" | "*" | "%" | "[" | "]" | "(" | ")":
                    line, i = preprocess_arithmetic_operator(line, i)
            i += 1
        
        current_line += 1
        processed_line = process_line(line)

        # Write the processed line to the file
        g.write(processed_line)

    g.write("return 0;\n}\n")
    if abs(required_loop_enders - loop_enders) > 0:
        raise StopsError(f"{required_loop_enders} necessary structure terminators - {loop_enders} present")
    elif abs(required_stops - stops) > 0:
        raise StopsError(f"{required_stops} necessary stops - {stops} present")
    
    g.close()