import preprocessor, processor, helpers
from io import TextIOWrapper

def force_exit(g: TextIOWrapper, output_file: str):
    """
    Used when the program is terminated due to a syntax error which triggered
    an exception. It closes `g` and clears the contents of `output_file`.
    """

    g.close()
    with open(output_file, "w+") as f:
        f.write("")

    input("Press Enter to close this window...")

def main():
    input_file = input("Input file: ")
    output_file = input("Output file (leave blank for default): ")
    print("\n\n")

    if len(output_file) == 0:
        output_file = "./main.cpp"

    g = open(output_file, "w+")
    g.write("#include <iostream>\nusing namespace std;\nint main(){")

    counter = helpers.Counter()
    # processing the code and outputting it
    with open(input_file, "r") as f:
        for line in f: # go line by line

            line = line.strip()
            pos = 0 # the position which it's currently at
            tokens = line.split()
            for token in tokens: # adding ";" after/before each relevant keyword
                pos += len(token) + 1 # the +1 is to compensate for the space (separator)
                if token in ("altfel", "atunci", "executa", "repeta"): # add ';' after the keywords
                    line = helpers.add_character_at(";", line, pos - 1)
                    pos += 1
                elif token in ("stop", "citeste", "scrie"): # add ';' before the keywords
                    line = helpers.add_character_at(";", line, pos - len(token) - 1)
                    pos += 1

            line += "\n" # adding it back (removed above)

            i = 0
            try:
                while i < len(line): # processing the current line
                                    # using a while-loop to properly have len(line) updated
                    match line[i]:
                        case "<":
                            line, i = preprocessor.preprocess_larrow(line, i, counter)

                        case "-":
                            line, i = preprocessor.preprocess_minus(line, i, counter)

                        case ">":
                            line, i = preprocessor.preprocess_rarrow(line, i, counter)

                        case "=":
                            line, i = preprocessor.preprocess_equals(line, i, counter)

                        case "/":
                            line, i = preprocessor.preprocess_division(line, i, counter)

                        case "+" | "*" | "%" | "[" | "]" | "(" | ")":
                            line, i = preprocessor.preprocess_arithmetic_operator(line, i, counter)
                    i += 1
            except Exception as e:
                print(f"{type(e).__name__}: {e}")
                force_exit(g, output_file)
                return

            counter.current_line += 1
            try: # try to process the current line
                processed_line = processor.process_line(line, counter)
            except Exception as e: # if an exception is raised, display it and terminate the program
                print(f"{type(e).__name__}: {e}")
                force_exit(g, output_file)
                return

            # Write the processed line to the file
            g.write(processed_line)

        g.write("return 0;\n}\n")
        if abs(counter.required_loop_enders - counter.loop_enders) > 0:
            print(f"StopsError: {counter.required_loop_enders} necessary structure terminators - {counter.loop_enders} present")
            force_exit(g, output_file)
            return
        elif abs(counter.required_stops - counter.stops) > 0:
            print(f"StopsError: {counter.required_stops} necessary stops - {counter.stops} present")
            force_exit(g, output_file)
            return
        
        g.close()

    input("Press Enter to close this window...")


if __name__ == "__main__":
    main()
