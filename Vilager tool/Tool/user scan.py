import os
import sys
import time
import webbrowser
import requests
import random
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

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

# ==========================================
# BASE DE DONNÉES MASSIVE (EXTRAITE DE USERNAME-TRACKER)
# ==========================================
SITES_DATA = {
    "Steam": {"url": "https://steamcommunity.com/id/{}", "err": None},
    "Telegram": {"url": "https://t.me/{}", "err": ["if you have telegram", "resolve?domain="]},
    "TikTok": {"url": "https://www.tiktok.com/@{}", "err": ["u002f@"]},
    "Instagram": {"url": "https://www.instagram.com/{}", "err": None},
    "PayPal": {"url": "https://www.paypal.com/paypalme/{}", "err": ["slug_name="]},
    "GitHub": {"url": "https://github.com/{}", "err": None},
    "Pinterest": {"url": "https://www.pinterest.com/{}", "err": ["username"]},
    "Snapchat": {"url": "https://www.snapchat.com/add/{}", "err": None},
    "YouTube": {"url": "https://www.youtube.com/@{}", "err": None},
    "Twitch": {"url": "https://www.twitch.tv/{}", "err": None},
    "Reddit": {"url": "https://reddit.com/user/{}", "err": ["nobody on reddit"]},
    "Linktree": {"url": "https://linktr.ee/{}", "err": None},
    "Spotify": {"url": "https://open.spotify.com/user/{}", "err": None},
    "Chess.com": {"url": "https://www.chess.com/member/{}", "err": None},
    "Kaggle": {"url": "https://www.kaggle.com/{}", "err": None},
    "Medium": {"url": "https://medium.com/@{}", "err": ["out of nothing"]},
    "SoundCloud": {"url": "https://soundcloud.com/{}", "err": None},
    "DeviantArt": {"url": "https://www.deviantart.com/{}", "err": None},
    "Keybase": {"url": "https://keybase.io/{}", "err": None},
    "Last.fm": {"url": "https://www.last.fm/user/{}", "err": None},
    "Roblox": {"url": "https://www.roblox.com/user.aspx?username={}", "err": None},
    "GitLab": {"url": "https://gitlab.com/{}", "err": None},
    "Wattpad": {"url": "https://www.wattpad.com/user/{}", "err": ["page can't be found"]},
    "Codecademy": {"url": "https://www.codecademy.com/profiles/{}", "err": ["could not be found"]},
    "Vimeo": {"url": "https://vimeo.com/{}", "err": None},
    "About.me": {"url": "https://about.me/{}", "err": None},
    "Fiverr": {"url": "https://www.fiverr.com/{}", "err": None},
    "ProductHunt": {"url": "https://www.producthunt.com/@{}", "err": None},
    "Dribbble": {"url": "https://dribbble.com/{}", "err": None},
    "Behance": {"url": "https://www.behance.net/{}", "err": None}
    # ... Tu peux rajouter tous les autres sites de Username-Tracker.py ici
}

found_results = []

def check_site(platform, data, username):
    url = data["url"].format(username)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
    try:
        # allow_redirects=False est indispensable pour éviter les "Fakes"
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=False)
        
        if response.status_code == 200:
            content = response.text.lower()
            
            # Vérification anti-fake : le pseudo doit être dans la page
            # et les messages d'erreur du site ne doivent pas y être
            is_fake = False
            if data["err"]:
                for e in data["err"]:
                    if e.lower() in content:
                        is_fake = True
            
            if not is_fake and username.lower() in content:
                print(f"{green}[✓ FOUND]{white} {platform:18} → {url}")
                found_results.append((platform, url))
    except:
        pass

def username_scanner():
    global found_results
    found_results = []
    Clear()
    print(f"{red}╔═══════════════════════════════════════╗{white}")
    print(f"{red}║     USER SCANNER                      ║{white}")
    print(f"{red}╚═══════════════════════════════════════╝{white}\n")
    
    user = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Pseudo -> {reset}").strip().lower()
    if not user: return

    print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Scan profond en cours...\n")
    
    # Utilisation de 50 threads pour la vitesse
    with ThreadPoolExecutor(max_workers=50) as executor:
        for platform, data in SITES_DATA.items():
            executor.submit(check_site, platform, data, user)

    print(f"\n{BEFORE + current_time_hour() + AFTER} {SUCCESS} Scan terminé !")
    print(f"{INFO} Total trouvés : {white}{len(found_results)}{reset}")
    
    if found_results:
        print(f"\n{yellow}--- RÉCAPITULATIF ---{reset}")
        for p, link in found_results:
            print(f"{green}[✓]{reset} {p}: {link}")

    print(f"\n{red}════════════════════════════════════════════════{reset}")
    input(f"{BEFORE + current_time_hour() + AFTER} Appuyez sur ENTRÉE pour continuer...")

def Logo():
    Clear()
    print(f"""{red}
    ╔═══════════════════════════════════════╗
    ║           DOX TOOL v3.0               ║
    ╚═══════════════════════════════════════╝
 {BEFORE}01{AFTER} Username Scanner
 {BEFORE}00{AFTER} Exit
    """)

def Main():
    while True:
        Logo()
        choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Select -> {reset}")
        if choice in ['1', '01']:
            username_scanner()
        elif choice in ['0', '00']:
            break

if __name__ == "__main__":
    Main()