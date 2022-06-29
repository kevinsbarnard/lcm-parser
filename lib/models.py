from dataclasses import dataclass
from datetime import datetime, timedelta, tzinfo
from typing import List, Optional

from dataclasses_json import dataclass_json
from timesignal import EventOrchestra, EventSignal


@dataclass_json
@dataclass
class AuxDataState:
    """
    BOX_STEREO_TRACK AuxData vehicle-frame target state.
    
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
    """
    BOX_STEREO_TRACK auxiliary data event.
    """
    track_id: str
    state: AuxDataState
    association_score: float
    iou: float
    pixel_error: float


@dataclass_json
@dataclass
class Box:
    """
    Floating-point 2D bounding box.
    """
    x: float
    y: float
    width: float
    height: float


@dataclass_json
@dataclass
class TrackEvent:
    """
    Track event derived from a BOX_STEREO_TRACK event.
    """
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
    """
    Track, derived from a series of BOX_STEREO_TRACK events.
    """
    id: int
    class_name: str
    events: List[TrackEvent]
    
    @property
    def unique_points(self) -> set:
        """
        Set of unique (x, y, z) points in the track.
        """
        return set((ev.x_mm, ev.y_mm, ev.z_mm) for ev in self.events)
    
    @property
    def sorted_events(self) -> List[TrackEvent]:
        """
        List of events, sorted by timestamp.
        """
        return sorted(self.events, key=lambda e: e.timestamp)
    
    @property
    def start_timestamp(self) -> datetime:
        """
        First timestamp in the track, as a datetime.
        """
        return self.sorted_events[0].timestamp
    
    @property
    def end_timestamp(self) -> datetime:
        """
        Last timestamp in the track, as a datetime.
        """
        return self.sorted_events[-1].timestamp
    
    @property
    def duration(self) -> timedelta:
        """
        Track duration, as a timedelta.
        """
        return self.end_timestamp - self.start_timestamp
    
    def to_event_orchestra(self) -> EventOrchestra:
        """
        Convert to a flat event orchestra object (timesignal.EventOrchestra).
        """
        timestamps = [ev.timestamp for ev in self.events]
        
        attrs = (
            'x_mm',
            'y_mm',
            'z_mm',
            'width_mm',
            'height_mm',
            'score',
            'association_score',
            'iou',
            'pixel_error',
        )
        
        signals = {
            attr: EventSignal(
                zip(
                    timestamps,
                    (getattr(ev, attr) for ev in self.events for attr in attrs)
                ),
                interpolation='nearest'
            )
            for attr in attrs
        }
        
        return EventOrchestra(signals)


@dataclass_json
@dataclass
class ParsedEventMeta:
    """
    Metadata for parsed event.
    """
    channel: str
    event_number: int
    timestamp: int  # microseconds since epoch
    
    def get_datetime(self, tz: Optional[tzinfo] = None) -> datetime:
        return datetime.fromtimestamp(self.timestamp / 1e6, tz=tz)


@dataclass_json
@dataclass
class ParsedEvent:
    """
    Event parsed from an LCM log. Contains metadata and event data as a dict.
    """
    meta: ParsedEventMeta
    event: dict  # JSON-parsed event
