![Meero Logo](https://github.com/princys-laboratory/videoprocess/blob/main/meero.gif)

--------------------------------------------------------------------------------------------------

This code aims at rectifying corrupted videos particularly where frames are shuffled and contains outlier images which 
are not part of the main video.

<!-- toc -->

- [More About The Project](#more-about-pytorch)
  - [Understanding the Use Case](#understanding-the-use-case)
  - [How did we solve the issue](#how-did-we-solve-the-issue)
     - [What is DBSCAN](#what-is-DBSCAN)
     - [What is SSIM](#what-is-ssim)
     - [How did we sort the frames](#how-did-we-sort-the-frames)
- [Installation](#installation)
  - [Install Package](#install-package)
  - [Docker Image](#docker-image)
    - [Building the image yourself](#building-the-image-yourself)
- [How to run the application](#how-to-run-the-application)
- [Resources](#resources)
<!-- tocstop -->

## More About The Project
Let us understand in detail about the project
| Before | After |
| ---- | --- |
|https://github.com/princys-laboratory/videoprocess/blob/main/Input_file.gif| https://github.com/princys-laboratory/videoprocess/blob/main/Output_file.gif|
### Understanding the Use Case
The goal is to have an installable Python package that could be integrated into the company’s  processing pipelines
or just be used by anyone in the team on their own computer to correct any corrupted videos they might have.

### How did we solve the issue
The images can vary enormously. Thus it is possible that the frames which are not part of the video (outliers) are very
close to an image at the start of the sequence but very far from an image at the end of the sequence. 
However, the distance between each successive image should be close (this is a hypothesis). Under these conditions,
it is likely that there is a dense area which is the area of the images of the sequence, and isolated points around,
which are the outliers. Therefore, the technique used here is to detect outliers with density-based clustering.
Then we implemented SSIM to quantise the difference between the two images and create a matrix . We sort the images based 
on the result of the values.

#### What is DBSCAN
Density-based spatial clustering of applications with noise (DBSCAN) is a data clustering algorithm.
It is a density-based clustering non-parametric algorithm: given a set of points in some space, it groups together 
points that are closely packed together (points with many nearby neighbors), marking as outliers points that lie alone 
in low-density regions (whose nearest neighbors are too far away). DBSCAN is one of the most common clustering 
algorithms and also most cited in scientific literature.

#### What is SSIM
The Structural Similarity Index (SSIM) is a much newer equation developed in 2004 by Wang et al. SSIM Index quality 
assessment index is based on the computation of three factors; luminance (l), contrast (c) and structure (s). 
The SSIM values range between 0 and 1 where 1 means a perfect match between the original image and the copy.

## Installation
We can use the code by either installing the package on the local or install the docker image 

### Install Package
1. Clone the code on your local
```
git clone https://github.com/princys-laboratory/videoprocess.git
cd videoprocess
```
2. Create and activate the conda environment
```
conda create --name vidprocess python=3.7
conda activate vidprocess
```
3. Install the package
```
pip install ./Installable/vidprocess-0.0.1.tar.gz
```

### Docker Image
Please note that the docker file was tested and implemented on Docker version 19.03.8,

The `Dockerfile` is supplied to build images. Make sure docker is installed on your local.
Type the following on your terminal to confirm docker is intsalled.
```
docker -v
```

You should be able to see the version of the docker in response similar to this `Docker version 19.03.8, build afacb8b`

#### Building the image yourself
1. Clone the code on your local
2. Navigate to the folder

```
git clone https://github.com/princys-laboratory/videoprocess.git
cd videoprocess
```
3. Update your video name on Docker image by replacing `shuffled_19.mp4` with your file name (consider the local file 
   location while updating the data) in the lines
   `COPY ./shuffled_19.mp4 .`  and `CMD ["./main.py", "--input_file", "shuffled_19.mp4", "--output_file", "out.mp4"]` in `Dockerfile` .

4. You can change `out.mp4` with your desired output file name.   

5. Build your image . Below `video-process` signifies the Repository name of the image and `0.1` signifies the Tag
```
docker build --file Dockerfile -t video-process:0.1 .
```

Once the image is successfully build you will see the message `Successfully tagged video-process:0.1
` on your terminal.

On successful installation, you should be able to see the Repository name and Tag when you type the following 
```
docker images
```

## How to run the application
Command line arguments
```
usage:python3 main.py --input_file shuffled_19.mp4 --output_file out6.mp4

argument  : 
--input_file      Path to the input video file to be recitfied
--output_fie      Path to the output file where the recified image is to be stored
```