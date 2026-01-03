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
GEN_VALID = f"{green}valid{white}"
GEN_INVALID = f"{red}invalid{white}"

def Clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def Slow(text, speed=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(speed)
    print()

def Censored(text):
    if '@' in text:
        parts = text.split('@')
        return f"{parts[0][:3]}***@***{parts[1]}"
    return f"{text[:3]}***{text[-3:]}"

# ==========================================
# BANNER & MENU
# ==========================================
def Logo():
    Clear()
    print(f"""{red}
    ╔═══════════════════════════════════════════════════════╗
    ║                  DOX TOOL v3.0                        ║
    ║           Advanced OSINT & Investigation Tool         ║
    ╚═══════════════════════════════════════════════════════╝
    {white}═══════════════════════════════════════════════════════════
 {BEFORE}1{AFTER} Dox Creator           {blue}(Complete Dossier Generator){white}
 {BEFORE}2{AFTER} Email Services        {blue}(Email Tracker & Lookup){white}
 {BEFORE}3{AFTER} Phone Lookup          {blue}(Phone Number Information){white}
 {BEFORE}00{AFTER} Exit
    {white}═══════════════════════════════════════════════════════════{reset}
    """)

# ==========================================
# DOX CREATOR
# ==========================================
def dox_creator():
    Clear()
    print(f"{red}╔═══════════════════════════════════════╗{white}")
    print(f"{red}║     COMPLETE DOX CREATOR TOOL        ║{white}")
    print(f"{red}╚═══════════════════════════════════════╝{white}\n")

    print(f"{yellow}[WARNING] Use this tool responsibly and legally.{reset}\n")

    # Basic Info
    print(f"{blue}▼ BASIC INFORMATION{reset}")
    target_pseudo = input(f"{BEFORE}*{AFTER} Target Pseudo/Username : {reset}")
    doxed_by = input(f"{BEFORE}*{AFTER} Doxed By               : {reset}")
    reason = input(f"{BEFORE}*{AFTER} Reason                 : {reset}")

    # Personal Info
    print(f"\n{blue}▼ PERSONAL INFORMATION{reset}")
    real_name = input(f"{BEFORE}*{AFTER} Full Real Name : {reset}")
    age = input(f"{BEFORE}*{AFTER} Age/DOB        : {reset}")
    gender = input(f"{BEFORE}*{AFTER} Gender         : {reset}")

    # Family
    print(f"\n{blue}▼ FAMILY{reset}")
    mother = input(f"{BEFORE}*{AFTER} Mother's Name : {reset}")
    father = input(f"{BEFORE}*{AFTER} Father's Name : {reset}")
    siblings = input(f"{BEFORE}*{AFTER} Siblings      : {reset}")

    # Location
    print(f"\n{blue}▼ LOCATION{reset}")
    country = input(f"{BEFORE}*{AFTER} Country     : {reset}")
    city = input(f"{BEFORE}*{AFTER} City        : {reset}")
    address = input(f"{BEFORE}*{AFTER} Address     : {reset}")
    postal_code = input(f"{BEFORE}*{AFTER} Postal Code : {reset}")

    # Contact & Social
    print(f"\n{blue}▼ CONTACT & SOCIAL{reset}")
    email = input(f"{BEFORE}*{AFTER} Email       : {reset}")
    phone = input(f"{BEFORE}*{AFTER} Phone       : {reset}")
    discord_id = input(f"{BEFORE}*{AFTER} Discord ID  : {reset}")
    discord_tag = input(f"{BEFORE}*{AFTER} Discord Tag : {reset}")

    # Network & PC
    print(f"\n{blue}▼ NETWORK & PC INFO{reset}")
    ip_public = input(f"{BEFORE}*{AFTER} Public IP  : {reset}")
    ip_local = input(f"{BEFORE}*{AFTER} Local IP   : {reset}")
    isp = input(f"{BEFORE}*{AFTER} ISP        : {reset}")
    vpn = input(f"{BEFORE}*{AFTER} VPN (Y/N)  : {reset}")

    # Hardware
    print(f"\n{blue}▼ HARDWARE{reset}")
    cpu = input(f"{BEFORE}*{AFTER} CPU : {reset}")
    gpu = input(f"{BEFORE}*{AFTER} GPU : {reset}")
    ram = input(f"{BEFORE}*{AFTER} RAM : {reset}")

    # Additional
    print(f"\n{blue}▼ ADDITIONAL INFO{reset}")
    other = input(f"{BEFORE}*{AFTER} Other Notes : {reset}")

    # File name
    file_name = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Output filename (leave empty for auto) -> {reset}")
    if not file_name.strip():
        file_name = f"{target_pseudo}_{random.randint(1000, 9999)}"

    # Generate report
    report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          DOX REPORT - {target_pseudo.upper()}                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│ METADATA                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Doxed By    : {doxed_by}
│ Reason      : {reason}
│ Date        : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
│ Target      : {target_pseudo}
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ PERSONAL INFORMATION                                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ [+] Full Name       : {real_name}
│ [+] Age/DOB         : {age}
│ [+] Gender          : {gender}
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FAMILY                                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ [+] Mother          : {mother}
│ [+] Father          : {father}
│ [+] Siblings        : {siblings}
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ LOCATION                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ [+] Country         : {country}
│ [+] City            : {city}
│ [+] Address         : {address}
│ [+] Postal Code     : {postal_code}
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ CONTACT & SOCIAL MEDIA                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ [+] Email           : {email}
│ [+] Phone           : {phone}
│ [+] Discord ID      : {discord_id}
│ [+] Discord Tag     : {discord_tag}
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ NETWORK INFORMATION                                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ [+] Public IP       : {ip_public}
│ [+] Local IP        : {ip_local}
│ [+] ISP             : {isp}
│ [+] VPN             : {vpn}
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ HARDWARE CONFIGURATION                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ [+] CPU             : {cpu}
│ [+] GPU             : {gpu}
│ [+] RAM             : {ram}
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ ADDITIONAL NOTES                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ {other}
└─────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
Generated by Dox Tool v3.0
═══════════════════════════════════════════════════════════════════════════════
"""

    # Save file
    output_file = f"Dox-{file_name}.txt"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n{green}[SUCCESS]{white} Dossier saved successfully!")
        print(f"{green}[+]{white} File: {blue}{output_file}{reset}")
    except Exception as e:
        print(f"{red}[ERROR] Could not save file: {e}{reset}")

    time.sleep(3)

# ==========================================
# EMAIL SERVICES
# ==========================================
def email_services():
    Clear()
    print(f"{red}╔═══════════════════════════════════════╗{white}")
    print(f"{red}║         EMAIL SERVICES               ║{white}")
    print(f"{red}╚═══════════════════════════════════════╝{white}\n")

    print(f" {BEFORE}1{AFTER} Email Tracker (Social Scan)")
    print(f" {BEFORE}2{AFTER} Email Lookup (DNS/MX)")
    print(f" {BEFORE}00{AFTER} Back\n")

    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Choice -> {reset}")

    if choice in ['1']:
        email_tracker()
    elif choice in ['2']:
        email_lookup()

def email_tracker():
    Clear()
    print(f"{red}╔═══════════════════════════════════════╗{white}")
    print(f"{red}║         EMAIL TRACKER                ║{white}")
    print(f"{red}╚═══════════════════════════════════════╝{white}\n")

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    def check_instagram(email):
        try:
            session = requests.Session()
            headers = {'User-Agent': user_agent, 'X-Requested-With': 'XMLHttpRequest'}
            response = session.get("https://www.instagram.com/accounts/emailsignup/", headers=headers)
            token = session.cookies.get('csrftoken')
            if token:
                headers["x-csrftoken"] = token
                response = session.post("https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/",
                                      headers=headers, data={"email": email}, timeout=5)
                if "email_is_taken" in response.text:
                    return True
            return False
        except:
            return "Error"

    def check_twitter(email):
        try:
            session = requests.Session()
            response = session.get("https://api.twitter.com/i/users/email_available.json",
                                 params={"email": email}, timeout=5)
            if response.status_code == 200:
                return response.json().get("taken", False)
            return False
        except:
            return "Error"

    def check_spotify(email):
        try:
            session = requests.Session()
            response = session.get('https://spclient.wg.spotify.com/signup/public/v1/account',
                                 params={'validate': '1', 'email': email}, timeout=5)
            if response.status_code == 200:
                return response.json().get("status") == 20
            return False
        except:
            return "Error"

    email = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Email -> {reset}")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Censored: {white}{Censored(email)}{reset}")
    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Scanning platforms...{reset}\n")

    checks = [
        ("Instagram", check_instagram),
        ("Twitter", check_twitter),
        ("Spotify", check_spotify)
    ]

    found = 0
    not_found = 0

    for name, func in checks:
        result = func(email)
        if result == True:
            print(f"{green}[✓ FOUND]{white} {name}{reset}")
            found += 1
        elif result == "Error":
            print(f"{yellow}[? ERROR]{white} {name}{reset}")
        else:
            print(f"{red}[✗ NOT FOUND]{white} {name}{reset}")
            not_found += 1

    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Found: {white}{found}{red} | Not Found: {white}{not_found}{reset}")
    input(f"\n{BEFORE + current_time_hour() + AFTER} Press Enter to continue...")

def email_lookup():
    try:
        import dns.resolver
    except ImportError:
        Clear()
        print(f"{red}[ERROR] dnspython module not installed{reset}")
        print(f"{yellow}[INFO] Install with: pip install dnspython{reset}")
        input(f"\n{BEFORE + current_time_hour() + AFTER} Press Enter to continue...")
        return

    Clear()
    print(f"{red}╔═══════════════════════════════════════╗{white}")
    print(f"{red}║         EMAIL LOOKUP                 ║{white}")
    print(f"{red}╚═══════════════════════════════════════╝{white}\n")

    email = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Email -> {reset}")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Censored: {white}{Censored(email)}{reset}")
    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Retrieving information...{reset}\n")

    try:
        domain = email.split('@')[-1]
        name = email.split('@')[0]

        # MX Records
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            mx_servers = [str(record.exchange) for record in mx_records]
            mx_str = ' / '.join(mx_servers)
        except:
            mx_str = "None"

        # SPF Records
        try:
            spf_records = dns.resolver.resolve(domain, 'TXT')
            spf_str = "Found"
        except:
            spf_str = "None"

        # DMARC
        try:
            dmarc_records = dns.resolver.resolve(f'_dmarc.{domain}', 'TXT')
            dmarc_str = "Found"
        except:
            dmarc_str = "None"

        print(f"{white}─────────────────────────────────────────────────────{reset}")
        print(f"{INFO} Email      : {white}{email}{reset}")
        print(f"{INFO} Name       : {white}{name}{reset}")
        print(f"{INFO} Domain     : {white}{domain}{reset}")
        print(f"{INFO} MX Servers : {white}{mx_str}{reset}")
        print(f"{INFO} SPF        : {white}{spf_str}{reset}")
        print(f"{INFO} DMARC      : {white}{dmarc_str}{reset}")
        print(f"{white}─────────────────────────────────────────────────────{reset}")

    except Exception as e:
        print(f"{red}[ERROR] {e}{reset}")

    input(f"\n{BEFORE + current_time_hour() + AFTER} Press Enter to continue...")

# ==========================================
# PHONE LOOKUP
# ==========================================
def phone_lookup():
    try:
        import phonenumbers
        from phonenumbers import geocoder, carrier, timezone
    except ImportError:
        Clear()
        print(f"{red}[ERROR] phonenumbers module not installed{reset}")
        print(f"{yellow}[INFO] Install with: pip install phonenumbers{reset}")
        input(f"\n{BEFORE + current_time_hour() + AFTER} Press Enter to continue...")
        return

    Clear()
    print(f"{red}╔═══════════════════════════════════════╗{white}")
    print(f"{red}║       PHONE NUMBER LOOKUP            ║{white}")
    print(f"{red}╚═══════════════════════════════════════╝{white}\n")

    print(f"{yellow}[INFO] Enter phone number (e.g., 5551234567 or +15551234567){reset}\n")

    phone_number = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Phone Number -> {reset}")
    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Analyzing...{reset}\n")

    try:
        phone_number = phone_number.replace(" ", "").replace("-", "")
        # Si le numéro ne commence pas par +, on suppose qu'il est local et on ajoute le code pays du Canada (+1)
        if not phone_number.startswith('+'):
            phone_number = '+1' + phone_number
        parsed = phonenumbers.parse(phone_number, None)

        valid = "Valid" if phonenumbers.is_valid_number(parsed) else "Invalid"
        country = phonenumbers.region_code_for_number(parsed)
        region = geocoder.description_for_number(parsed, "en")
        operator = carrier.name_for_number(parsed, "en")
        number_type = "Mobile" if phonenumbers.number_type(parsed) == phonenumbers.PhoneNumberType.MOBILE else "Fixed Line"
        timezones = timezone.time_zones_for_number(parsed)
        tz = timezones[0] if timezones else "Unknown"
        formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        print(f"{white}─────────────────────────────────────────────────────{reset}")
        print(f"{INFO} Phone      : {white}{phone_number}{reset}")
        print(f"{INFO} Formatted  : {white}{formatted}{reset}")
        print(f"{INFO} Status     : {white}{valid}{reset}")
        print(f"{INFO} Country    : {white}{country}{reset}")
        print(f"{INFO} Region     : {white}{region}{reset}")
        print(f"{INFO} Operator   : {white}{operator}{reset}")
        print(f"{INFO} Type       : {white}{number_type}{reset}")
        print(f"{INFO} Timezone   : {white}{tz}{reset}")
        print(f"{white}─────────────────────────────────────────────────────{reset}")

    except Exception as e:
        print(f"{red}[ERROR] Invalid phone number format{reset}")
        print(f"{yellow}[INFO] Use format: 5551234567 or +15551234567{reset}")

    input(f"\n{BEFORE + current_time_hour() + AFTER} Press Enter to continue...")

# ==========================================
# MAIN FUNCTION
# ==========================================
def Main():
    while True:
        Logo()
        choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Select Option -> {reset}")

        if choice in ['1']:
            dox_creator()
        elif choice in ['2']:
            email_services()
        elif choice in ['3']:
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
    try:
        Main()
    except KeyboardInterrupt:
        Clear()
        print(f"\n{red}[!] Program interrupted by user{reset}")
        sys.exit(0)
