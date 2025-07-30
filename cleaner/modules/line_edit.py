import re
from modules.utils.log import edit_log
from enums.keyword import keywords


def fix_multiple_spaces(line):
    if line.count("/*") <= 0:
        line = re.sub(r" {2,}", " ", line)
    return line


def fix_space_in_brackets(line):
    line = re.sub(r"\(\s*", "(", line)
    tmp_line = re.sub(r"\s*\)", ")", line)
    if tmp_line.strip(") \t\n") != "":
        line = tmp_line
    line = re.sub(r"\{\s*", "{", line)
    tmp_line = re.sub(r"\s*\}", "}", line)
    if tmp_line.strip("} \t\n") != "":
        line = tmp_line
    line = re.sub(r"\[\s*", "[", line)
    tmp_line = re.sub(r"\s*\]", "]", line)
    if tmp_line.strip("] \t\n") != "":
        line = tmp_line
    return line


def fix_space_before_semicolon(line):
    line = re.sub(r"\s*;", r";", line)
    return line


# TODO : no space arround "-" if "-x"
def fix_space_operator(line, states):
    if states["in_function"]:
        line = re.sub(r"\t*\s*([=!\-\*\+/<>&]{0,1})=\s*\t*", r" \1= ", line)
        line = re.sub(r"\t*\s*([\-\+]{2,})\s*\t*", r"\1", line)
        # We edit only if there is no other operator beside/var
        line = re.sub(
            r"(?<![\+\-/%=\*!><])\s*\t*([\+\-/%><])\s*\t*(?![\+\-\*/%=!><])",
            r" \1 ",
            line,
        )
        # pointer exeption
        line = re.sub(
            r"(?<![\+\-/%=!\(\[\}])\s*\t*\*\s*\t*(?![\+\-\*/%=!abcdefghijklmnopqrstuvwxyz\(\{\[\]\}\)])",
            r" * ",
            line,
        )
        # referencement
        line = re.sub(r"&{1,1}\s*", "&", line)
        # and / or
        line = re.sub(r"\s*([&|]{2,2})\s*", r" \1 ", line)
        # coma
        line = re.sub(r"(?<![0123456789]),\s*(?![0123456789])", r", ", line)
    return line


def fix_space_after_keyword(line):
    for keyword in keywords:
        line = re.sub(rf"\b{keyword}\s*\(", f"{keyword} (", line)
    return line


def fix_edition_in_line(cleaned_line, line_number, states):
    tmp_line = cleaned_line
    cleaned_line = fix_space_in_brackets(cleaned_line)
    if cleaned_line != tmp_line:
        edit_log("Space(s) arround brackets", line_number)

    tmp_line = cleaned_line.rstrip("\n")
    cleaned_line = cleaned_line.rstrip()
    if cleaned_line != tmp_line:
        edit_log("Space(s) at end of line", line_number)

    tmp_line = cleaned_line
    cleaned_line = fix_space_before_semicolon(cleaned_line)
    if cleaned_line != tmp_line:
        edit_log("Space(s) before semicolon", line_number)

    tmp_line = cleaned_line
    cleaned_line = fix_space_operator(cleaned_line, states)
    if cleaned_line != tmp_line:
        edit_log("Space(s) arround operator", line_number)

    tmp_line = cleaned_line
    cleaned_line = fix_space_after_keyword(cleaned_line)
    if cleaned_line != tmp_line:
        edit_log("Space after keyword needed", line_number)

    tmp_line = cleaned_line
    cleaned_line = fix_multiple_spaces(cleaned_line)
    if cleaned_line != tmp_line:
        edit_log("Consecutive spaces", line_number)

    return cleaned_line
