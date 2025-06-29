import os
import json
from typing import List, Dict
from datetime import datetime

class TrackInfoGetter:
    def __init__(self, exclude_tracks: List[str] = [], track_dir: str = "./save/trackfile"):
        self.track_dir = track_dir
        self.tracks_info: List[Dict] = []
        self.exclude_tracks = exclude_tracks
        self.info_collected = False #Lazy Recollection

    def read_chart_metadata(self, chart_name: str) -> Dict:
        metadata = {
            "file_name": chart_name,
        }
        
        file_path = os.path.join(self.track_dir, chart_name, chart_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                metadata["title"] = data.get("title", "")
                metadata["artist"] = data.get("artist", "")
                metadata["bpm"] = str(data.get("bpm", ""))
                metadata["chart_maker"] = data.get("chart_maker", "")
                metadata["duration"] = str(data.get("duration_ms", ""))
                metadata['level'] = data.get("level", "0?")
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")
            
        return metadata

    def collect_tracks_info(self) -> None:
        if not os.path.exists(self.track_dir):
            print(f"Directory {self.track_dir} not found!")
            return

        for dir_name in [f for f in os.listdir(self.track_dir) if (os.path.isdir(os.path.join(self.track_dir, f)) and (f not in self.exclude_tracks))]:
            track_info = self.read_chart_metadata(dir_name)
            self.tracks_info.append(track_info)
        
        self.info_collected = True

    def save_to_json(self, output_file: str = "tracks_info.json") -> None:
        data_dir = "./save"
        output_data = {
            "tracks": self.tracks_info,
            "cache_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(os.path.join(data_dir,output_file), 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
    
    def dump(self, force_recheck = False) -> None:
        if force_recheck or (not self.info_collected):
            self.collect_tracks_info()
        self.save_to_json()
    
    def get_tracks(self, force_recheck) -> List[Dict]:
        if force_recheck or (not self.info_collected):
            self.collect_tracks_info()
        return self.tracks_info

def main():
    getter = TrackInfoGetter(exclude_tracks=["demo"])
    getter.dump()

if __name__ == "__main__":
    main()