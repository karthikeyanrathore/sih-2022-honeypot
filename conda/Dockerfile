FROM continuumio/miniconda3

LABEL maintainer="Karthikeyan rathore <karthikeyan@sih2022>"



COPY ./build /home/sih/build 

WORKDIR /home/sih

COPY environment.yml /home/sih/environment.yml

RUN conda env create -f environment.yml

# RUN conda create --name sih

SHELL ["conda", "run", "-n", "sih", "/bin/bash", "-c"]

RUN python3 -c "import flask"

