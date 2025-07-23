import re
from enums.forbidden import forbidden_functions, forbidden_includes
from modules.utils.log import delete_log


def clean_comment_line(line, in_function, in_comment_block):
    if in_function:
        if in_comment_block:
            if line.count("*/") >= 1:
                line = re.sub(r"^([ \t]*)[^*/]*\*/\s*", r"\1", line)
                if line.strip() == "":
                    return ""
            else:
                return ""
        if re.match(r"^\s*//", line) or line.strip() == "":
            return ""
        line = re.sub(r"//.*", "", line)
    return line


def clean_forbidden_function(line):
    for function in forbidden_functions:
        if re.search(r"\b" + function + r"\(", line):
            return ""
    return line


def clean_forbidden_import(line):
    for include in forbidden_includes:
        if include in line:
            return ""
    return line


def clean_multiple_empty_line(line, state):
    tmp_line = line.strip()
    if tmp_line == "":
        if state["last_was_empty"] == 1:
            return ""
        state["last_was_empty"] = 1
    else:
        state["last_was_empty"] = 0
    return line


def delete_invalid_line(line, line_number, states):
    update_comment_block = line.count("/*")
    states["in_comment_block"] = (states["in_comment_block"] + update_comment_block) > 0

    cleaned_line = clean_forbidden_function(line)
    if cleaned_line == "":
        delete_log("Forbidden function", line_number)
        return ""

    cleaned_line = clean_forbidden_import(cleaned_line)
    if cleaned_line == "":
        delete_log("Forbidden include", line_number)
        return ""

    cleaned_line = clean_comment_line(
        cleaned_line,
        states["in_function"],
        (1 if states["in_comment_block"] > 0 else 0),
    )
    if cleaned_line == "":
        delete_log("Comment forbidden in function", line_number)
        return ""

    cleaned_line = clean_multiple_empty_line(cleaned_line, states)
    if cleaned_line == "":
        delete_log("Multiple empty lines", line_number)
        return ""
    states["in_comment_block"] = (states["in_comment_block"] - line.count("*/")) < 0
    return cleaned_line
