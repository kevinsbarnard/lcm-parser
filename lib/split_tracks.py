from hashlib import new
from scripts.extract_tracks import Track


def split_track(t: Track) -> Track:
    # Find maximum time difference between events
    max_diff_idx = max([((t.events[idx].timestamp - t.events[idx-1].timestamp).total_seconds(), idx) for idx in range(1, len(t.events))])[1]
    
    # Split the track at the maximum time difference
    new_track = Track(
        id=t.id,
        class_name='',
        events=t.events[max_diff_idx:]
    )
    
    # Truncat the track at the maximum time difference
    t.events = t.events[:max_diff_idx]
    
    return new_track