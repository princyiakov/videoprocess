import os
import math
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import imageio
from skimage.metrics import structural_similarity as ssim


def _sort_indx(start_frame, m_d_idx):
    """
    Sort the index of the frames
    """
    ordered_idx = [start_frame]  # Starting frame to be considered for sorting

    while len(ordered_idx) != m_d_idx.shape[0]:
        for e in m_d_idx[ordered_idx[-1]]:  # from m_d_idx consider the last array in ordered_idx
            if e not in ordered_idx:
                ordered_idx.append(e) # Append only if the value is not present in ordered_idx
                break

    return ordered_idx


class VidRectifier:
    def __init__(self, in_file, out_file, verbose=True):
        self.in_file = in_file
        self.out_file = out_file
        self.verbose = verbose
        self.basename = os.path.splitext(out_file)[0]
        self.frames = []
        self.good_frames = []
        self.width = 0
        self.height = 0

    def __read_video_file(self):
        """
        Reads the declared input video file
        Return: a list with the ordered video frames index value
        """
        cap = cv2.VideoCapture(self.in_file)
        self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Width of the frame
        self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Height of the frame

        vid_frames = []
        while True:
            ret, frame = cap.read()  # Read the frames of the video
            if not ret:
                break
            vid_frames.append(frame)

        assert len(vid_frames) > 0, "No frames found: Please check the path of the input file"
        return vid_frames

    def __write_video_file(self, frames, fps=30):
        """
        Write a video file
        Args:
            frames: Frames to write
            fps: Frames per second
        """
        res = (self.width, self.height)
        out = cv2.VideoWriter(self.out_file,
                              cv2.VideoWriter_fourcc(*'XVID'),
                              fps,
                              res)

        for f in frames:
            out.write(f)

        out.release()

    def __save_sample(self, frames, file, grid_pad=5, resize=(128, 128)):
        """
        Write a grid of images
        Args:
            frames: Frames to be saved
            file: Output file name
            grid_pad: Pixels between samples
            resize: Size of the images in the grid
        """
        # Create a array of frames to be saved
        samples = np.array(
            [cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2RGB), resize) for f in frames])

        if len(samples.shape) < 4:
            samples = np.expand_dims(samples, 4)

        img_height = int(samples.shape[1])
        img_width = int(samples.shape[2])
        nb_channels = int(samples.shape[3])

        grid_size = (
            int(math.ceil(np.sqrt(samples.shape[0]))), int(math.ceil(np.sqrt(samples.shape[0]))))
        if self.verbose:
            print(grid_size)
        samples = samples.reshape(samples.shape[0], img_height, img_width, nb_channels)

        grid_h = img_height * grid_size[0] + grid_pad * (grid_size[0] - 1)
        grid_w = img_width * grid_size[1] + grid_pad * (grid_size[1] - 1)
        img_grid = np.zeros((grid_h, grid_w, nb_channels), dtype=np.uint8)

        for i, res in enumerate(samples):
            if i >= grid_size[0] * grid_size[1]:
                break
            row = (i // grid_size[0]) * (img_height + grid_pad)
            col = (i % grid_size[1]) * (img_width + grid_pad)
            img_grid[row:row + img_height, col:col + img_width, :] = res

        imageio.imwrite(file, np.squeeze(img_grid))

    def __extract_outliers(self):
        """
        Extract outliers based on density based clustering
        """
        self.frames = self.__read_video_file()

        # Flatten the image
        flat_reduced = [cv2.resize(f, (128, 128)).flatten() for f in self.frames]

        # DBSCAN - Density-Based Spatial Clustering from features
        db = DBSCAN(eps=13000, min_samples=2)
        cl = db.fit(flat_reduced)

        # Cluster labels. Noisy samples are given the label -1
        n_cluster = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
        assert n_cluster == 1, "Only one cluster should exist"

        self.good_frames = np.array(self.frames)[cl.labels_ == 0]

        # Save the outliers frames as a grid
        self.__save_sample(np.array(self.frames)[cl.labels_ == -1], self.basename + "_outliers.png")

        # Save the good frames as a grid
        self.__save_sample(self.good_frames, self.basename + "_good_frames.png")

    def __smoothness(self, order, dist_m, stats=False):
        vals = []
        for i, j in zip(order, order[1:]):
            vals.append(dist_m[i, j])

        d_vals = []
        for i, j in zip(vals, vals[1:]):
            d_vals.append(abs(i - j))

        if stats:
            if self.verbose:
                print("mean ", np.mean(vals))
                print("median", np.median(vals))
                print("max, min ", max(vals), min(vals))

            x_pos = [i for i, _ in enumerate(vals)]
            plt.bar(x_pos, vals)
            plt.show()

        return sum(d_vals)

    def rectify_vid_seq(self):
        """
        Function to rectify the sequence of the video
        """

        # Extract the outliers(images that don't belong to the original) from the video
        self.__extract_outliers()

        # Initialise m_d_ssim
        m_d_ssim = np.zeros((len(self.good_frames), len(self.good_frames)), dtype=float)

        # Resize and convert to grayscale the good frames(belonging to original video)
        f_r = [cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (256, 256)) for f in
               self.good_frames]

        # m_d_ssim builds a matrix of structural similarity of the good_frames list
        for i, f1 in enumerate(f_r):
            for j, f2 in enumerate(f_r):
                m_d_ssim[i, j] = ssim(f1, f2, multichannel=False)
            if self.verbose:
                print(f"step {i + 1}/{len(f_r)}")

        # Distance ssim is equal to 1 for identical images and -1 for distant images
        # m_d_s_idx provides sorted index matrix representing the image index with max similarity
        m_d_s_idx = np.argsort(-m_d_ssim, axis=1)

        vals = []
        for s in range(m_d_s_idx.shape[0]):
            ordered_idx = _sort_indx(s, m_d_s_idx)

            d = self.__smoothness(ordered_idx, -m_d_ssim)
            vals.append((s, d))

        starts = sorted(vals, key=lambda x: x[1])
        best_start = starts[0][0]
        worst_start = starts[-1][0]

        ordered_idx = _sort_indx(best_start, m_d_s_idx)

        self.__save_sample(np.array(self.good_frames)[ordered_idx], self.basename
                           + "_good_order.png")

        best_order = _sort_indx(best_start, m_d_s_idx)
        self.__smoothness(best_order, m_d_ssim, True)

        worst_order = _sort_indx(worst_start, m_d_s_idx)
        self.__smoothness(worst_order, m_d_ssim, True)

        self.__write_video_file(self.good_frames[ordered_idx])
