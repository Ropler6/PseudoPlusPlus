import helpers
from helpers import Counter

def process_user_output(line: str, counter: Counter):
    line = line.strip()
    line = line[6:] # remove "scrie" from the line
    tokens = line.split(",")

    if len(tokens) == 0:
        raise helpers.MissingIdentifierError(f"Line {counter.current_line}")

    tokens[-1] = tokens[-1].strip("\n")
    tokens = [x.strip(" ") for x in tokens] # removing unnecesary spaces

    result = "cout<<"

    result = helpers.check_for_errors(tokens, result, counter, "<<",
                              operators_allowed=True,
                              identifiers_allowed=True,
                              literals_allowed=True)

    result = result[:-2] # removing extra "<<" from the end
    result += ";\n" # finishing the line

    return result


def process_user_input(line: str, counter: Counter):
    line = line.strip()
    line = line[8:] # remove "citeste" from the line
    line, _, data_type = line.partition("(")

    if len(data_type) == 0: # if the type (or paranthesis) is missing
        raise helpers.MissingKeywordError(f"Missing '(' or the data type on line {counter.current_line}")
    
    if data_type[-1] != ")":
        raise helpers.MissingKeywordError(f"Missing ')' on line {counter.current_line}")

    data_type = data_type[:-1].strip() # remove the ")"
    tokens = line.split(",")
    tokens = [x.strip(" ") for x in tokens] # removing unnecesary spaces

    if len(tokens) == 0: # if there are no variables being read
        raise helpers.MissingIdentifierError(f"Line {counter.current_line}")

    result = ""
    result += helpers.KEYWORDS[data_type] + " " # the data type of the variables

    for token in tokens: #declaring the variables and saving them for later usage
        
        result += f"{token},"
        counter.identifiers.append(helpers.Identifier(token, data_type))

        # check for literals/helpers.OPERATORS/reserved helpers.KEYWORDS
        if helpers.type_of(token, counter) in ("intreg", "real"):
            raise helpers.UnknownTokenError(f"{token} on line {counter.current_line}")
        
        if token in helpers.OPERATORS:
            raise helpers.UnexpectedOperatorError(f"{token} on line {counter.current_line}")
        
        if token in helpers.RESERVED_KEYWORDS:
            raise helpers.UnexpectedKeywordError(f"{token} on line {counter.current_line}")

    result = result[:-1] + ";\n" # finishing the line
    result += "cin>>"

    for token in tokens: # adding reading syntax for each token
        result += f"{token}>>"

    result = result[:-2] # removing extra ">>" from the end
    result += ";\n" # finishing the line

    return result


def process_while_structure(line: str, counter: Counter):
    """
    Determines whether the "cat timp" is the start of a while-loop
    or the end of a repeat-while loop and processes the code accordingly.
    It splits the line into multiple lines after "executa" and processes them
    separately.
    """

    line = line.strip()
    result = ""
    exe_index = line.find("executa")
    if exe_index != -1: # while-loop
        counter.required_stops += 1
        while_loop, _, other = line.partition("executa")
        tokens = while_loop.split()
        result += "while ("
        
        if tokens[0] != "cat" or tokens[1] != "timp":
            raise helpers.MissingKeywordError(f"Line {counter.current_line}")
            
        tokens = tokens[2:] # remove "cat" & "timp"

        if len(tokens) == 0:
            raise helpers.MissingIdentifierError(f"Line {counter.current_line}")
        
        result = helpers.check_for_errors(tokens, result, counter, operators_allowed=True,
                                              identifiers_allowed=True,
                                              literals_allowed=True)
        
        result += helpers.KEYWORDS["executa"]

        processed_subline = ""
        if len(other):
            processed_subline = process_line(other, counter)

        return result + processed_subline
    else: # end of repeat-while loop
        counter.loop_enders += 1
        result = "} while("
        tokens = line.split()
        
        if tokens[0] != "cat" or tokens[1] != "timp":
            raise helpers.MissingKeywordError(f"Line {counter.current_line}")
        
        tokens = tokens[2:] # remove "cat" & "timp"
        
        result = helpers.check_for_errors(tokens, result, counter, operators_allowed=True,
                                              identifiers_allowed=True,
                                              literals_allowed=True)

        result += ");"        
        return result


def process_repeat_until(line: str, counter: Counter):
    line = line.strip()
    result = "} while (!(" # negate the condition(s)
    tokens = line.split()

    if tokens[0] != "pana" or tokens[1] != "cand":
        raise helpers.MissingKeywordError(f"Line {counter.current_line}")

    tokens = tokens[2:] # remove ["pana", "cand"]

    result = helpers.check_for_errors(tokens, result, counter, operators_allowed=True,
                                              identifiers_allowed=True,
                                              literals_allowed=True)

    result += "));\n"
    return result


def process_for_loop(line: str, counter: Counter):
    line = line.strip()

    if line[-7:] not in ("executa", "executa;"):
        raise helpers.MissingKeywordError(f"\"executa\" on line {counter.current_line}")

    line = line[7:-8] # remove "pentru" & "executa"
    result = "for ("
    tokens = line.split(",")

    identifier, op, init_value = tokens[0].partition("<-") # the declaration of the iterator variable (ex: "i <- 1")
    identifier = identifier.strip()
    init_value = init_value.strip()
    bound = tokens[1].strip() # the value at which the for-loop ends
    
    if len(tokens) > 3:
        raise helpers.UnknownTokenError(f"{tokens[3:]} on line {counter.current_line}")
    
    if len(op) == 0:
        raise helpers.MissingKeywordError(f"\"<-\" on line {counter.current_line}")
    
    if len(init_value) == 0:
        raise helpers.MissingLiteralError(f"Line {counter.current_line}")
        
    if len(identifier) == 0:
        raise helpers.MissingIdentifierError(f"Line {counter.current_line}")

    if helpers.type_of(identifier, counter) in ("intreg", "real"):
        raise helpers.UnknownTokenError(f"{identifier} on line {counter.current_line}") 

    if init_value in helpers.RESERVED_KEYWORDS:
        raise helpers.UnexpectedKeywordError(f"{init_value} on line {counter.current_line}")
    
    if init_value in helpers.OPERATORS:
        raise helpers.UnexpectedOperatorError(f"{init_value} on line {counter.current_line}")
    
    if bound in helpers.RESERVED_KEYWORDS:
        raise helpers.UnexpectedKeywordError(f"{bound} on line {counter.current_line}")
    
    if bound in helpers.OPERATORS:
        raise helpers.UnexpectedOperatorError(f"{bound} on line {counter.current_line}")

    if helpers.type_of(init_value, counter) == "identificator":
        iterator = helpers.Identifier(identifier, helpers.get_identifier_type(init_value, counter))
    else:
        iterator = helpers.Identifier(identifier, helpers.type_of(init_value, counter))

    if not helpers.is_identifier(iterator.name, counter):
        if iterator.type != "necunoscut":
            result += f"{helpers.KEYWORDS[iterator.type]} {iterator.name} = {init_value}; "
        else:
            raise helpers.UnknownTokenError(f"{iterator.name} on line {counter.current_line}")
    else:
        result += f"{iterator.name} = {init_value}; "

    increment = tokens[2].replace(" ", "") # removing all spaces added by the preprocessor (or already existing)

    
    # if the increment is an identifier, put the processed sign ("<=" or ">=")
    # depending on whether or not it has a '-' preceding it
    if helpers.is_identifier(increment, counter) or helpers.is_identifier(increment[1:], counter):
        if increment[0] == "-":
            result += f"{iterator.name} >= {bound}; {iterator.name} += {increment})" + "{"
        else:
            result += f"{iterator.name} <= {bound}; {iterator.name} += {increment})" + "{"

        return result

    # if the increment is a number literal, set the sign (">=" or "<=") accordingly
    if helpers.type_of(increment, counter) in ("real", "intreg"):
        if float(increment) > 0:
            result += f"{iterator.name} <= {bound}; {iterator.name} += {increment})" + "{"
        else:
            result += f"{iterator.name} >= {bound}; {iterator.name} += {increment})" + "{"
    elif helpers.type_of(increment, counter) == "caracter":
        result += f"{iterator.name} <= {bound}; {iterator.name} += {increment})" + "{"
    else: # if the increment is a string
        raise helpers.UnknownTokenError(f"{increment} on line {counter.current_line}")

    return result


#TODO: support for strings
def process_assignment(line: str, counter: Counter):
    line = line.strip()
    result = ""
    tokens = line.split()

    if not helpers.is_identifier(tokens[0], counter): # variable declaration
        result += "float "
        counter.identifiers.append(helpers.Identifier(tokens[0], "real"))

    result += tokens[0] + "="
    tokens = tokens[2:]

    result = helpers.check_for_errors(tokens, result, counter, operators_allowed=True,
                                              identifiers_allowed=True,
                                              literals_allowed=True)

    return result + ";"


def process_if_statement(line: str, counter: Counter):
    line = line.strip()
    result = ""
    tokens = line.split()
    if tokens[-1] not in ("atunci", "atunci;"):
        raise helpers.MissingKeywordError(f"\"atunci\" on line {counter.current_line}")
    
    result = helpers.KEYWORDS[tokens[0]] # "daca"
    tokens = tokens[1:-1] # removed "daca" & "atunci;"

    if len(tokens) == 0:
        raise helpers.MissingIdentifierError(f"Line {counter.current_line}")

    result = helpers.check_for_errors(tokens, result, counter, operators_allowed=True,
                                              identifiers_allowed=True,
                                              literals_allowed=True)

    return result + helpers.KEYWORDS["atunci"]


def process_line(line: str, counter: Counter):
    line = line.strip()
    if len(line) == 0: return ""

    segments = line.split(";")
    if len(segments) > 1: #if there are more instructions, process them separately
        result = ""
        for segment in segments:
            result += process_line(segment, counter)

        return result

    tokens = segments[0].strip("\n").split()
    result = ""
    required_end = ";"

    if tokens[0] == "citeste":
        return process_user_input(segments[0], counter)
    
    elif tokens[0] == "scrie":
        return process_user_output(segments[0], counter)
    
    elif tokens[0] == "daca":
        counter.required_stops += 1
        return process_if_statement(segments[0], counter)

    elif tokens[0] == "cat":
        return process_while_structure(segments[0], counter)
    
    elif tokens[0] == "repeta":
        counter.required_loop_enders += 1
        return helpers.KEYWORDS["repeta"]

    elif tokens[0] == "stop":
        counter.stops += 1
        return helpers.KEYWORDS["stop"]

    elif tokens[0] == "pana":
        counter.loop_enders += 1
        return process_repeat_until(segments[0], counter)
    
    elif tokens[0] == "pentru":
        counter.required_stops += 1
        return process_for_loop(segments[0], counter)
    
    elif tokens[0] == "altfel":
        return helpers.KEYWORDS["altfel"]

    elif len(tokens) > 1:
        if tokens[1] == "<-":
            return process_assignment(segments[0], counter)
        
    else:
        raise helpers.UnknownTokenError(f"{segments[0]} on line {counter.current_line}")

    for token in tokens: #TODO: error-handling
        if helpers.KEYWORDS.get(token) is not None:
            raise helpers.UnexpectedKeywordError(f"{token} on line {counter.current_line}")
        else:
            result += token + " "

    result += required_end

    return result + "\n"