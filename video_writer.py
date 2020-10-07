# video_writer.py (lcm-parser)
# Write a video from a list of unread frames

import cv2
import numpy as np
import mwt
from lcm_reader import Event

from typing import List


def write_video(filename: str, image_events: List[Event], framerate: int = 10, codec: str = 'mp4v'):
    """
    Write a video from a list of unread image_t events.
    Note: Currently only working with PIXEL_FORMAT_GRAY (see mwt.image_t)
    :param filename: Filename to write video
    :param image_events: Image events list
    :param framerate: Framerate in Hz (default=10)
    :param codec: Codec (default='mp4v')
    :return: None
    """
    if not image_events:  # Ensure at least one frame
        return

    # Read first frame
    first_ev = image_events[0]
    first_ev.read_data()
    first_im = mwt.image_t.decode(first_ev.data)
    h, w = first_im.height, first_im.width
    del first_im
    first_ev.clear_data()

    # Image extractor helper function
    def extract_im(ev: Event) -> np.ndarray:
        ev.read_data()
        im = mwt.image_t.decode(ev.data)
        im_mat = np.frombuffer(im.data, dtype=np.uint8).reshape((h, w))
        del im
        ev.clear_data()
        return im_mat

    # Create generator objects
    image_event_gen = iter(image_events)
    frame_gen = (extract_im(ev) for ev in image_event_gen)

    # Creat video writer object
    fourcc = cv2.VideoWriter_fourcc(*codec)
    writer = cv2.VideoWriter(filename, fourcc, framerate, (w, h), False)

    # Write the video
    for idx, frame in enumerate(frame_gen):
        print('Writing frame {}'.format(idx))
        writer.write(frame)
    print('Done.')

    writer.release()
