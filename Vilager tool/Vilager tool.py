import os
import shutil

# --- COULEURS ---
G = '\033[92m'  # Vert clair
DG = '\033[32m' # Vert foncé
W = '\033[0m'   # Reset

# --- CONFIGURATION (Noms affichés dans le menu) ---
options = {
    "01": "Crack password",
    "02": "Doxing",
    "03": "Ip Tool",
    "04": "Roblox",
    "05": "Virus Builder",
    "06": "Website",
}

# --- CORRESPONDANCE (Noms exacts des fichiers dans le dossier 'Tool') ---
# Corrigé selon ton image "image_0c6cff.png"
file_mapping = {
    "01": "Crack pasworld.py",
    "02": "Dox tool.py",
    "03": "Ip Tool.py",
    "04": "Roblox.py",
    "05": "Virus-Builder.py",
    "06": "Website.py",
}

def Clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def GetCenter(text):
    terminal_width = shutil.get_terminal_size().columns
    return "\n".join(line.center(terminal_width) for line in text.split('\n'))

def Banner():
    logo_ascii = f"""
    {G}____   ____.__.__                                    __                .__   
\   \ /   /|  |  | _____     ____   ___________    _/  |_  ____   ____ |  |  
 \   Y   / |  |  | \__  \   / ___\_/ __ \_  __ \   \   __\/  _ \ /  _ \|  |  
    {DG}  \     /  |  |  |__/ __ \_/ /_/  >  ___/|  | \/    |  | (  <_> |  <_> )  |__
   \___/   |__|____(____  /\___  / \___  >__|       |__|  \____/ \____/|____/
                        \//_____/      \/                                    
    """
    
    menu_content = f"""
            {G} ┌─ [{W}I{G}] Info                                                                       Next [{W}N{G}] ─┐                                                                                           
             {W}│         {G}[{W}01{G}]{W} {options["01"].ljust(30)} {G}[{W}04{G}]{W} {options["04"].ljust(30)}           │
             │         {G}[{W}02{G}]{W} {options["02"].ljust(30)} {G}[{W}05{G}]{W} {options["05"].ljust(30)}           │
             │         {G}[{W}03{G}]{W} {options["03"].ljust(30)} {G}[{W}06{G}]{W} {options["06"].ljust(30)}           │
│                                                                                           │
└───────────────────────────────────────────────────────────────────────────────────────────┘
    """
    
    print(GetCenter(logo_ascii))
    print(GetCenter(menu_content))

while True:
    try:
        Clear()
        Banner()
        
        print(f" {G}──────────────────────────────────────────────────────────────────────────────────────────")
        print(f" {G}({W}charlemup@villagertool{G})─{G}[{W}~/Vilager Tool{G}]")
        choice = input(f" {G}└─{W}$ ").strip().zfill(2)

        if choice in file_mapping:
            real_filename = file_mapping[choice]
            # On cherche dans le dossier "Tool" qui est au même niveau que Vilager tool.py
            file_path = os.path.join("Tool", real_filename)
            
            if os.path.exists(file_path):
                # Utilisation de python pour lancer le sous-script
                os.system(f"python \"{file_path}\"")
                input(f"\n{G}Appuyez sur Entrée pour revenir...")
            else:
                print(f"\n{DG}Erreur: Le fichier '{real_filename}' est introuvable.")
                print(f"Chemin tenté : {os.path.abspath(file_path)}")
                input("Appuyez sur Entrée...")
        elif choice.lower() in ['exit', 'quit', 'q']:
            break
            
    except Exception as e:
        print(f"{DG}Erreur: {e}")
        input("Appuyez sur Entrée...")
        break