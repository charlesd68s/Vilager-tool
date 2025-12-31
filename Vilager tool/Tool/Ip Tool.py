import socket
import ssl
import subprocess
import sys
import requests
import time
import random
import os
import signal
from datetime import datetime

# --- CONFIGURATION COULEURS ---
red, white, green, reset = "\033[91m", "\033[97m", "\033[92m", "\033[0m"

def current_time_hour():
    return datetime.now().strftime("%H:%M:%S")

BEFORE, AFTER = f"{red}[{white}", f"{red}]{white}"
ADD, INFO = f"{red}+{white}", f"{red}info{white}"

def Clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def Title(text):
    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(text)

def signal_handler(sig, frame):
    os._exit(0)

# --- NOUVELLE FONCTION : HOST TO IP ---
def HostToIp():
    Clear()
    print(f"\n{BEFORE} DOMAIN RESOLVER {AFTER}")
    # On nettoie l'entrée pour enlever http/https si l'utilisateur le met
    domain = input(f"{BEFORE}input{AFTER} Entrez l'URL du site -> {reset}").replace("https://", "").replace("http://", "").split('/')[0]
    
    try:
        ip = socket.gethostbyname(domain)
        print(f"{BEFORE + ADD + AFTER} Nom de domaine: {white}{domain}{red}")
        print(f"{BEFORE + ADD + AFTER} Adresse IP: {green}{ip}{red}")
        print(f"\n{BEFORE}info{AFTER} Lancement du scan sur cette IP...")
        time.sleep(1.5)
        IpScan(ip) # Utilise ta fonction de scan d'origine
    except socket.gaierror:
        print(f"{BEFORE}error{AFTER} Impossible de résoudre le domaine.")
        time.sleep(2)

# --- TES FONCTIONS DE SCAN D'ORIGINE ---
def IpScan(ip):
    print(f"\n{BEFORE} ANALYSE COMPLÈTE EN COURS {AFTER}")
    ip_type = "ipv4" if "." in ip else "ipv6"
    print(f"{BEFORE + ADD + AFTER} Type: {white}{ip_type}{red}")

    # Test de Ping
    try:
        cmd = f"ping -n 1 {ip}" if os.name == 'nt' else f"ping -c 1 {ip}"
        res = subprocess.run(cmd, shell=True, capture_output=True)
        if res.returncode == 0:
            print(f"{BEFORE + ADD + AFTER} Status: {green}Online{red}")
        else:
            print(f"{BEFORE + ADD + AFTER} Status: {red}Offline/Protected{red}")
    except: pass

    # Récupération API (Détails complets)
    try:
        req = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719").json()
        for key, value in req.items():
            print(f"{BEFORE + ADD + AFTER} {key.capitalize()}: {white}{value}{red}")
    except:
        print(f"{BEFORE}error{AFTER} Erreur API")
    
    input(f"\n{BEFORE}info{AFTER} Appuyez sur Entrée pour revenir au menu...")

def Generator():
    valid, invalid = 0, 0
    while True:
        ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        try:
            cmd = f"ping -n 1 -w 100 {ip}" if os.name == "nt" else f"ping -c 1 -W 1 {ip}"
            result = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                valid += 1
                print(f"{BEFORE + current_time_hour() + AFTER} {green}[valid]{white} -> {green}{ip}{reset}")
            else:
                invalid += 1
                print(f"{BEFORE + current_time_hour() + AFTER} {red}[invalid]{white} -> {red}{ip}{reset}")
        except: pass
        Title(f"Valid: {valid} | Invalid: {invalid}")

# --- TON MENU MIS À JOUR ---
def Main():
    while True:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        Clear()
        print(f"""{red}
    ╔════════════════════════════════════════╗
    ║      {white}SUPER IP TOOL - FULL SCAN{red}         ║
    ╚════════════════════════════════════════╝
    {BEFORE}01{AFTER} {white}IP Scan (Manual Input)
    {BEFORE}02{AFTER} {white}Host to IP (Website Scanner)
    {BEFORE}03{AFTER} {white}IP Generator (Auto-Scan)
    
    {BEFORE}00{AFTER} {white}Quitter
        """)
        choice = input(f"{BEFORE}input{AFTER} Choix -> {reset}")
        
        if choice == '00': break
        elif choice == '01':
            ip = input(f"{BEFORE}input{AFTER} IP -> {reset}")
            IpScan(ip)
        elif choice == '02':
            HostToIp()
        elif choice == '03':
            Generator()

if __name__ == "__main__":
    Main()