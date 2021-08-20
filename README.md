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
    - [Using pre-built images](#using-pre-built-images)
    - [Building the image yourself](#building-the-image-yourself)
- [Resources](#resources)
<!-- tocstop -->

## More About The Project

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
