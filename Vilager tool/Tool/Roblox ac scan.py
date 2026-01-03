import sys
import requests
import time
import json
from datetime import datetime
from collections import Counter

# ANSI Colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def print_banner():
    print(f"""{Colors.RED}{Colors.BOLD}
    ╔══════════════════════════════════════════════╗
    ║           ROBLOX USER SCANNER V5             ║
    ╚══════════════════════════════════════════════╝{Colors.RESET}""")

def loading_animation(text="Loading", dots=3):
    for i in range(dots):
        sys.stdout.write(f"\r{Colors.CYAN}{text}{'.' * (i + 1)}   {Colors.RESET}")
        sys.stdout.flush()
        time.sleep(0.3)
    sys.stdout.write(f"\r{Colors.GREEN}✓ {text} - Complete!{Colors.RESET}\n")

def section_header(title):
    print(f"\n{Colors.YELLOW}{'='*70}{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BOLD}{title.center(70)}{Colors.RESET}")
    print(f"{Colors.YELLOW}{'='*70}{Colors.RESET}\n")

# ======================== ULTRA DETAILED USER SCANNER ========================
def ultra_scan_user(user_id):
    all_data = {}
    
    try:
        # === 1. INFORMATIONS DE BASE ===
        loading_animation("Fetching basic user info")
        user_info = requests.get(f"https://users.roblox.com/v1/users/{user_id}").json()
        if "errors" in user_info:
            print(f"{Colors.RED}[!] User not found.{Colors.RESET}")
            return None
        
        all_data['basic_info'] = user_info
        
        section_header("👤 BASIC USER INFORMATION")
        print(f"{Colors.CYAN}Username         :{Colors.WHITE} {user_info.get('name')}{Colors.RESET}")
        print(f"{Colors.CYAN}Display Name     :{Colors.WHITE} {user_info.get('displayName')}{Colors.RESET}")
        print(f"{Colors.CYAN}User ID          :{Colors.WHITE} {user_id}{Colors.RESET}")
        print(f"{Colors.CYAN}Description      :{Colors.WHITE} {user_info.get('description') or 'None'}{Colors.RESET}")
        print(f"{Colors.CYAN}Created Date     :{Colors.WHITE} {user_info.get('created')}{Colors.RESET}")
        print(f"{Colors.CYAN}Account Banned   :{Colors.RED if user_info.get('isBanned') else Colors.GREEN} {'YES' if user_info.get('isBanned') else 'NO'}{Colors.RESET}")
        print(f"{Colors.CYAN}Profile Link     :{Colors.BLUE} https://www.roblox.com/users/{user_id}/profile{Colors.RESET}")
        
        # === 2. PRESENCE STATUS ===
        loading_animation("Checking online status")
        try:
            presence_res = requests.post("https://presence.roblox.com/v1/presence/users",
                                        json={"userIds": [int(user_id)]})
            presence_data = presence_res.json()
            if presence_data.get('userPresences'):
                presence = presence_data['userPresences'][0]
                status_map = {0: "Offline", 1: "Online", 2: "In Game", 3: "In Studio"}
                status = status_map.get(presence.get('userPresenceType', 0), "Unknown")
                last_location = presence.get('lastLocation', 'Unknown')
                last_online = presence.get('lastOnline', 'Unknown')
                
                all_data['presence'] = presence
                
                print(f"\n{Colors.MAGENTA}[ONLINE STATUS]{Colors.RESET}")
                status_color = Colors.GREEN if status == "Online" else Colors.YELLOW if "Game" in status else Colors.RED
                print(f"{Colors.CYAN}Status           :{status_color} {status}{Colors.RESET}")
                print(f"{Colors.CYAN}Last Location    :{Colors.WHITE} {last_location}{Colors.RESET}")
                print(f"{Colors.CYAN}Last Online      :{Colors.WHITE} {last_online}{Colors.RESET}")
        except:
            pass
        
        # === 3. USERNAME HISTORY ===
        loading_animation("Fetching username history")
        try:
            username_history = []
            cursor = ""
            while len(username_history) < 50:  # Limite à 50 anciens noms
                url = f"https://users.roblox.com/v1/users/{user_id}/username-history?limit=100"
                if cursor:
                    url += f"&cursor={cursor}"
                history_res = requests.get(url).json()
                data = history_res.get('data', [])
                if not data:
                    break
                username_history.extend(data)
                cursor = history_res.get('nextPageCursor')
                if not cursor:
                    break
            
            if username_history:
                all_data['username_history'] = username_history
                section_header("📝 USERNAME HISTORY")
                print(f"{Colors.CYAN}Total Past Names : {len(username_history)}{Colors.RESET}\n")
                for i, entry in enumerate(username_history[:10], 1):  # Afficher les 10 derniers
                    print(f" {i}. {Colors.WHITE}{entry['name']:<25}{Colors.RESET} (Changed: {Colors.DIM}{entry['created']}{Colors.RESET})")
                if len(username_history) > 10:
                    print(f"\n{Colors.DIM}... and {len(username_history) - 10} more{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Username history unavailable{Colors.RESET}")
        
        # === 4. SOCIAL STATS ===
        loading_animation("Fetching social statistics")
        try:
            friends_res = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/friends").json()
            friends_count = len(friends_res.get('data', []))
            
            followers_res = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count").json()
            followers_count = followers_res.get('count', 0)
            
            following_res = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followings/count").json()
            following_count = following_res.get('count', 0)
            
            all_data['social'] = {
                'friends': friends_count,
                'followers': followers_count,
                'following': following_count
            }
            
            section_header("👥 SOCIAL STATISTICS")
            print(f"{Colors.CYAN}Friends          :{Colors.WHITE} {friends_count:,}{Colors.RESET}")
            print(f"{Colors.CYAN}Followers        :{Colors.WHITE} {followers_count:,}{Colors.RESET}")
            print(f"{Colors.CYAN}Following        :{Colors.WHITE} {following_count:,}{Colors.RESET}")
            print(f"{Colors.CYAN}Follower/Friend  :{Colors.WHITE} {followers_count / max(friends_count, 1):.2f}x{Colors.RESET}")
        except:
            pass
        
        # === 5. GROUPS INFORMATION ===
        loading_animation("Analyzing groups")
        try:
            groups_res = requests.get(f"https://groups.roblox.com/v1/users/{user_id}/groups/roles").json()
            groups_list = groups_res.get('data', [])
            all_data['groups'] = groups_list
            
            section_header("🏢 GROUPS MEMBERSHIP")
            print(f"{Colors.CYAN}Total Groups     : {len(groups_list)}{Colors.RESET}\n")
            
            if groups_list:
                print(f"{Colors.CYAN}{'Group Name':<40} | {'Role':<20} | Members{Colors.RESET}")
                print(f"{Colors.DIM}{'-'*80}{Colors.RESET}")
                for g in groups_list[:15]:  # Afficher 15 premiers groupes
                    group_name = g['group']['name'][:40]
                    role_name = g['role']['name'][:20]
                    members = g['group'].get('memberCount', 'N/A')
                    print(f" {Colors.WHITE}{group_name:<40}{Colors.RESET} | {Colors.YELLOW}{role_name:<20}{Colors.RESET} | {Colors.CYAN}{members:,}{Colors.RESET}")
                
                if len(groups_list) > 15:
                    print(f"\n{Colors.DIM}... and {len(groups_list) - 15} more groups{Colors.RESET}")
        except:
            pass
        
        # === 6. BADGES ===
        loading_animation("Collecting badges")
        try:
            all_badges = []
            cursor = ""
            while len(all_badges) < 100:  # Limite à 100 badges
                url = f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=100"
                if cursor:
                    url += f"&cursor={cursor}"
                badges_res = requests.get(url).json()
                data = badges_res.get('data', [])
                if not data:
                    break
                all_badges.extend(data)
                cursor = badges_res.get('nextPageCursor')
                if not cursor:
                    break
            
            if all_badges:
                all_data['badges'] = all_badges
                section_header("🏆 BADGES EARNED")
                print(f"{Colors.CYAN}Total Badges     : {len(all_badges)}{Colors.RESET}\n")
                
                # Grouper par jeu
                games_badges = {}
                for badge in all_badges:
                    game_id = badge.get('awardingUniverse', {}).get('id', 'Unknown')
                    if game_id not in games_badges:
                        games_badges[game_id] = []
                    games_badges[game_id].append(badge)
                
                print(f"{Colors.CYAN}Badges from {len(games_badges)} different games{Colors.RESET}\n")
                
                # Afficher les 10 premiers badges
                print(f"{Colors.CYAN}Recent Badges:{Colors.RESET}")
                for badge in all_badges[:10]:
                    print(f" • {Colors.WHITE}{badge['name']:<40}{Colors.RESET} {Colors.DIM}(Earned: {badge.get('created', 'Unknown')}){Colors.RESET}")
                
                if len(all_badges) > 10:
                    print(f"\n{Colors.DIM}... and {len(all_badges) - 10} more badges{Colors.RESET}")
        except:
            pass
        
        # === 7. GAME PASSES ===
        loading_animation("Checking game passes")
        try:
            # Note: L'API des game passes nécessite de connaître les IDs des jeux
            # On peut les obtenir via les favoris ou les badges
            pass
        except:
            pass
        
        # === 8. FAVORITE GAMES ===
        loading_animation("Fetching favorite games")
        try:
            favorites_res = requests.get(f"https://games.roblox.com/v2/users/{user_id}/favorite/games").json()
            favorites = favorites_res.get('data', [])
            
            if favorites:
                all_data['favorite_games'] = favorites
                section_header("⭐ FAVORITE GAMES")
                print(f"{Colors.CYAN}Total Favorites  : {len(favorites)}{Colors.RESET}\n")
                
                print(f"{Colors.CYAN}{'Game Name':<45} | Players{Colors.RESET}")
                print(f"{Colors.DIM}{'-'*60}{Colors.RESET}")
                for game in favorites[:10]:
                    game_name = game['name'][:45]
                    playing = game.get('playing', 0)
                    print(f" {Colors.WHITE}{game_name:<45}{Colors.RESET} | {Colors.GREEN}{playing:,}{Colors.RESET}")
        except:
            pass
        
        # === 9. CREATED GAMES ===
        loading_animation("Finding created games")
        try:
            # Recherche des jeux créés par l'utilisateur
            creator_res = requests.get(f"https://games.roblox.com/v2/users/{user_id}/games?limit=50").json()
            created_games = creator_res.get('data', [])
            
            if created_games:
                all_data['created_games'] = created_games
                section_header("🎮 CREATED GAMES")
                print(f"{Colors.CYAN}Total Games      : {len(created_games)}{Colors.RESET}\n")
                
                print(f"{Colors.CYAN}{'Game Name':<40} | {'Visits':<12} | Active{Colors.RESET}")
                print(f"{Colors.DIM}{'-'*70}{Colors.RESET}")
                for game in created_games[:10]:
                    game_name = game['name'][:40]
                    visits = game.get('visits', 0)
                    playing = game.get('playing', 0)
                    print(f" {Colors.WHITE}{game_name:<40}{Colors.RESET} | {Colors.YELLOW}{visits:>12,}{Colors.RESET} | {Colors.GREEN}{playing:>5,}{Colors.RESET}")
        except:
            pass
        
        # === 10. INVENTORY (Limiteds & Collectibles) ===
        loading_animation("Scanning inventory")
        try:
            # Collecter les assets de l'inventaire
            asset_types = {
                8: "Hats",
                41: "Hair Accessories", 
                42: "Face Accessories",
                43: "Neck Accessories",
                44: "Shoulder Accessories",
                45: "Front Accessories",
                46: "Back Accessories",
                47: "Waist Accessories"
            }
            
            total_items = 0
            inventory_summary = {}
            
            for asset_type, name in asset_types.items():
                try:
                    inv_res = requests.get(
                        f"https://inventory.roblox.com/v1/users/{user_id}/assets/collectibles?limit=100&assetType={asset_type}"
                    ).json()
                    items = inv_res.get('data', [])
                    if items:
                        inventory_summary[name] = len(items)
                        total_items += len(items)
                except:
                    continue
            
            if inventory_summary:
                all_data['inventory'] = inventory_summary
                section_header("🎒 INVENTORY (Collectibles)")
                print(f"{Colors.CYAN}Total Items      : {total_items}{Colors.RESET}\n")
                for item_type, count in inventory_summary.items():
                    print(f" • {Colors.WHITE}{item_type:<25}{Colors.RESET} : {Colors.YELLOW}{count}{Colors.RESET}")
        except:
            pass
        
        # === 11. FRIENDS ANALYSIS ===
        loading_animation("Deep analyzing friends network")
        try:
            friends_data = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/friends").json()
            friends_list = friends_data.get('data', [])
            
            if friends_list:
                # Récupérer les détails des amis
                friend_ids = [f['id'] for f in friends_list]
                friends_details = {}
                
                for i in range(0, len(friend_ids), 100):
                    batch = friend_ids[i:i+100]
                    users_res = requests.post("https://users.roblox.com/v1/users", 
                                            json={"userIds": batch, "excludeBannedUsers": False})
                    for user in users_res.json().get('data', []):
                        friends_details[user['id']] = user
                
                # Statut des amis
                online_count = 0
                in_game_count = 0
                
                for i in range(0, len(friend_ids), 50):
                    batch = friend_ids[i:i+50]
                    try:
                        presence_res = requests.post("https://presence.roblox.com/v1/presence/users",
                                                    json={"userIds": batch})
                        for p in presence_res.json().get('userPresences', []):
                            status = p.get('userPresenceType', 0)
                            if status == 1:
                                online_count += 1
                            elif status == 2:
                                in_game_count += 1
                    except:
                        pass
                
                all_data['friends_analysis'] = {
                    'total': len(friends_list),
                    'online': online_count,
                    'in_game': in_game_count,
                    'offline': len(friends_list) - online_count - in_game_count
                }
                
                section_header("🤝 FRIENDS NETWORK ANALYSIS")
                print(f"{Colors.CYAN}Total Friends    : {len(friends_list)}{Colors.RESET}")
                print(f"{Colors.GREEN}Currently Online : {online_count}{Colors.RESET}")
                print(f"{Colors.YELLOW}Playing Games    : {in_game_count}{Colors.RESET}")
                print(f"{Colors.RED}Offline          : {len(friends_list) - online_count - in_game_count}{Colors.RESET}")
                
                # Demander si on veut voir la liste complète
                show_friends = input(f"\n{Colors.YELLOW}[?] Display full friends list? (y/n) -> {Colors.WHITE}")
                if show_friends.lower() == 'y':
                    print(f"\n{Colors.CYAN}{'Username':<30} | {'User ID':<15} | Status{Colors.RESET}")
                    print(f"{Colors.DIM}{'-'*70}{Colors.RESET}")
                    
                    # Récupérer le statut de chaque ami
                    friends_status = {}
                    for i in range(0, len(friend_ids), 50):
                        batch = friend_ids[i:i+50]
                        try:
                            presence_res = requests.post("https://presence.roblox.com/v1/presence/users",
                                                        json={"userIds": batch})
                            status_map = {0: "Offline", 1: "Online", 2: "In Game", 3: "In Studio"}
                            for p in presence_res.json().get('userPresences', []):
                                friends_status[p['userId']] = status_map.get(p.get('userPresenceType', 0), "Unknown")
                        except:
                            pass
                    
                    for friend in friends_list[:50]:  # Afficher 50 premiers
                        friend_id = friend['id']
                        username = friends_details.get(friend_id, {}).get('name', 'Unknown')
                        status = friends_status.get(friend_id, "Unknown")
                        status_color = Colors.GREEN if status == "Online" else Colors.YELLOW if "Game" in status else Colors.RED
                        print(f" {Colors.WHITE}{username:<30}{Colors.RESET} | {Colors.YELLOW}{friend_id:<15}{Colors.RESET} | {status_color}{status}{Colors.RESET}")
        except:
            pass
        
        # === 12. ACCOUNT AGE & STATISTICS ===
        section_header("📊 ACCOUNT STATISTICS")
        try:
            created_date = datetime.strptime(user_info['created'], "%Y-%m-%dT%H:%M:%S.%fZ")
            account_age_days = (datetime.now() - created_date).days
            account_age_years = account_age_days / 365.25
            
            print(f"{Colors.CYAN}Account Age      :{Colors.WHITE} {account_age_days:,} days ({account_age_years:.2f} years){Colors.RESET}")
            print(f"{Colors.CYAN}Friends/Day      :{Colors.WHITE} {all_data.get('social', {}).get('friends', 0) / max(account_age_days, 1):.2f}{Colors.RESET}")
            
            if 'badges' in all_data:
                print(f"{Colors.CYAN}Badges/Year      :{Colors.WHITE} {len(all_data['badges']) / max(account_age_years, 1):.2f}{Colors.RESET}")
        except:
            pass
        
        # === EXPORT OPTION ===
        print(f"\n{Colors.MAGENTA}{'='*70}{Colors.RESET}")
        export_choice = input(f"{Colors.YELLOW}[?] Export all data to JSON file? (y/n) -> {Colors.WHITE}")
        if export_choice.lower() == 'y':
            export_full_data(all_data, user_id, user_info.get('name'))
        
        print(f"\n{Colors.GREEN}{'='*70}")
        print(f"{Colors.GREEN}{Colors.BOLD}✓ SCAN COMPLETE - All available public data collected!{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*70}{Colors.RESET}\n")
        
        return all_data
        
    except Exception as e:
        print(f"{Colors.RED}[ERROR] {e}{Colors.RESET}")
        return None

# ======================== EXPORT FUNCTION ========================
def export_full_data(data, user_id, username):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"roblox_scan_{username}_{user_id}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"{Colors.GREEN}✓ Full data exported to: {filename}{Colors.RESET}")
        print(f"{Colors.CYAN}File size: {len(json.dumps(data)) / 1024:.2f} KB{Colors.RESET}")
        
    except Exception as e:
        print(f"{Colors.RED}[ERROR] Export failed: {e}{Colors.RESET}")

# ======================== SEARCH FUNCTIONS ========================
def search_by_name():
    print(f"\n{Colors.YELLOW}Enter Username:{Colors.RESET}")
    name = input(">> ").strip()
    try:
        res = requests.post("https://users.roblox.com/v1/usernames/users", 
                            json={"usernames": [name], "excludeBannedUsers": False})
        data = res.json()
        if data.get('data') and len(data['data']) > 0:
            u_id = data['data'][0]['id']
            print(f"\n{Colors.GREEN}✓ User found! ID: {u_id}{Colors.RESET}")
            time.sleep(1)
            ultra_scan_user(u_id)
        else:
            print(f"{Colors.RED}[!] User '{name}' not found.{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[!] Error: {e}{Colors.RESET}")

def search_by_id():
    print(f"\n{Colors.YELLOW}Enter User ID:{Colors.RESET}")
    u_id = input(">> ").strip()
    if u_id.isdigit():
        ultra_scan_user(u_id)
    else:
        print(f"{Colors.RED}[!] ID must be numeric.{Colors.RESET}")

# ======================== MAIN MENU ========================
def main():
    while True:
        print_banner()
        print(f"\n{Colors.CYAN}Advanced user information scanner{Colors.RESET}\n")
        
        print(f"{Colors.GREEN}[1]{Colors.RESET} Scan by Username")
        print(f"{Colors.GREEN}[2]{Colors.RESET} Scan by User ID")
        print(f"{Colors.RED}[0]{Colors.RESET} Exit")
        
        choice = input(f"\n{Colors.YELLOW}Choice -> {Colors.WHITE}")
        
        if choice == '1': 
            search_by_name()
        elif choice == '2': 
            search_by_id()
        elif choice == '0': 
            print(f"\n{Colors.GREEN}Thanks for using Roblox User Scanner!{Colors.RESET}\n")
            break
        else:
            print(f"{Colors.RED}Invalid choice.{Colors.RESET}")
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

if __name__ == "__main__":
    main()