# frame_grabber.py (lcm-parser)
import argparse
import os
import time

import cv2


def ns_epoch():
    return int(time.time() * 1e9)


def capture_frame(cap: cv2.VideoCapture, root_dir: str):
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('{}/{}.png'.format(root_dir, ns_epoch()), frame)
        return True
    return False


def main(root_dir: str, n: int):
    assert os.path.isdir(root_dir)
    cap = cv2.VideoCapture(0)
    for _ in range(n):
        if not capture_frame(cap, root_dir):
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=str, help='Root directory to store images')
    parser.add_argument('n', type=int, help='Number of frames to capture')
    args = parser.parse_args()
    main(args.dir, args.n)
