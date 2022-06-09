from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class AuxDataState:
    """
    Units are all millimeters.
    """
    x: float
    y: float
    z: float
    w: float
    h: float


@dataclass_json
@dataclass
class AuxData:
    track_id: str
    state: AuxDataState
    association_score: float
    iou: float
    pixel_error: float


@dataclass_json
@dataclass
class Box:
    x: float
    y: float
    width: float
    height: float


@dataclass_json
@dataclass
class TrackEvent:
    timestamp: datetime
    
    # Image-space boxes
    box_left: Box
    box_right: Box
    
    # Position in robot frame
    x_mm: float
    y_mm: float
    z_mm: float
    
    # Size in robot frame
    width_mm: float
    height_mm: float
    
    # Track score (-100 to 100)
    score: int
    
    # Box association metadata
    association_score: float
    iou: float
    pixel_error: float


@dataclass_json
@dataclass
class Track:
    id: int
    class_name: str
    events: List[TrackEvent]
    
    @property
    def sorted_events(self) -> List[TrackEvent]:
        return sorted(self.events, key=lambda e: e.timestamp)
    
    @property
    def start_timestamp(self) -> datetime:
        return self.sorted_events[0].timestamp
    
    @property
    def end_timestamp(self) -> datetime:
        return self.sorted_events[-1].timestamp
    
    @property
    def duration(self) -> timedelta:
        return self.end_timestamp - self.start_timestamp