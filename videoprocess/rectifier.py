import math
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import imageio
from skimage.metrics import structural_similarity as ssim


class VidRectifier:
    def __init__(self, in_file, out_file, verbose=False):
        self.in_file = in_file
        self.out_file = out_file
        self.verbose = verbose
        self.frames = []
        self.good_frames = []

    def __read_video_file(self):
        """Reads the declared input video file
           Return: a list with the video frames
        """
        cap = cv2.VideoCapture(self.in_file)

        vid_frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            vid_frames.append(frame)

        assert len(vid_frames) > 0, "Empty list, file exists ?"
        return vid_frames

    def __write_video_file(self, fps=30, res=(1280, 480)):
        """Write a video file
        Args:
          frames: frames to write
          fps: video fps
          res: resolution of the video (should match with the frames shape)
        """

        out = cv2.VideoWriter(self.out_file,
                              cv2.VideoWriter_fourcc(*'XVID'),
                              fps,
                              res)

        for f in self.frames:
            out.write(f)

        out.release()

    def __save_sample(self, file, grid_pad=5, resize=(64, 64)):
        """Write a grid of images
        Args:
          samples: list of images
          file: output file
          grid_pad: pixels between samples
          resize: size of the images in the grid
        """

        samples = np.array(
            [cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2RGB), (128, 128)) for f in self.frames])

        if len(samples.shape) < 4:
            samples = np.expand_dims(samples, 4)

        img_height = int(samples.shape[1])
        img_width = int(samples.shape[2])
        nb_channels = int(samples.shape[3])

        grid_size = (
        int(math.ceil(np.sqrt(samples.shape[0]))), int(math.ceil(np.sqrt(samples.shape[0]))))
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
        self.frames = self.__read_video_file()

        flat_reduced = [cv2.resize(f, (128, 128)).flatten() for f in self.frames]
        db = DBSCAN(eps=13000, min_samples=2)
        cl = db.fit(flat_reduced)

        n_cluster = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
        assert n_cluster == 1, "Only one cluster should exist"

        self.good_frames = np.array(self.frames)[cl.labels_ == 0]

        self.__save_sample(np.array(self.frames)[cl.labels_ == -1], "outliers.png")
        self.__save_sample(self.good_frames, "good_frames.png")

    def __sort_indx(self, start_frame, m_d_idx):
        ordered_idx = [start_frame]

        while len(ordered_idx) != m_d_idx.shape[0]:
            for e in m_d_idx[ordered_idx[-1]]:
                if e not in ordered_idx:
                    ordered_idx.append(e)
                    break

        return ordered_idx

    def __smoothness(self, order, dist_m, stats=False):
        vals = []
        for i, j in zip(order, order[1:]):
            vals.append(dist_m[i, j])

        d_vals = []
        for i, j in zip(vals, vals[1:]):
            d_vals.append(abs(i - j))

        if stats:
            print("mean ", np.mean(vals))
            print("median", np.median(vals))
            print("max, min ", max(vals), min(vals))

            x_pos = [i for i, _ in enumerate(vals)]
            plt.bar(x_pos, vals)
            plt.show()

        return sum(d_vals)

    def rectify_vid_seq(self):
        m_d_ssim = np.zeros((len(self.good_frames), len(self.good_frames)), dtype=float)

        f_r = [cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (256, 256)) for f in self.good_frames]

        for i, f1 in enumerate(f_r):
            for j, f2 in enumerate(f_r):
                m_d_ssim[i, j] = ssim(f1, f2, multichannel=False)
            print(f"step {i + 1}/{len(f_r)}")

        m_d_s_idx = np.argsort(-m_d_ssim, axis=1)
        vals = []
        for s in range(m_d_s_idx.shape[0]):
            ordered_idx = self.__sort_indx(s, m_d_s_idx)

            d = self.__smoothness(ordered_idx, -m_d_ssim)
            vals.append((s, d))

        starts = sorted(vals, key=lambda x: x[1])
        best_start = starts[0][0]
        worst_start = starts[-1][0]

        ordered_idx = self.__sort_indx(best_start, m_d_s_idx)

        self.__save_sample(np.array(self.good_frames)[ordered_idx], 'good_order.png')

        best_order = self.__sort_indx(best_start, m_d_s_idx)
        self.__smoothness(best_order, m_d_ssim, True)

        worst_order = self.__sort_indx(worst_start, m_d_s_idx)
        self.__smoothness(worst_order, m_d_ssim, True)

        self.__write_video_file('out.mp4', self.good_frames[ordered_idx])