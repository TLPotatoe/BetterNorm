import os
import sys
import subprocess
from cleaner.cleaner_main import copy_file_properly
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

def checkflag():
	if "nauto" in sys.argv:
		norm_auto()
	if "gitp" in sys.argv:
		gitp()

def find_flags(name:str):
	temp = ""
	all_flag = [
		"gitp",
		"-gitf"
	]
	match name:
		case "gitpm":
			for arg in sys.argv[1:]:
				if not arg in all_flag:
					return arg
			return 0

def gitp():
	global PUSH_FLAG
	if find_flags("gitpm") and (PUSH_FLAG or "-gitf" in sys.argv):
		print(Fore.RESET)
		os.system("find . -name '*.out' -type f && find . -name '*.out' -type f -delete")
		os.system(f"git add . && git commit -m {find_flags('gitpm')} && git push")
	elif not find_flags("gitpm"):
		print(Fore.RED + "Missing message to push")
	else:
		print(Fore.RED + "Error push.")

def norm_auto():
	path = os.getcwd()
	for thing in os.listdir(path):
		if os.path.isdir(os.path.join(path, thing)) and not thing.find("ex"):
			print(Fore.CYAN + thing, end=" ")
			for file in os.listdir(os.path.join(path, thing)):
				if file.startswith("ft_") and file.endswith(".c"):
					print(file)
					copy_file_properly(os.path.join(path, thing, file), os.path.join(path, thing, file + "REWRITTEN"))
			if not len(os.listdir(os.path.join(path, thing))): print("No files.")

def check_norm():
	global PUSH_FLAG
	norm_result = run_with_output('norminette -R CheckDefine | grep "Error"')
	print(Fore.LIGHTYELLOW_EX + "Norminette")
	if not len(norm_result.stdout):
		print(Fore.LIGHTGREEN_EX + "OK")
	elif "operr" in sys.argv:
		find_file(norm_result.stdout)
		print(norm_result.stdout)
	else:
		print(norm_result.stdout)
		PUSH_FLAG = False

def find_file(result_moul):
	index = 0
	for _ in range(result_moul.count("\n")):
		name = result_moul[result_moul.find("ft_", index):result_moul.find(".c", index)+2]
		index = result_moul.find(".c", index)
		result_grep = run_with_output(f"find . -name '{name}'").stdout
		if name in result_grep: os.system(f'open {result_grep}')

def check_compile(path):
	print(Fore.LIGHTBLUE_EX + "Compiler test")
	for thing in os.listdir(path):
		if os.path.isdir(os.path.join(path, thing)) and not thing.find("ex"):
			print(Fore.CYAN + thing, end=" ")
			for file in os.listdir(os.path.join(path, thing)):
				if file.startswith("ft_") and file.endswith(".c"):
					print(file)
					compiler_and_try(os.path.join(path, thing, file))
			if not len(os.listdir(os.path.join(path, thing))): print("No files.")

def compiler_and_try(path):
	global PUSH_FLAG
	check_file_content(path)
	result = run_with_output(f"cc -Wall -Werror -Wextra {path}")
	if str(result.stderr).find("undefined reference to `main'") != -1:
		print(Fore.LIGHTGREEN_EX + "COMPILE OK")
	else:
		print(Fore.LIGHTRED_EX + f"{os.path.basename(os.path.dirname(path))} Error.\n", result.stderr)
		PUSH_FLAG = False
		if "operr" in sys.argv: os.system("open " + path)

def check_file_content(file):
	exclulist = ["stdio.h", "int main(", "printf"]
	with open(file, "r") as f:
		for line in f.readlines():
			for i in exclulist:
				if i in line:
					print(Fore.RED + line, end="")
					if "operr" in sys.argv: os.system("open " + file)

def run_with_output(command):
	result = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=5)
	return result

if __name__ == '__main__':
	main()
