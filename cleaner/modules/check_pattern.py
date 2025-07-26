from enums.types import types
import re


def get_nb_bracket_line(line):
    return line.count("{") - line.count("}")


# TODO : check avec find de python + reggex pour les t_*
def is_variable_declaration(line):
    for type in types:
        if line.find(type) != -1:
            return 1
    if re.search(r"\bt_", line):
        return 1
    return 0


def update_status(states, line):
    states["nb_brackets"] += get_nb_bracket_line(line)
    states["in_function"] = states["nb_brackets"] >= 1
    states["is_declaration"] = is_variable_declaration(line)
    if states["is_declaration"] == 1 and states["in_function"]:
        states["declaration_passed"] = 1
    return states
