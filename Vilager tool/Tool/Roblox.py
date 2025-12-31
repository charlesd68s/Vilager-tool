#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Roblox Multi-Tool - Script Corrigé
Corrections : Injection de domaine Selenium et API Authenticated
"""

import sys
import time
import json
import random
from datetime import datetime

try:
    import requests
except ImportError:
    print("[ERROR] Module 'requests' manquant. Installez-le avec: pip install requests")
    sys.exit(1)

# Couleurs ANSI
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

def clear_screen():
    sys.stdout.write('\033[2J\033[H')
    sys.stdout.flush()

def print_banner():
    clear_screen()
    banner = f"""{Colors.RED}{Colors.BOLD}
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                         ROBLOX TOOL                          ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    {Colors.RESET}"""
    print(banner)

def print_box_title(title):
    border = "═" * (len(title) + 4)
    print(f"\n{Colors.RED}╔{border}╗")
    print(f"║  {Colors.WHITE}{title}{Colors.RED}  ║")
    print(f"╚{border}╝{Colors.RESET}\n")

def get_user_agent():
    return random.choice(USER_AGENTS)

# ======================== COOKIE INFO (CORRIGÉ) ========================
def cookie_info():
    """Vérifie la validité du cookie via l'API d'authentification officielle"""
    print_box_title("COOKIE INFO - VERIFICATION")
    
    cookie = input(f"{Colors.YELLOW}[input]{Colors.RESET} Cookie -> {Colors.WHITE}").strip()
    print(f"{Colors.CYAN}[→]{Colors.RESET} Vérification auprès des serveurs Roblox...{Colors.RESET}")
    
    try:
        headers = {"User-Agent": get_user_agent()}
        # Utilisation de l'API moderne pour vérifier l'identité
        response = requests.get(
            "https://users.roblox.com/v1/users/authenticated",
            headers=headers,
            cookies={".ROBLOSECURITY": cookie}
        )
        
        if response.status_code == 200:
            user_data = response.json()
            user_id = user_data.get('id')
            username = user_data.get('name')
            status = "VALIDE"
            
            # Récupération du solde Robux
            econ_res = requests.get(
                f"https://economy.roblox.com/v1/users/{user_id}/currency",
                cookies={".ROBLOSECURITY": cookie}
            )
            robux = econ_res.json().get('robux', 'N/A') if econ_res.status_code == 200 else "Hidden"
        else:
            status = "INVALIDE / EXPIRÉ"
            username = user_id = robux = "N/A"
            
    except Exception as e:
        status = f"Erreur: {str(e)}"
        username = user_id = robux = "Error"
    
    print(f"\n{Colors.RED}╔══════════════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.RED}║{Colors.RESET} {Colors.GREEN}[01]{Colors.RESET} Status        : {Colors.WHITE}{status:<44}{Colors.RED}║{Colors.RESET}")
    print(f"{Colors.RED}║{Colors.RESET} {Colors.GREEN}[02]{Colors.RESET} Username      : {Colors.WHITE}{username:<44}{Colors.RED}║{Colors.RESET}")
    print(f"{Colors.RED}║{Colors.RESET} {Colors.GREEN}[03]{Colors.RESET} ID            : {Colors.WHITE}{str(user_id):<44}{Colors.RED}║{Colors.RESET}")
    print(f"{Colors.RED}║{Colors.RESET} {Colors.GREEN}[04]{Colors.RESET} Robux         : {Colors.WHITE}{str(robux):<44}{Colors.RED}║{Colors.RESET}")
    print(f"{Colors.RED}╚══════════════════════════════════════════════════════════════╝{Colors.RESET}\n")

# ======================== COOKIE LOGIN (CORRIGÉ) ========================
def cookie_login():
    """Connexion automatique avec gestion du domaine Selenium"""
    print_box_title("COOKIE LOGIN - AUTO-CONNEXION")
    
    try:
        from selenium import webdriver
    except ImportError:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Module 'selenium' manquant (pip install selenium)")
        return
    
    cookie = input(f"{Colors.YELLOW}[input]{Colors.RESET} Cookie -> {Colors.WHITE}").strip()
    
    print(f"\n{Colors.GREEN}[01]{Colors.RESET} Chrome\n{Colors.GREEN}[02]{Colors.RESET} Edge")
    browser_choice = input(f"{Colors.YELLOW}[input]{Colors.RESET} Navigateur -> {Colors.WHITE}")
    
    driver = None
    try:
        if browser_choice in ['1', '01']:
            driver = webdriver.Chrome()
        elif browser_choice in ['2', '02']:
            driver = webdriver.Edge()
        else:
            print("Choix invalide.")
            return

        print(f"{Colors.CYAN}[→]{Colors.RESET} Accès au domaine Roblox...")
        # On doit d'abord charger le domaine pour que le navigateur accepte le cookie
        driver.get("https://www.roblox.com/home")
        time.sleep(2)
        
        print(f"{Colors.CYAN}[→]{Colors.RESET} Injection de la session...")
        driver.add_cookie({
            "name": ".ROBLOSECURITY",
            "value": cookie,
            "domain": ".roblox.com"
        })
        
        print(f"{Colors.GREEN}[✓]{Colors.RESET} Session injectée. Actualisation...")
        driver.refresh()
        
        print(f"\n{Colors.YELLOW}[!]{Colors.RESET} Ne fermez pas cette console avant d'avoir fini.")
        print(f"{Colors.CYAN}[→]{Colors.RESET} Appuyez sur ENTRÉE ici pour fermer le navigateur.")
        input()
        driver.quit()
        
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Une erreur est survenue : {e}")
        if driver:
            driver.quit()

# ======================== AUTRES FONCTIONS ========================

def user_info_by_name():
    print_box_title("RECHERCHE PAR USERNAME")
    username = input(f"{Colors.YELLOW}[input]{Colors.RESET} Username -> {Colors.WHITE}")
    try:
        res = requests.post("https://users.roblox.com/v1/usernames/users", 
                            json={"usernames": [username], "excludeBannedUsers": False})
        data = res.json()
        if data['data']:
            user_id = data['data'][0]['id']
            display_user_stats(user_id)
        else:
            print("Utilisateur non trouvé.")
    except:
        print("Erreur de connexion.")

def user_info_by_id():
    print_box_title("RECHERCHE PAR ID")
    user_id = input(f"{Colors.YELLOW}[input]{Colors.RESET} User ID -> {Colors.WHITE}")
    display_user_stats(user_id)

def display_user_stats(user_id):
    try:
        info = requests.get(f"https://users.roblox.com/v1/users/{user_id}").json()
        print(f"\n{Colors.WHITE}Nom: {info.get('name')}")
        print(f"Display: {info.get('displayName')}")
        print(f"Créé le: {info.get('created')}")
        print(f"Banni: {info.get('isBanned')}")
    except:
        print("Erreur lors de la récupération des données.")

# ======================== MENU ========================
def main():
    while True:
        print_banner()
        print(f"{Colors.GREEN}[01]{Colors.RESET} Cookie Info")
        print(f"{Colors.GREEN}[02]{Colors.RESET} User Info")
        print(f"{Colors.GREEN}[03]{Colors.RESET} User Info")
        print(f"{Colors.GREEN}[04]{Colors.RESET} Cookie Login")
        print(f"\n{Colors.RED}[00]{Colors.RESET} Quitter")
        
        choice = input(f"\n{Colors.YELLOW}[input]{Colors.RESET} Choix -> {Colors.WHITE}")
        
        if choice in ['1', '01']: cookie_info()
        elif choice in ['2', '02']: user_info_by_name()
        elif choice in ['3', '03']: user_info_by_id()
        elif choice in ['4', '04']: cookie_login()
        elif choice in ['0', '00']: break
        
        input(f"\n{Colors.CYAN}[→]{Colors.RESET} Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()