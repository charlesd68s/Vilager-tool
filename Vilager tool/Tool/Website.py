import socket
import os
import time
import webbrowser
import urllib3
import requests
import json
import ssl
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from datetime import datetime

# --- DESIGN CONFIGURATION ---
red, white, green, yellow, blue, reset = "\033[91m", "\033[97m", "\033[92m", "\033[93m", "\033[94m", "\033[0m"
def current_time(): return time.strftime("%H:%M:%S")
BEFORE, AFTER = f"{red}[", f"]{white}"
INFO, WAIT, ERROR, ADD, VULN, SAFE = f"{blue}INFO{white}", f"{yellow}WAIT{white}", f"{red}ERROR{white}", f"{green}+{white}", f"{red}VULN{white}", f"{green}SAFE{white}"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers_global = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(f"""{red}
    ╔═══════════════════════════════════════════════════════╗
    ║     VILLAGER TOOL - PROFESSIONAL WEB SCANNER v2.0     ║
    ║              Advanced Security Assessment             ║
    ╚═══════════════════════════════════════════════════════╝{reset}""")

# ==========================================
# ADVANCED PORT SCANNER WITH SERVICE DETECTION
# ==========================================
def advanced_port_scan(ip, ports_info):
    print(f"\n{BEFORE}{WAIT}{AFTER} Scanning {len(ports_info)} ports...")
    open_ports = []
    
    for port, desc in ports_info.items():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex((ip, port))
                
                if result == 0:
                    # Try to grab banner
                    try:
                        s.send(b'HEAD / HTTP/1.0\r\n\r\n')
                        banner = s.recv(1024).decode('utf-8', errors='ignore')[:100]
                        service = banner.split('\n')[0] if banner else "Unknown"
                    except:
                        service = "Service detected"
                    
                    open_ports.append(port)
                    print(f"{BEFORE}{ADD}{AFTER} Port {green}{port}{white} - {green}OPEN{white} | {desc} | {service}")
        except:
            pass
    
    return open_ports

# ==========================================
# SSL/TLS CERTIFICATE CHECKER
# ==========================================
def check_ssl_certificate(domain):
    print(f"\n{BEFORE}{WAIT}{AFTER} Checking SSL/TLS certificate...")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                
                print(f"{BEFORE}{ADD}{AFTER} Certificate issuer: {white}{cert.get('issuer', 'Unknown')}")
                print(f"{BEFORE}{ADD}{AFTER} Valid until: {white}{cert.get('notAfter', 'Unknown')}")
                print(f"{BEFORE}{SAFE}{AFTER} SSL/TLS: {green}Valid & Secure{white}")
    except ssl.SSLError:
        print(f"{BEFORE}{VULN}{AFTER} SSL/TLS: {red}Invalid or expired certificate!{white}")
    except:
        print(f"{BEFORE}{ERROR}{AFTER} Unable to check SSL certificate")

# ==========================================
# HTTP SECURITY HEADERS CHECKER
# ==========================================
def check_security_headers(url):
    print(f"\n{BEFORE}{WAIT}{AFTER} Analyzing HTTP security headers...")
    
    security_headers = {
        'X-Frame-Options': 'Protects against clickjacking',
        'X-Content-Type-Options': 'Prevents MIME-sniffing',
        'Strict-Transport-Security': 'Enforces HTTPS',
        'Content-Security-Policy': 'Prevents XSS attacks',
        'X-XSS-Protection': 'XSS filter',
        'Referrer-Policy': 'Controls referrer information'
    }
    
    try:
        r = requests.get(url, timeout=5, headers=headers_global, verify=False)
        headers = r.headers
        
        missing = []
        for header, desc in security_headers.items():
            if header in headers:
                print(f"{BEFORE}{SAFE}{AFTER} {header}: {green}Present{white} - {desc}")
            else:
                print(f"{BEFORE}{VULN}{AFTER} {header}: {red}Missing{white} - {desc}")
                missing.append(header)
        
        if len(missing) > 3:
            print(f"\n{BEFORE}{VULN}{AFTER} {red}Warning: {len(missing)} security headers missing!{white}")
    except:
        print(f"{BEFORE}{ERROR}{AFTER} Unable to check headers")

# ==========================================
# TECHNOLOGY DETECTION (CMS, Frameworks)
# ==========================================
def detect_technologies(url):
    print(f"\n{BEFORE}{WAIT}{AFTER} Detecting technologies...")
    
    try:
        r = requests.get(url, timeout=5, headers=headers_global, verify=False)
        headers = r.headers
        content = r.text.lower()
        
        # Server detection
        server = headers.get('Server', 'Unknown')
        print(f"{BEFORE}{ADD}{AFTER} Server: {white}{server}")
        
        # CMS Detection
        cms_signatures = {
            'WordPress': ['wp-content', 'wp-includes'],
            'Joomla': ['joomla', 'option=com_'],
            'Drupal': ['drupal', 'sites/default'],
            'Magento': ['magento', 'mage/'],
            'Shopify': ['shopify', 'cdn.shopify'],
        }
        
        detected_cms = []
        for cms, signatures in cms_signatures.items():
            if any(sig in content for sig in signatures):
                detected_cms.append(cms)
                print(f"{BEFORE}{ADD}{AFTER} CMS Detected: {green}{cms}{white}")
        
        if not detected_cms:
            print(f"{BEFORE}{INFO}{AFTER} No common CMS detected")
            
        # Framework detection
        if 'x-powered-by' in headers:
            print(f"{BEFORE}{ADD}{AFTER} Framework: {white}{headers['x-powered-by']}")
            
    except:
        print(f"{BEFORE}{ERROR}{AFTER} Unable to detect technologies")

# ==========================================
# SENSITIVE FILES SCANNER
# ==========================================
def scan_sensitive_files(url):
    print(f"\n{BEFORE}{WAIT}{AFTER} Scanning for sensitive files...")
    
    sensitive_paths = [
        '/robots.txt', '/sitemap.xml', '/.git/config', '/.env',
        '/admin', '/login', '/phpinfo.php', '/config.php',
        '/backup.sql', '/database.sql', '/.htaccess', '/wp-config.php',
        '/.DS_Store', '/composer.json', '/package.json'
    ]
    
    found = []
    for path in sensitive_paths:
        try:
            test_url = urljoin(url, path)
            r = requests.get(test_url, timeout=3, headers=headers_global, verify=False, allow_redirects=False)
            
            if r.status_code == 200:
                found.append(path)
                print(f"{BEFORE}{VULN}{AFTER} Found: {green}{path}{white} (Status: {r.status_code})")
            elif r.status_code in [301, 302]:
                print(f"{BEFORE}{INFO}{AFTER} {path} - Redirected ({r.status_code})")
        except:
            pass
    
    if not found:
        print(f"{BEFORE}{SAFE}{AFTER} No sensitive files exposed")
    
    return found

# ==========================================
# ADVANCED VULNERABILITY SCANNER
# ==========================================
def advanced_vuln_scan(url, domain):
    print(f"\n{BEFORE}{WAIT}{AFTER} Advanced vulnerability scanning...")
    
    scanned_links = set()
    to_scan = [url]
    vulnerabilities = {'sql': [], 'xss': [], 'forms': []}
    
    # Enhanced SQL payloads
    sql_payloads = [
        "'", '"', "' OR '1'='1", "' OR 1=1--", "admin'--",
        "' UNION SELECT NULL--", "1' AND '1'='1", "' OR 'a'='a",
        "1 AND 1=1", "' WAITFOR DELAY '00:00:05'--"
    ]
    sql_indicators = [
        "sql syntax", "mysql", "sqlstate", "syntax error",
        "unclosed quotation", "quoted string", "database error"
    ]
    
    # XSS payloads
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "javascript:alert('XSS')"
    ]
    
    scan_count = 0
    while to_scan and scan_count < 30:  # Limit for performance
        current_url = to_scan.pop(0)
        if current_url in scanned_links:
            continue
        
        scanned_links.add(current_url)
        scan_count += 1
        
        try:
            # SQL Injection test
            for payload in sql_payloads[:5]:  # Test first 5 payloads
                test_url = current_url + payload
                r = requests.get(test_url, timeout=3, headers=headers_global, verify=False)
                
                if any(ind in r.text.lower() for ind in sql_indicators):
                    if current_url not in vulnerabilities['sql']:
                        vulnerabilities['sql'].append(current_url)
                        print(f"{BEFORE}{VULN}{AFTER} SQL Injection: {red}{current_url}{white}")
                    break
            
            # Get page content for analysis
            r = requests.get(current_url, timeout=3, headers=headers_global, verify=False)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Find forms (potential XSS/CSRF targets)
            forms = soup.find_all('form')
            if forms:
                vulnerabilities['forms'].append((current_url, len(forms)))
                print(f"{BEFORE}{INFO}{AFTER} Found {len(forms)} form(s) on: {white}{current_url}")
            
            # Discover new links
            for a in soup.find_all('a', href=True):
                link = urljoin(current_url, a['href'])
                if domain in link and link not in scanned_links and len(to_scan) < 50:
                    to_scan.append(link)
                    
        except:
            continue
    
    # Summary
    print(f"\n{BEFORE}{INFO}{AFTER} Scan completed: {scan_count} pages analyzed")
    if vulnerabilities['sql']:
        print(f"{BEFORE}{VULN}{AFTER} {red}Found {len(vulnerabilities['sql'])} potential SQL injection points{white}")
    if vulnerabilities['forms']:
        print(f"{BEFORE}{INFO}{AFTER} Found {len(vulnerabilities['forms'])} pages with forms")
    
    return vulnerabilities

# ==========================================
# FULL SCAN (MAIN FUNCTION)
# ==========================================
def run_scan_all():
    clear()
    banner()
    
    url_in = input(f"\n{BEFORE}{current_time()}{AFTER} Target URL -> {reset}")
    if "://" not in url_in:
        url_in = "https://" + url_in
    
    domain = urlparse(url_in).netloc
    report = {'url': url_in, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    print(f"\n{BEFORE}{INFO}{AFTER} Starting comprehensive scan on: {green}{domain}{white}")
    
    # 1. Resolve IP
    try:
        ip = socket.gethostbyname(domain)
        print(f"{BEFORE}{ADD}{AFTER} Resolved IP: {white}{ip}")
        report['ip'] = ip
    except:
        print(f"{BEFORE}{ERROR}{AFTER} Unable to resolve domain")
        return
    
    # 2. Port Scanning
    ports_info = {
        21: "FTP - File Transfer Protocol",
        22: "SSH - Secure Shell", 
        23: "Telnet - Insecure Remote Access",
        25: "SMTP - Email Server",
        53: "DNS - Domain Name System",
        80: "HTTP - Web Server",
        110: "POP3 - Email Retrieval",
        143: "IMAP - Email Access",
        443: "HTTPS - Secure Web",
        3306: "MySQL - Database",
        3389: "RDP - Remote Desktop",
        5432: "PostgreSQL - Database",
        8080: "HTTP-Alt - Alternative Web Port",
        8443: "HTTPS-Alt - Alternative Secure Port"
    }
    report['open_ports'] = advanced_port_scan(ip, ports_info)
    
    # 3. SSL Certificate Check
    if 'https' in url_in:
        check_ssl_certificate(domain)
    
    # 4. Security Headers
    check_security_headers(url_in)
    
    # 5. Technology Detection
    detect_technologies(url_in)
    
    # 6. Sensitive Files
    report['sensitive_files'] = scan_sensitive_files(url_in)
    
    # 7. Vulnerability Scan
    report['vulnerabilities'] = advanced_vuln_scan(url_in, domain)
    
    # 8. Save Report
    save_report = input(f"\n{BEFORE}?{AFTER} Save report to file? (y/n): {reset}").lower()
    if save_report == 'y':
        filename = f"scan_report_{domain}_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=4)
        print(f"{BEFORE}{ADD}{AFTER} Report saved: {green}{filename}{white}")
    
    input(f"\n{BEFORE}END{AFTER} Press Enter to return to menu...")

# ==========================================
# ENHANCED GOOGLE DORKING
# ==========================================
def run_dorking():
    clear()
    banner()
    
    print(f"\n{white}═══ GOOGLE DORKING - ADVANCED SEARCH BUILDER ═══{reset}\n")
    print(f"{yellow}Available operators:{reset}")
    print(f"  {green}[01]{white} inurl:      - Search in URL")
    print(f"  {green}[02]{white} intitle:    - Search in page title")
    print(f"  {green}[03]{white} site:       - Limit to specific domain")
    print(f"  {green}[04]{white} filetype:   - Search specific file types")
    print(f"  {green}[05]{white} intext:     - Search in page content")
    print(f"  {green}[06]{white} cache:      - View cached version")
    print(f"  {green}[07]{white} related:    - Find similar sites")
    print(f"  {green}[00]{white} Finish and search\n")
    
    database = []
    
    while True:
        choice = input(f"{BEFORE}{current_time()}{AFTER} Select operator -> {reset}")
        
        if choice in ['0', '00']:
            break
        elif choice == '1':
            kw = input(f"  → Keyword for URL: {reset}")
            database.append(f"inurl:{kw}")
            print(f"{BEFORE}{ADD}{AFTER} Added: {green}inurl:{kw}{white}")
        elif choice == '2':
            kw = input(f"  → Keyword for title: {reset}")
            database.append(f"intitle:{kw}")
            print(f"{BEFORE}{ADD}{AFTER} Added: {green}intitle:{kw}{white}")
        elif choice == '3':
            domain = input(f"  → Target domain: {reset}")
            database.append(f"site:{domain}")
            print(f"{BEFORE}{ADD}{AFTER} Added: {green}site:{domain}{white}")
        elif choice == '4':
            ext = input(f"  → File extension (pdf, doc, xls, txt...): {reset}")
            database.append(f"filetype:{ext}")
            print(f"{BEFORE}{ADD}{AFTER} Added: {green}filetype:{ext}{white}")
        elif choice == '5':
            txt = input(f"  → Text to search: {reset}")
            database.append(f"intext:{txt}")
            print(f"{BEFORE}{ADD}{AFTER} Added: {green}intext:{txt}{white}")
        elif choice == '6':
            url = input(f"  → URL to check cache: {reset}")
            database.append(f"cache:{url}")
            print(f"{BEFORE}{ADD}{AFTER} Added: {green}cache:{url}{white}")
        elif choice == '7':
            url = input(f"  → URL to find related sites: {reset}")
            database.append(f"related:{url}")
            print(f"{BEFORE}{ADD}{AFTER} Added: {green}related:{url}{white}")
    
    if database:
        query = " ".join(database)
        print(f"\n{BEFORE}{INFO}{AFTER} Final query: {green}{query}{white}")
        print(f"{BEFORE}{INFO}{AFTER} Opening browser...")
        webbrowser.open("https://www.google.com/search?q=" + query.replace(" ", "%20"))
    else:
        print(f"{BEFORE}{ERROR}{AFTER} No operators selected")
    
    input(f"\n{BEFORE}END{AFTER} Press Enter...")

# ==========================================
# MAIN MENU
# ==========================================
def main():
    while True:
        clear()
        banner()
        
        print(f"""
    {white}Available Tools:{reset}
    
    [{red}01{white}] {green}Full Security Scan{white}
        ├─ Port scanning with service detection
        ├─ SSL/TLS certificate verification
        ├─ Security headers analysis
        ├─ Technology fingerprinting
        ├─ Sensitive files discovery
        ├─ SQL Injection testing
        └─ Comprehensive vulnerability assessment
    
    [{red}02{white}] {green}Google Dorking Tool{white}
        └─ Advanced search query builder with 7+ operators
    
    [{red}00{white}] Exit
    
        """)
        
        choice = input(f"{red}[SELECT]{white} Choose option -> {reset}")
        
        if choice in ['1', '01']:
            run_scan_all()
        elif choice in ['2', '02']:
            run_dorking()
        elif choice in ['0', '00']:
            print(f"\n{green}[✓] Thanks for using Villager Tool - Stay Ethical!{reset}\n")
            break

if __name__ == "__main__":
    main()