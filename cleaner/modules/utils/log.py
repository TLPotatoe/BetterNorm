def delete_log(error, line_number):
    print(f"\033[1;{31}m❌ Line {line_number:>3} - {error} -> Line deleted\033[0m")


def edit_log(edit, line_number):
    print(f"\033[1;{36}m🧹 Line {line_number:>3} - {edit} -> Line edited\033[0m")


def warning_log(warning, line_number):
    print(f"\033[1;{33}m👀 Line {line_number:>3} - {warning} -> Need check\033[0m")
