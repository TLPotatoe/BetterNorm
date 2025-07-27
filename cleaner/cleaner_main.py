#!/usr/bin/env python3
import argparse
from modules.line_add import add_line_after_var_declaration, add_line_between_function
from modules.utils.log import delete_log, edit_log
from modules.line_deletion import delete_invalid_line
from modules.line_edit import (
    fix_edition_in_line,
)
from modules.check_pattern import update_status
from modules.utils.display import start_display, norminette_display, think_display
import subprocess


def clean_line(line, number, states):
    # Delete if line is invalid
    cleaned_line = delete_invalid_line(line, number, states)
    if cleaned_line == "":
        return ""

    # Warning -> edit
    cleaned_line = fix_edition_in_line(cleaned_line, number, states)

    states["in_comment_block"] -= line.count("*/")
    return cleaned_line + "\n"


def copy_file_properly(src, dest):
    states = {
        "nb_brackets": 0,
        "in_comment_block": 0,
        "last_was_empty": 0,
        "in_function": 0,
        "is_declaration": 0,
        "declaration_passed": 0,
        "space_declaration_place": 0,
        "function_passed": 0,
    }
    with open(src, "r") as source_file:
        lines = source_file.readlines()
    with open(dest, "w") as dest_file:
        for i in range(len(lines)):
            update_status(states, lines[i])
            add_line_after_var_declaration(lines[i], dest_file, states, i + 1)
            add_line_between_function(lines[i], dest_file, states, i + 1)
            # Empty line in function
            if states["in_function"]:
                if lines[i].strip() == "":
                    delete_log("Empty line in function", i + 1)
            lines[i] = clean_line(lines[i], i + 1, states)
            # Write the line if not empty
            if lines[i] != "":
                dest_file.write(lines[i])


# TODO : si pas de dest -> src
# TODO : supprimer les espace après les types -> mettre un tab
# TODO : nettoyer le copy_file_properly
def main():
    parser = argparse.ArgumentParser(
        description="Create a copy of a c file but clean basic norminette errors"
    )
    parser.add_argument("src", help="Source File")
    parser.add_argument("dest", help="Destination File")

    args = parser.parse_args()
    start_display()
    copy_file_properly(args.src, args.dest)
    norminette_display()
    subprocess.run(["norminette", args.dest])
    think_display()


if __name__ == "__main__":
    main()
