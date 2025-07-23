def get_nb_bracket_line(line):
    return line.count("{") - line.count("}")


def update_status(states, line):
    states["nb_brackets"] += get_nb_bracket_line(line)
    states["in_function"] = states["nb_brackets"] >= 1
    return states
