from modules.utils.log import edit_log


def add_line_after_var_declaration(line, dest_file, states, line_number):
    if (
        states["is_declaration"] == 0
        and states["declaration_passed"] == 1
        and states["space_declaration_place"] == 0
    ):
        dest_file.write("\n")
        if line.strip() != "":
            edit_log("Space needed after variable declaration", line_number)
        states["space_declaration_place"] = 1


def add_line_between_function(line, dest_file, states, line_number):
    if states["in_function"] == 0 and states["function_passed"] == 1:
        if line.strip() != "":
            dest_file.write("\n")
            edit_log("Space needed between function", line_number)
        states["function_passed"] = 0
