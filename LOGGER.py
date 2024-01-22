from colorama import Fore, Style, init

init(autoreset=True)

colors = {
    'DEBUG': Fore.BLUE,
    'INFO': Fore.GREEN,
    'WARNING': Fore.YELLOW,
    'ERROR': Fore.RED,
    'CRITICAL': f"{Fore.RED}{Style.BRIGHT}",
    'RESET': Fore.RESET
}


def debug(message):
    print(f"{colors['DEBUG']}[DEBUG] {message}{colors['RESET']}")

def info(message):
    print(f"[INFO] {message}")
    
def warning(message):
    print(f"{colors['WARNING']}[WARNING] {message}{colors['RESET']}")

def error(message):
    print(f"{colors['ERROR']}[ERROR] {message}{colors['RESET']}")
    
def critical(message):
    print(f"{colors['CRITICAL']}[CRITICAL] {message}{colors['RESET']}")
