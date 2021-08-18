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