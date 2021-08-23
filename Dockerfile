FROM python:3.7

ARG target_env='PROD'

RUN mkdir -p /usr/src/app/videoprocess

WORKDIR /usr/src/app/videoprocess

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY ./videoprocess ./videoprocess
COPY ./main.py .
COPY ./LICENSE .
COPY ./setup.py .
COPY ./README.md .
COPY ./shuffled_19.mp4 .
# COPY ./requirements.txt .

RUN pip install ./ wheel

ENTRYPOINT ["python3"]
CMD ["./main.py", "--input_file", "shuffled_19.mp4", "--output_file", "out.mp4"]