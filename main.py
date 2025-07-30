import os
import sys
import subprocess
from colorama import Fore
from cleaner.cleaner_main import copy_file_properly

PUSH_FLAG = True

def main():
    global PUSH_FLAG
    #os.system("cls" if os.name == "nt" else "clear")
    curr_dir = os.getcwd()
    print(f"Executing command at{curr_dir}")
    check_norm()
    check_compile(curr_dir)
    checkflag()


def find_flags(name):
    if name == "mess":
        if sys.argv.index("gitp") != -1:
            return sys.argv[sys.argv.index("gitp") + 1]


def checkflag():
    if "gitp" in sys.argv and PUSH_FLAG and len(sys.argv) > 2:
        print(Fore.RESET)
        os.system(
            "find . -name '*.out' -type f && find . -name '*.out' -type f -delete"
        )
        os.system(f"git add . && git commit -m {find_flags('mess')} && git push")
    elif "gitp" in sys.argv and "-force" in sys.argv:
        print(Fore.RESET)
        os.system(
            "find . -name '*.out' -type f && find . -name '*.out' -type f -delete"
        )
        os.system(f"git add . && git commit -m {find_flags('mess')} && git push")
    elif "gitp" in sys.argv:
        print("Can't push")


def check_norm():
    global PUSH_FLAG
    norm_result = run_with_output('norminette | grep "Error"')
    print(Fore.LIGHTBLUE_EX + "Norminette")
    print(norm_result.stdout)
    if not len(norm_result.stdout):
        print(Fore.LIGHTGREEN_EX + "OK")
    elif "operr" in sys.argv:
        find_file(norm_result.stdout)
    else:
        PUSH_FLAG = False


def find_file(result_moul):
    name = result_moul[result_moul.find("ft_") : result_moul.find(".c") + 2]
    result_grep = run_with_output(f"find . -name '{name}'").stdout
    if name in result_grep:
        os.system(f"open {result_grep}")


def check_compile(path):
    print(Fore.LIGHTBLUE_EX + "Compiler test")
    for thing in os.listdir(path):
        if os.path.isdir(os.path.join(path, thing)) and not thing.find("ex"):
            print(Fore.CYAN + thing, end=" ")
            for file in os.listdir(os.path.join(path, thing)):
                if file.startswith("ft_") and file.endswith(".c"):
                    print(file)
                    compiler_and_try(os.path.join(path, thing, file))
            if not len(os.listdir(os.path.join(path, thing))):
                print("No files.")


def compiler_and_try(path):
    global PUSH_FLAG
    check_file_content(path)
    result = run_with_output(f"cc -Wall -Werror -Wextra {path}")
    if str(result.stderr).find("undefined reference to `main'") != -1:
        print(Fore.LIGHTGREEN_EX + "COMPILE OK")
    else:
        print(
            Fore.LIGHTRED_EX + f"{os.path.basename(os.path.dirname(path))} Error.\n",
            result.stderr,
        )
        PUSH_FLAG = False
        if "operr" in sys.argv:
            os.system("open " + path)


def check_file_content(file):
    exclulist = ["stdio.h", "int main(", "printf"]
    with open(file, "r") as f:
        for line in f.readlines():
            for i in exclulist:
                if i in line:
                    print(Fore.RED + line, end="")
                    if "operr" in sys.argv:
                        os.system("open " + file)


def run_with_output(command):
    result = subprocess.run(
        command, shell=True, text=True, capture_output=True, timeout=5
    )
    return result


if __name__ == "__main__":
    main()
