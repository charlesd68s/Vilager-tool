import sys
import time
import requests

# ANSI Colors for styling
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    print(f"""{Colors.CYAN}{Colors.BOLD}
    ╔══════════════════════════════════════════════╗
    ║           ROBLOX COOKIE MANAGER V3           ║
    ╚══════════════════════════════════════════════╝{Colors.RESET}""")

# ======================== 1. COOKIE INFO ========================
def cookie_info():
    print(f"\n{Colors.YELLOW}[?] Enter the .ROBLOSECURITY Cookie:{Colors.RESET}")
    cookie = input(f"{Colors.WHITE}>> ").strip()
    
    # Standard format for Roblox cookies
    cookies = {".ROBLOSECURITY": cookie}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    try:
        # Check authentication status
        res = requests.get("https://users.roblox.com/v1/users/authenticated", cookies=cookies, headers=headers)
        
        if res.status_code == 200:
            data = res.json()
            u_id = data['id']
            u_name = data['name']
            
            # Fetch Robux Balance
            robux_res = requests.get(f"https://economy.roblox.com/v1/users/{u_id}/currency", cookies=cookies).json()
            robux = robux_res.get('robux', 'Hidden/Unknown')

            print(f"\n{Colors.GREEN}[✓] Valid Cookie!{Colors.RESET}")
            print(f"{Colors.CYAN}User Name   :{Colors.WHITE} {u_name}")
            print(f"{Colors.CYAN}User ID     :{Colors.WHITE} {u_id}")
            print(f"{Colors.CYAN}Robux       :{Colors.YELLOW} {robux} R${Colors.RESET}")
        else:
            print(f"{Colors.RED}[X] Invalid or Expired Cookie.{Colors.RESET}")

    except Exception as e:
        print(f"{Colors.RED}[ERROR] Connection failed: {e}{Colors.RESET}")

# ======================== 2. COOKIE LOGIN ========================
def cookie_login():
    try:
        from selenium import webdriver
    except ImportError:
        print(f"{Colors.RED}[!] Selenium is not installed. Run: pip install selenium{Colors.RESET}")
        return

    print(f"\n{Colors.YELLOW}[?] Paste Cookie to Inject:{Colors.RESET}")
    cookie = input(f"{Colors.WHITE}>> ").strip()

    print(f"\n{Colors.GREEN}[1]{Colors.RESET} Chrome")
    print(f"{Colors.GREEN}[2]{Colors.RESET} Edge")
    nav = input(f"{Colors.YELLOW}Select Browser -> {Colors.WHITE}")

    driver = None
    try:
        if nav == '1': 
            driver = webdriver.Chrome()
        elif nav == '2': 
            driver = webdriver.Edge()
        else: 
            return

        # Load domain first to allow cookie injection
        print(f"{Colors.CYAN}[→] Opening Roblox...{Colors.RESET}")
        driver.get("https://www.roblox.com/home")
        time.sleep(2) 
        
        # Injecting the security cookie
        driver.add_cookie({
            "name": ".ROBLOSECURITY",
            "value": cookie,
            "domain": ".roblox.com"
        })
        
        print(f"{Colors.GREEN}[✓] Session Injected. Refreshing...{Colors.RESET}")
        driver.refresh()
        
        print(f"\n{Colors.YELLOW}[!] Do not close this console until you are finished.{Colors.RESET}")
        input(f"{Colors.CYAN}Press Enter to close the browser and exit...{Colors.RESET}")
        driver.quit()
        
    except Exception as e:
        print(f"{Colors.RED}[ERROR] Login failed: {e}{Colors.RESET}")
        if driver: 
            driver.quit()

# ======================== MAIN MENU ========================
def main():
    while True:
        print_banner()
        print(f"{Colors.GREEN}[1]{Colors.RESET} Check Cookie (Get Info & Robux)")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Browser Login (Auto-Injection)")
        print(f"{Colors.RED}[0]{Colors.RESET} Exit")
        
        choice = input(f"\n{Colors.YELLOW}Choice -> {Colors.WHITE}")
        
        if choice == '1': 
            cookie_info()
        elif choice == '2': 
            cookie_login()
        elif choice == '0': 
            break
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

if __name__ == "__main__":
    main()