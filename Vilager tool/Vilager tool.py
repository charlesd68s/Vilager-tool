import os
import shutil
import re

# --- COULEURS avec dégradé vert ---
G1 = '\033[38;2;0;100;0m'      # Vert très foncé
G2 = '\033[38;2;0;128;0m'      # Vert foncé
G3 = '\033[38;2;34;139;34m'    # Vert forêt
G4 = '\033[38;2;50;205;50m'    # Vert lime
G5 = '\033[38;2;144;238;144m'  # Vert clair
G6 = '\033[38;2;152;251;152m'  # Vert pâle
G = '\033[92m'                  # Vert clair
DG = '\033[32m'                 # Vert foncé
W = '\033[0m'                   # Reset

# --- CONFIGURATION ---
options = {
    "01": "Crack password", "02": "Doxing", "03": "Ip Tool",
    "04": "Roblox user", "05": "Username Scan", "06": "Website",
    "07": "DDOS Tool", "08": "Roblox cookie", "09": "Ip logger",
    "10": "Fake website", "11": "Incoming", "12": "Incoming",
    "13": "Incoming", "14": "Incoming", "15": "Incoming",
    "16": "Incoming", "17": "Incoming", "18": "Incoming",
    "19": "Incoming", "20": "Incoming", "21": "Incoming",
    "22": "Incoming", "23": "Incoming", "24": "Incoming",
    "25": "Incoming", "26": "Incoming", "27": "Incoming",
}

file_mapping = {
    "01": "Crack pasworld.py", "02": "Dox tool.py", "03": "Ip Tool.py",
    "04": "Roblox ac scan.py", "05": "user scan.py", "06": "Website.py",
    "07": "DDOS stress.py", "08": "roblox cookie.py", "09": "ip logger.py",
    "10": "fake website.py", "11": "incoming.py", "12": "incoming.py",
    "13": "incoming.py", "14": "incoming.py", "15": "incoming.py",
    "16": "incoming.py", "17": "incoming.py", "18": "incoming.py",
    "19": "incoming.py", "20": "incoming.py", "21": "incoming.py",
    "22": "incoming.py", "23": "incoming.py", "24": "incoming.py",
    "25": "incoming.py", "26": "incoming.py", "27": "incoming.py",
}

current_page = 1
LIGNES_PAR_COLONNE = 7
COLONNES = 3

def Clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def visible_len(text):
    """Calcule la longueur du texte sans les codes ANSI."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return len(ansi_escape.sub('', text))

def GetCenter(text):
    """Centre chaque ligne de texte par rapport à la largeur du terminal."""
    terminal_width = shutil.get_terminal_size().columns
    centered_lines = []
    for line in text.split('\n'):
        line_width = visible_len(line)
        spaces = (terminal_width - line_width) // 2
        centered_lines.append(" " * spaces + line)
    return "\n".join(centered_lines)

def Banner(page):
    logo_ascii = f"""
{G1}____   ____.__.__                                    __                .__   
{G2}\\   \\ /   /|  |  | _____     ____   ___________    _/  |_  ____   ____ |  |  
{G3} \\   Y   / |  |  | \\__  \\   / ___\\_/ __ \\_  __ \\   \\   __\\/  _ \\ /  _ \\|  |  
{G4}  \\     /  |  |  |__/ __ \\_/ /_/  >  ___/|  | \\/    |  | (  <_> |  <_> )  |__
{G5}   \\___/   |__|____(____  /\\___  / \\___  >__|       |__|  \\____/ \\____/|____/
{G6}                        \\//_____/      \\/                                    {W}"""
    
    items_per_page = LIGNES_PAR_COLONNE * COLONNES
    total_pages = (len(options) + items_per_page - 1) // items_per_page
    start = (page - 1) * items_per_page + 1
    end = min(start + items_per_page - 1, len(options))
    
    header = f"{G}┌─ [{W}I{G}] Info                            Page {page}/{total_pages}  Back [{W}B{G}] Next [{W}N{G}] ─┐{W}"
    
    lines = []
    for ligne in range(LIGNES_PAR_COLONNE):
        line_content = ""
        for col in range(COLONNES):
            option_num = start + (col * LIGNES_PAR_COLONNE) + ligne
            if option_num <= end:
                opt_key = str(option_num).zfill(2)
                opt_name = options[opt_key]
                line_content += f"{G}[{W}{opt_key}{G}]{W} {opt_name.ljust(18)}  "
            else:
                line_content += " " * 25
        lines.append(line_content.rstrip())
    
    print(GetCenter(logo_ascii))
    print(GetCenter(header))
    print(GetCenter("\n".join(lines)))

# --- BOUCLE PRINCIPALE ---
while True:
    try:
        Clear()
        Banner(current_page)
        
        terminal_width = shutil.get_terminal_size().columns
        
        # Textes du prompt
        label = f"{G}[{W}Vilager Tool{G}]{W}"
        pointer = f"{G}└─{W} "
        
        # Calcul précis des espaces pour égaliser au centre
        label_spaces = " " * ((terminal_width - visible_len(label)) // 2)
        pointer_spaces = " " * ((terminal_width - visible_len(pointer)) // 2)

        print(f"\n{label_spaces}{label}")
        choice = input(f"{pointer_spaces}{pointer}").strip().lower()

        # Navigation et Logique
        items_per_page = LIGNES_PAR_COLONNE * COLONNES
        total_pages = (len(options) + items_per_page - 1) // items_per_page
        
        if choice in ['n', 'next']:
            current_page = current_page + 1 if current_page < total_pages else 1
            continue
        elif choice in ['b', 'back']:
            current_page = current_page - 1 if current_page > 1 else total_pages
            continue
        elif choice in ['exit', 'quit', 'q']:
            break
        
        choice_key = choice.zfill(2)
        if choice_key in file_mapping:
            file_path = os.path.join("Tool", file_mapping[choice_key])
            if os.path.exists(file_path):
                os.system(f"python \"{file_path}\"")
                input(f"\n{G}Appuyez sur Entrée pour revenir...")
            else:
                print(GetCenter(f"{DG}Erreur: Fichier introuvable.{W}"))
                input()
            
    except Exception as e:
        print(f"Erreur: {e}")
        break