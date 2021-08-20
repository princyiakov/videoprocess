import argparse
from videoprocess import VidRectifier, os
import time


def check_path(path, curr_dir):
    """
    Checks if the path is absolute value if not the present working directory is concatenated
    with the path
    """
    if not os.path.isabs(path):
        path = os.path.join(curr_dir, path)

    return path


def main():
    start_time = time.time()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print("Your current working directory is ", current_dir)

    parser = argparse.ArgumentParser(description='Video Rectifier')
    parser.add_argument('--input_file', type=str, required=True,
                        help='location of the video to be rectified')
    parser.add_argument('--output_file', type=str, required=True,
                        help='location to save the video rectified')
    args = parser.parse_args()

    input_file = check_path(args.input_file, current_dir)
    output_file = check_path(args.output_file, current_dir)
    print("Input video path is {} ".format(input_file))
    print("Initiating the rectification process")

    vr = VidRectifier(in_file=input_file, out_file=output_file, verbose=True)
    vr.rectify_vid_seq()
    print("Rectified video has been saved at  {} ".format(output_file))

    print("Time taken to process the video is {}s seconds".format(time.time() - start_time))


if __name__ == '__main__':
    main()
