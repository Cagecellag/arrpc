import json
import urllib.request
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_JSON = os.path.join(SCRIPT_DIR, "detectable.json")
DETECTABLES_URL = "https://discord.com/api/v8/applications/detectable"

ADDITIONS = {
    "Changed Special": "changed special/game.exe",
    "Class of '09": "class_of_09.exe",
    "Class of '09: The Re-Up": "c09ru.exe",
    "Class of '09: The Flip Side": "c09fs.exe",
    "Minecraft: Story Mode": "minecraftstorymode.exe",
    "Minecraft: Story Mode - Season Two": "minecraft2.exe",
    "shapez 2": "shapez 2.exe",
    "Untitled Goose Game": "untitled.exe",
    "Viewfinder": "viewfinder.exe",
    "Windowkill": "windowkill-vulkan.exe",
    "Hollow Knight: Silksong": "hollow knight silksong.exe",
    "Hollow Knight": "Hollow Knight/hollow_knight.exe",
}

try:
    req = urllib.request.Request(
        DETECTABLES_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(req) as response:
        data = json.load(response)
    
    print(f"Fetched {len(data)} items from Discord API")
    
    added_count = 0
    not_found = []
    
    for game_name, exe_name in ADDITIONS.items():
        found = False
        for item in data:
            if item.get("name") == game_name:
                found = True
                # Initialize executables list if it doesn't exist
                if "executables" not in item:
                    item["executables"] = []
                
                # Create the new executable entry
                new_exec = {
                    "is_launcher": False,
                    "name": exe_name,
                    "os": "win32"
                }
                
                # Check if this exact executable already exists
                already_exists = any(
                    e.get("name") == exe_name and e.get("os") == "win32" 
                    for e in item["executables"]
                )
                
                if not already_exists:
                    item["executables"].append(new_exec)
                    added_count += 1
                    print(f"[+] Added '{exe_name}' to '{game_name}'")
                else:
                    print(f"    '{exe_name}' already exists in '{game_name}'")
                break
        
        if not found:
            not_found.append(game_name)
            print(f"[-] '{game_name}' not found in API")
    
    # Save the updated data
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSummary:")
    print(f"  Added: {added_count} executables")
    print(f"  Not found: {len(not_found)} games")
    print(f"  Output saved to: {OUTPUT_JSON}")
    
    if not_found:
        print(f"\nGames not found in API:")
        for game in not_found:
            print(f"    - {game}")

except urllib.error.URLError as e:
    print(f"Error fetching from API: {e}")
    print("Make sure you have internet connection and the API URL is correct.")
except json.JSONDecodeError as e:
    print(f"Error parsing JSON response: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

