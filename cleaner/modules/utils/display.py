def start_display():
    print(
        f"\033[1;{35}m\n==========================================================\n\033[0m"
    )
    print(
        f"\033[1;{35}m         Starting coppying the file and fix errors ...\n\033[0m"
    )
    print(
        f"\033[1;{35}m==========================================================\n\033[0m"
    )


def norminette_display():
    print(
        f"\033[1;{35}m\n==========================================================\n\033[0m"
    )
    print(f"\033[1;{35}m         Launching norminette -> Go fix by hand ...\n\033[0m")
    print(
        f"\033[1;{35}m==========================================================\n\033[0m"
    )


def think_display():
    print(
        f"\033[1;{35}m\n==========================================================\n\033[0m"
    )
    print(f"\033[1;{35}m        Pay attention to automatic modifications ...\n\033[0m")
    print(
        f"\033[1;{35}m==========================================================\n\033[0m"
    )
    print("- Space arround operator '*' because of conflict with pointer")
    print("- Space after ',' in double because conflict with other coma")
