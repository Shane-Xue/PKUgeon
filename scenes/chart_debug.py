import os
import json
from typing import List, Dict

def check_track_timing(track_file_path: str, min_delta: float = 0.5) -> List[Dict]:
    # List to store timing issues
    timing_issues = []

    try:
        # Read the track file
        with open(track_file_path, 'r') as file:
            track_data = json.load(file)

        # Process the notes directly since they're at the top level
        notes = track_data.get('notes', [])

        # Check consecutive notes
        for i in range(len(notes) - 1):
            current_note = notes[i]
            next_note = notes[i + 1]
            
            current_time = current_note.get('time', 0)
            next_time = next_note.get('time', 0)
            # print(current_time, next_time)
            time_delta = next_time - current_time
            
            if time_delta < min_delta and current_note.get('path', -1) == next_note.get('path', -1):
                issue = {
                'track_index': current_note.get('path', -1),
                'note1_time': current_time / 1000,  # Convert to seconds
                'note2_time': next_time / 1000,     # Convert to seconds
                'delta': time_delta / 1000          # Convert to seconds
                }
                timing_issues.append(issue)

        return timing_issues

    except FileNotFoundError:
        print(f"Error: File not found at {track_file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {track_file_path}")
        return []

def main():
    for f in [f for f in os.listdir("save/trackfile") if os.path.isdir(os.path.join("save/trackfile", f))]:
        print(f)
        track_file_path = os.path.join("save/trackfile", f, f)
        issues = check_track_timing(track_file_path)
        
        if not issues:
            print("No timing issues found!")
        else:
            print("Found timing issues:")
            for issue in issues:
                print(f"Track {issue['track_index']}: Notes at {issue['note1_time']:.2f}s and "
                    f"{issue['note2_time']:.2f}s (delta: {issue['delta']:.3f}s)")

if __name__ == "__main__":
    main()