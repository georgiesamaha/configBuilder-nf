from colorama import Fore, Style, init

# Initialise colorama
init(autoreset=True)

# 
def nfconfigBuilder():
    def ask_for_input(prompt, type_=None, min_=None, max_=None, num_of_attempts=3):
        for _ in range(num_of_attempts):
            val = input(Fore.GREEN + prompt + Style.RESET_ALL)
            if type_ is not None:
                try:
                    val = type_(val)
                except ValueError:
                    print(Fore.RED + f"Input type must be {type_.__name__}!" + Style.RESET_ALL)
                    continue
            if min_ is not None and val < min_:
                print(Fore.RED + f"Input must be greater than or equal to {min_}!" + Style.RESET_ALL)
            elif max_ is not None and val > max_:
                print(Fore.RED + f"Input must be less than or equal to {max_}!" + Style.RESET_ALL)
            else:
                return val
        raise ValueError('Invalid Input')