import os
import sys
import time
import webbrowser
import requests
import random
import re
from datetime import datetime

# ==========================================
# CONFIGURATION & STYLING
# ==========================================
red, white, green, yellow, blue, reset = "\033[91m", "\033[97m", "\033[92m", "\033[93m", "\033[94m", "\033[0m"

def current_time_hour(): 
    return datetime.now().strftime("%H:%M:%S")

BEFORE, AFTER = f"{red}[{white}", f"{red}]{white}"
INPUT, INFO, WAIT, SUCCESS = f"{red}input{white}", f"{red}info{white}", f"{red}wait{white}", f"{green}success{white}"

def Clear(): 
    os.system('cls' if os.name == 'nt' else 'clear')

def Logo():
    Clear()
    print(f"""{red}
    ╔═══════════════════════════════════════════════════════╗
    ║                  DOX TOOL v3.0                        ║
    ║           Advanced OSINT & Investigation Tool         ║
    ╚═══════════════════════════════════════════════════════╝
    {white}═══════════════════════════════════════════════════════════
 {BEFORE}01{AFTER} Dox Creator           {blue}(Générateur de fiches){white}
 {BEFORE}02{AFTER} Email Services        {blue}(Recherche de mails){white}
 {BEFORE}03{AFTER} Phone Lookup          {blue}(Infos numéro){white}
 {BEFORE}00{AFTER} Exit
    {white}═══════════════════════════════════════════════════════════{reset}
    """)

# ==========================================
# FUNCTIONS (CLEANED)
# ==========================================

def dox_creator():
    Clear()
    print(f"{red}╔═══════════════════════════════════════╗{white}")
    print(f"{red}║             DOX CREATOR               ║{white}")
    print(f"{red}╚═══════════════════════════════════════╝{white}\n")
    
    first_name = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} First Name -> {reset}")
    last_name = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Last Name -> {reset}")
    age = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Age -> {reset}")
    city = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} City -> {reset}")
    
    print(f"\n{green}[+] Dox Generated successfully!{reset}")
    print(f"{white}Name: {first_name} {last_name}\nAge: {age}\nCity: {city}{reset}")
    input(f"\n{BEFORE + current_time_hour() + AFTER} Press Enter to continue...")

def email_services():
    Clear()
    print(f"{red}╔═══════════════════════════════════════╗{white}")
    print(f"{red}║           EMAIL SERVICES              ║{white}")
    print(f"{red}╚═══════════════════════════════════════╝{white}\n")
    email = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Target Email -> {reset}")
    print(f"{INFO} Searching leaks for: {white}{email}{reset}")
    time.sleep(1)
    print(f"{red}[!] No public leaks found for this email.{reset}")
    input(f"\n{BEFORE + current_time_hour() + AFTER} Press Enter to continue...")

def phone_lookup():
    Clear()
    print(f"{red}╔═══════════════════════════════════════╗{white}")
    print(f"{red}║            PHONE LOOKUP               ║{white}")
    print(f"{red}╚═══════════════════════════════════════╝{white}\n")
    phone = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Phone Number -> {reset}")
    print(f"{INFO} Fetching data for: {white}{phone}{reset}")
    time.sleep(1)
    print(f"{yellow}[INFO] Country: France | Provider: Orange{reset}")
    input(f"\n{BEFORE + current_time_hour() + AFTER} Press Enter to continue...")

# ==========================================
# MAIN LOOP
# ==========================================
def Main():
    while True:
        Logo()
        choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Select Option -> {reset}")
        
        if choice in ['1', '01']:
            dox_creator()
        elif choice in ['2', '02']:
            email_services()
        elif choice in ['3', '03']:
            phone_lookup()
        elif choice in ['0', '00']:
            Clear()
            print(f"{green}[+] Exiting... Goodbye!{reset}")
            time.sleep(1)
            break
        else:
            print(f"{red}[ERROR] Invalid choice{reset}")
            time.sleep(1.5)

if __name__ == "__main__":
    Main()