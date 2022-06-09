# video_maker.py (lcm-parser)
import argparse
import glob
import os

import cv2


def write_frames(writer, frame_gen):
    for idx, frame in enumerate(frame_gen):
        print('Writing frame {}'.format(idx))
        writer.write(frame)
    print('Done.')


def main(root_dir: str, filename: str):
    assert os.path.isdir(root_dir)
    frame_filenames = glob.glob('{}/*.png'.format(root_dir))
    frame_filenames.sort(reverse=True)

    assert len(frame_filenames) > 0

    k = 100
    k = min(len(frame_filenames), k)
    first_k_ns = [int(os.path.basename(fname)[:-4]) for fname in frame_filenames[:k]]
    ns_diffs = [first_k_ns[idx + 1] - first_k_ns[idx] for idx in range(k - 1)]
    avg_ns_diff = sum(ns_diffs) / len(ns_diffs)
    avg_fps = round(1e9 / avg_ns_diff)

    first_frame = cv2.imread(frame_filenames[0])
    (h, w) = first_frame.shape[:2]

    frame_gen = (cv2.imread(frame_filename) for frame_filename in frame_filenames)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(filename, fourcc, avg_fps, (w, h), True)

    write_frames(writer, frame_gen)

    writer.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=str, help='Root directory of PNG frames')
    parser.add_argument('filename', type=str, help='Output filename')
    args = parser.parse_args()
    main(args.dir, args.filename)
