#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Password Hash Manager - Standalone Version
A comprehensive security toolkit for password management, file cracking, and image analysis
"""

import sys
import os
import time
import random
import string
import base64
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

try:
    import bcrypt
    import hashlib
    from hashlib import pbkdf2_hmac
    import piexif
    import exifread
    from PIL import Image
    import rarfile
    import pyzipper
    import tkinter
    from tkinter import filedialog
except ImportError as e:
    print(f"[ERROR] Missing module: {e}")
    print("Please install required modules:")
    print("pip install bcrypt pillow piexif exifread rarfile pyzipper")
    sys.exit(1)

# ============================================
# GLOBAL VARIABLES & UTILITIES
# ============================================

# Color codes for terminal
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'

def get_time():
    """Get current time formatted"""
    return datetime.now().strftime("%H:%M:%S")

def print_banner():
    """Display main banner"""
    banner = f"""
{CYAN}╔════════════════════════════════════════════════════════════╗
║     PASSWORD HASH MANAGER - SECURITY TOOLKIT v1.0          ║
║                    Standalone Edition                      ║
╚════════════════════════════════════════════════════════════╝{RESET}
    """
    print(banner)

def print_section(title):
    """Print section header"""
    print(f"\n{CYAN}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{RESET}\n")

def continue_prompt():
    """Prompt to continue"""
    input(f"\n{YELLOW}[{get_time()}] Press Enter to continue...{RESET}")

def slow_print(text, delay=0.01):
    """Print text slowly for effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ============================================
# MAIN MENU
# ============================================

def show_menu():
    """Display main menu"""
    print_banner()
    menu = f"""
{WHITE}[01]{RESET} {GREEN}Encrypt Password{RESET}
{WHITE}[02]{RESET} {YELLOW}Decrypt Password{RESET}
{WHITE}[03]{RESET} {RED}Crack ZIP/RAR Password{RESET}
{WHITE}[04]{RESET} {BLUE}Get Image EXIF Data{RESET}
{WHITE}[05]{RESET} {MAGENTA}Exit{RESET}
    """
    print(menu)

def show_encryption_methods():
    """Display encryption methods"""
    methods = f"""
{WHITE}[01]{RESET} BCRYPT
{WHITE}[02]{RESET} MD5
{WHITE}[03]{RESET} SHA-1
{WHITE}[04]{RESET} SHA-256
{WHITE}[05]{RESET} PBKDF2 (SHA-256)
{WHITE}[06]{RESET} Base64 Encode/Decode
    """
    print(methods)

# ============================================
# SECTION 1: PASSWORD ENCRYPTION
# ============================================

def encrypt_password(choice, password):
    """Encrypt password using selected method"""
    encrypt_methods = {
        '1': lambda p: bcrypt.hashpw(p.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        '2': lambda p: hashlib.md5(p.encode('utf-8')).hexdigest(),
        '3': lambda p: hashlib.sha1(p.encode('utf-8')).hexdigest(),
        '4': lambda p: hashlib.sha256(p.encode('utf-8')).hexdigest(),
        '5': lambda p: pbkdf2_hmac('sha256', p.encode('utf-8'), "this_is_a_salt".encode('utf-8'), 100000).hex(),
        '6': lambda p: base64.b64encode(p.encode('utf-8')).decode('utf-8')
    }
    
    try:
        return encrypt_methods.get(choice, lambda p: None)(password)
    except Exception as e:
        print(f"{RED}[{get_time()}] [ERROR] Encryption failed: {e}{RESET}")
        return None

def encrypt_mode():
    """Encryption mode handler"""
    print_section("PASSWORD ENCRYPTION")
    show_encryption_methods()
    
    choice = input(f"{CYAN}[{get_time()}] [INPUT] Encryption Method -> {RESET}").strip()
    
    if choice not in ['1', '01', '2', '02', '3', '03', '4', '04', '5', '05', '6', '06']:
        print(f"{RED}[{get_time()}] [ERROR] Invalid choice!{RESET}")
        continue_prompt()
        return

    password = input(f"{CYAN}[{get_time()}] [INPUT] Password to Encrypt -> {RESET}").strip()

    encrypted_password = encrypt_password(choice, password)
    if encrypted_password:
        print(f"{GREEN}[{get_time()}] [SUCCESS] Encrypted Password: {WHITE}{encrypted_password}{RESET}")
        continue_prompt()

# ============================================
# SECTION 2: PASSWORD DECRYPTION
# ============================================

def check_password(encrypted_password, password_test, choice, salt):
    """Check if password matches encrypted version"""
    try:
        methods = {
            '1': lambda pwd: bcrypt.checkpw(pwd.encode('utf-8'), encrypted_password.encode('utf-8')),
            '2': lambda pwd: hashlib.md5(pwd.encode('utf-8')).hexdigest() == encrypted_password,
            '3': lambda pwd: hashlib.sha1(pwd.encode('utf-8')).hexdigest() == encrypted_password,
            '4': lambda pwd: hashlib.sha256(pwd.encode('utf-8')).hexdigest() == encrypted_password,
            '5': lambda pwd: pbkdf2_hmac('sha256', pwd.encode('utf-8'), salt, 100000).hex() == encrypted_password,
            '6': lambda pwd: base64.b64decode(encrypted_password.encode('utf-8')).decode('utf-8') == pwd
        }
        return methods.get(choice, lambda _: False)(password_test)
    except:
        return False

def decrypt_random_character(encrypted_password, choice):
    """Decrypt using random character brute force"""
    try:
        threads_number = int(input(f"{CYAN}[{get_time()}] [INPUT] Threads Number -> {RESET}").strip())
        char_min = int(input(f"{CYAN}[{get_time()}] [INPUT] Password Characters Min -> {RESET}").strip())
        char_max = int(input(f"{CYAN}[{get_time()}] [INPUT] Password Characters Max -> {RESET}").strip())
    except ValueError:
        print(f"{RED}[{get_time()}] [ERROR] Invalid number!{RESET}")
        return

    password_found = False
    generated_passwords = set()
    salt = "this_is_a_salt".encode('utf-8')
    all_characters = string.ascii_letters + string.digits + string.punctuation

    def generate_password():
        return ''.join(random.choices(all_characters, k=random.randint(char_min, char_max)))
    
    def test_decrypt():
        nonlocal password_found
        while not password_found:
            password_test = generate_password()
            if password_test not in generated_passwords:
                generated_passwords.add(password_test)
                if check_password(encrypted_password, password_test, choice, salt):
                    password_found = True
                    print(f'{GREEN}[{get_time()}] [FOUND] Password: {WHITE}{password_test}{RESET}')
                    continue_prompt()
                    return

    print(f"{YELLOW}[{get_time()}] [WAIT] Brute force in progress... (This can take a long time){RESET}")
    
    try:
        with ThreadPoolExecutor(max_workers=threads_number) as executor:
            futures = [executor.submit(test_decrypt) for _ in range(threads_number)]
            for future in futures:
                if password_found:
                    break
                future.result()
    except KeyboardInterrupt:
        print(f"\n{RED}[{get_time()}] [INFO] Brute force stopped by user{RESET}")

def decrypt_wordlist(encrypted_password, choice):
    """Decrypt using wordlist"""
    wordlist_path = input(f"{CYAN}[{get_time()}] [INPUT] Wordlist file path -> {RESET}").strip()
    
    if not os.path.exists(wordlist_path):
        print(f"{RED}[{get_time()}] [ERROR] Wordlist file not found!{RESET}")
        continue_prompt()
        return

    salt = "this_is_a_salt".encode('utf-8')
    print(f"{YELLOW}[{get_time()}] [WAIT] Testing passwords from wordlist...{RESET}")
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                password_test = line.strip()
                if check_password(encrypted_password, password_test, choice, salt):
                    print(f"{GREEN}[{get_time()}] [FOUND] Password: {WHITE}{password_test}{RESET}")
                    continue_prompt()
                    return
                
                if line_num % 1000 == 0:
                    print(f"{BLUE}[{get_time()}] [INFO] Tested {line_num} passwords...{RESET}")
    except Exception as e:
        print(f"{RED}[{get_time()}] [ERROR] Error reading wordlist: {e}{RESET}")
    
    print(f"{RED}[{get_time()}] [INFO] Password not found in wordlist{RESET}")
    continue_prompt()

def decrypt_mode():
    """Decryption mode handler"""
    print_section("PASSWORD DECRYPTION")
    show_encryption_methods()
    
    choice = input(f"{CYAN}[{get_time()}] [INPUT] Encryption Method -> {RESET}").strip()

    if choice not in ['1', '01', '2', '02', '3', '03', '4', '04', '5', '05', '6', '06']:
        print(f"{RED}[{get_time()}] [ERROR] Invalid choice!{RESET}")
        continue_prompt()
        return

    encrypted_password = input(f"{CYAN}[{get_time()}] [INPUT] Encrypted Password -> {RESET}").strip()

    print(f"""
{WHITE}[01]{RESET} Random Character Brute Force
{WHITE}[02]{RESET} Wordlist Attack
    """)

    method = input(f"{CYAN}[{get_time()}] [INPUT] Attack Method -> {RESET}").strip()

    if method in ["01", "1"]:
        decrypt_random_character(encrypted_password, choice)
    elif method in ["02", "2"]:
        decrypt_wordlist(encrypted_password, choice)
    else:
        print(f"{RED}[{get_time()}] [ERROR] Invalid method!{RESET}")
        continue_prompt()

# ============================================
# SECTION 3: ZIP/RAR CRACKER
# ============================================

def choose_zip_rar_file():
    """Choose ZIP/RAR file using file dialog"""
    try:
        print(f"{CYAN}[{get_time()}] [INPUT] Select .zip or .rar file...{RESET}")
        root = tkinter.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file = filedialog.askopenfilename(
            title="Choose a ZIP/RAR file",
            filetypes=[("ZIP/RAR files", "*.zip;*.rar"), ("ZIP files", "*.zip"), ("RAR files", "*.rar")]
        )
        if file:
            print(f"{GREEN}[{get_time()}] [INFO] File selected: {WHITE}{file}{RESET}")
        return file
    except:
        return input(f"{CYAN}[{get_time()}] [INPUT] Enter path to .zip or .rar file -> {RESET}").strip()

def count_encrypted_files(file):
    """Count password-protected files in archive"""
    count = 0
    try:
        if file.lower().endswith('.zip'):
            with pyzipper.AESZipFile(file) as archive:
                for filename in archive.namelist():
                    try:
                        archive.extract(filename, pwd=b'wrongpassword')
                    except RuntimeError:
                        count += 1
        elif file.lower().endswith('.rar'):
            with rarfile.RarFile(file) as archive:
                for filename in archive.namelist():
                    try:
                        archive.extract(filename, pwd='wrongpassword')
                    except rarfile.BadPassword:
                        count += 1
        return count
    except:
        return count

def check_zip_password(file, password_test):
    """Test password on ZIP/RAR file"""
    try:
        if file.lower().endswith('.zip'):
            with pyzipper.AESZipFile(file) as archive:
                archive.extractall(pwd=password_test.encode())
                return True
        elif file.lower().endswith('.rar'):
            with rarfile.RarFile(file) as archive:
                archive.extractall(pwd=password_test)
                return True
    except:
        return False

def crack_zip_random(file):
    """Crack ZIP/RAR with random character brute force"""
    try:
        threads = int(input(f"{CYAN}[{get_time()}] [INPUT] Threads Number -> {RESET}").strip())
        char_min = int(input(f"{CYAN}[{get_time()}] [INPUT] Password Characters Min -> {RESET}").strip())
        char_max = int(input(f"{CYAN}[{get_time()}] [INPUT] Password Characters Max -> {RESET}").strip())
    except ValueError:
        print(f"{RED}[{get_time()}] [ERROR] Invalid number!{RESET}")
        return

    generated = set()
    password_found = False
    all_chars = string.ascii_letters + string.digits + string.punctuation

    def generate_pass():
        return ''.join(random.choice(all_chars) for _ in range(random.randint(char_min, char_max)))

    def test_crack():
        nonlocal password_found
        while not password_found:
            pwd = generate_pass()
            if pwd not in generated:
                generated.add(pwd)
                if check_zip_password(file, pwd):
                    password_found = True
                    print(f'{GREEN}[{get_time()}] [FOUND] Password: {WHITE}{pwd}{RESET}')
                    continue_prompt()
                    return

    print(f"{YELLOW}[{get_time()}] [WAIT] Brute force cracking... (This can take a long time){RESET}")
    
    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(test_crack) for _ in range(threads)]
            for future in futures:
                if password_found:
                    break
                future.result()
    except KeyboardInterrupt:
        print(f"\n{RED}[{get_time()}] [INFO] Cracking stopped by user{RESET}")

def crack_zip_wordlist(file):
    """Crack ZIP/RAR with wordlist"""
    wordlist_path = input(f"{CYAN}[{get_time()}] [INPUT] Wordlist file path -> {RESET}").strip()
    
    if not os.path.exists(wordlist_path):
        print(f"{RED}[{get_time()}] [ERROR] Wordlist file not found!{RESET}")
        continue_prompt()
        return

    print(f"{YELLOW}[{get_time()}] [WAIT] Testing passwords from wordlist...{RESET}")
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                pwd = line.strip()
                if check_zip_password(file, pwd):
                    print(f"{GREEN}[{get_time()}] [FOUND] Password: {WHITE}{pwd}{RESET}")
                    continue_prompt()
                    return
                
                if line_num % 100 == 0:
                    print(f"{BLUE}[{get_time()}] [INFO] Tested {line_num} passwords...{RESET}")
    except Exception as e:
        print(f"{RED}[{get_time()}] [ERROR] Error reading wordlist: {e}{RESET}")
    
    print(f"{RED}[{get_time()}] [INFO] Password not found in wordlist{RESET}")
    continue_prompt()

def crack_zip_rar_mode():
    """ZIP/RAR cracker mode handler"""
    print_section("ZIP/RAR PASSWORD CRACKER")
    
    file = choose_zip_rar_file()
    if not file or not os.path.exists(file):
        print(f"{RED}[{get_time()}] [ERROR] Invalid file!{RESET}")
        continue_prompt()
        return
    
    count = count_encrypted_files(file)
    print(f"{BLUE}[{get_time()}] [INFO] Password-protected files found: {WHITE}{count}{RESET}")
    
    if count == 0:
        print(f"{GREEN}[{get_time()}] [INFO] No password-protected files found!{RESET}")
        continue_prompt()
        return

    print(f"""
{WHITE}[01]{RESET} Random Character Brute Force
{WHITE}[02]{RESET} Wordlist Attack
    """)

    method = input(f"{CYAN}[{get_time()}] [INPUT] Attack Method -> {RESET}").strip()

    if method in ["01", "1"]:
        crack_zip_random(file)
    elif method in ["02", "2"]:
        crack_zip_wordlist(file)
    else:
        print(f"{RED}[{get_time()}] [ERROR] Invalid method!{RESET}")
        continue_prompt()

# ============================================
# SECTION 4: IMAGE EXIF READER
# ============================================

def choose_image_file():
    """Choose image file using file dialog"""
    try:
        print(f"{CYAN}[{get_time()}] [INPUT] Select image file...{RESET}")
        root = tkinter.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file = filedialog.askopenfilename(
            title="Choose an image file",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff"), ("All files", "*.*")]
        )
        if file:
            print(f"{GREEN}[{get_time()}] [INFO] File selected: {WHITE}{file}{RESET}")
        return file
    except:
        return input(f"{CYAN}[{get_time()}] [INPUT] Enter path to image file -> {RESET}").strip()

def clean_exif_value(value):
    """Clean EXIF value for display"""
    if isinstance(value, bytes):
        try:
            return value.decode('utf-8', errors='replace')
        except:
            return base64.b64encode(value).decode('utf-8')
    elif isinstance(value, (list, tuple)):
        return ', '.join(str(v) for v in value)
    elif isinstance(value, dict):
        return {k: clean_exif_value(v) for k, v in value.items()}
    else:
        return value

def get_all_exif(image_path):
    """Extract all EXIF data from image"""
    exif_data = {}

    # Try piexif
    try:
        exif_dict = piexif.load(image_path)
        for ifd in exif_dict:
            if isinstance(exif_dict[ifd], dict):
                for tag in exif_dict[ifd]:
                    tag_name = piexif.TAGS[ifd].get(tag, {"name": tag})["name"]
                    raw_value = exif_dict[ifd][tag]
                    exif_data[f"{tag_name}"] = clean_exif_value(raw_value)
    except:
        pass

    # Try exifread
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f, details=True)
            for tag in tags:
                label = tag.split()[-1]
                if label not in exif_data:
                    exif_data[label] = clean_exif_value(str(tags[tag]))
    except:
        pass
    
    # Get image dimensions
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            depth = len(img.getbands())
            exif_data['Dimension'] = f"{width}x{height}"
            exif_data['Width'] = width
            exif_data['Height'] = height
            exif_data['Depth'] = depth
    except Exception as e:
        exif_data["Image Error"] = str(e)

    # Get file stats
    try:
        file_stats = os.stat(image_path)
        exif_data['Name'] = os.path.basename(image_path)
        exif_data['Type'] = os.path.splitext(image_path)[1]
        exif_data['Size'] = f"{file_stats.st_size / 1024:.2f} KB"
        exif_data['Creation date'] = time.ctime(file_stats.st_ctime)
        exif_data['Date modified'] = time.ctime(file_stats.st_mtime)
        exif_data['Attributes'] = oct(file_stats.st_mode)
        exif_data['Availability'] = 'Available' if os.access(image_path, os.R_OK) else 'Not available'
    except Exception as e:
        exif_data["File Stats Error"] = str(e)
        
    if exif_data:
        max_key_length = max(len(k) for k in exif_data.keys())
        
        print(f"\n{WHITE}{'─' * 100}")
        for key, value in sorted(exif_data.items(), key=lambda x: x[0].lower()):
            print(f" {GREEN}[+]{RESET} {key.ljust(max_key_length)} : {WHITE}{str(value)}{RESET}")
        print(f"{WHITE}{'─' * 100}\n")
    else:
        print(f"{RED}[{get_time()}] [ERROR] No EXIF information found.{RESET}")

def image_exif_mode():
    """Image EXIF reader mode handler"""
    print_section("IMAGE EXIF DATA EXTRACTOR")
    
    image_path = choose_image_file()
    if not image_path or not os.path.exists(image_path):
        print(f"{RED}[{get_time()}] [ERROR] Invalid file!{RESET}")
        continue_prompt()
        return
    
    print(f"{YELLOW}[{get_time()}] [WAIT] Extracting EXIF data...{RESET}")
    get_all_exif(image_path)
    continue_prompt()

# ============================================
# MAIN PROGRAM
# ============================================

def main():
    """Main program loop"""
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            show_menu()
            
            choice = input(f"{CYAN}[{get_time()}] [INPUT] Choice -> {RESET}").strip()

            if choice in ['1', '01']:
                encrypt_mode()
            elif choice in ['2', '02']:
                decrypt_mode()
            elif choice in ['3', '03']:
                crack_zip_rar_mode()
            elif choice in ['4', '04']:
                image_exif_mode()
            elif choice in ['5', '05']:
                print(f"{GREEN}[{get_time()}] [INFO] Exiting... Goodbye!{RESET}")
                break
            else:
                print(f"{RED}[{get_time()}] [ERROR] Invalid choice!{RESET}")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{RED}[{get_time()}] [INFO] Program interrupted by user{RESET}")
            break
        except Exception as e:
            print(f"{RED}[{get_time()}] [ERROR] Unexpected error: {e}{RESET}")
            continue_prompt()

if __name__ == "__main__":
    main()