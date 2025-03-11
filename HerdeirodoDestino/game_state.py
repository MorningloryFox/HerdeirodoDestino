import json
import os
from datetime import datetime

class GameState:
    def __init__(self):
        self.saves_dir = "saves"
        self.ensure_saves_directory()
        
    def ensure_saves_directory(self):
        """Ensure the saves directory exists"""
        if not os.path.exists(self.saves_dir):
            os.makedirs(self.saves_dir)
            
    def save_game(self, chapter, scene_index, description=""):
        """Save current game state"""
        save_data = {
            "chapter": chapter,
            "scene_index": scene_index,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "description": description
        }
        
        # Create filename with timestamp
        filename = f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.saves_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=4)
            
        return filepath
        
    def load_game(self, filepath):
        """Load game state from file"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading save file: {e}")
            return None
            
    def get_save_files(self):
        """Get list of all save files"""
        self.ensure_saves_directory()
        saves = []
        
        for filename in os.listdir(self.saves_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(self.saves_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        save_data = json.load(f)
                        saves.append({
                            "filepath": filepath,
                            "timestamp": save_data["timestamp"],
                            "chapter": save_data["chapter"],
                            "description": save_data["description"]
                        })
                except Exception as e:
                    print(f"Error reading save file {filename}: {e}")
                    
        return sorted(saves, key=lambda x: x["timestamp"], reverse=True)
