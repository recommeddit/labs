# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 pytorch/pytorch:1.4-cuda10.1-cudnn7-devel
WORKDIR /root
ADD ./pyabsa_files /root
RUN python -m pip install -r ./requirements.txt
CMD sleep infinity
