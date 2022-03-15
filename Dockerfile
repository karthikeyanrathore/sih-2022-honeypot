FROM python:3.8-slim-buster

LABEL maintainer="Karthikeyan rathore <karthikeyan@sih2022>"

WORKDIR /home/sih

COPY requirements.txt /home/sih/requirements.txt

RUN pip3 install -r requirements.txt


#RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc \
                                        # libsndfile1 
RUN apt-get update -y && apt-get install libsndfile1-dev -y 

RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:jonathonf/ffmpeg-4 -y
RUN apt-get install ffmpeg -y

COPY ./build/app.py .
COPY ./build/secure.py .
COPY ./build/templates templates
COPY ./build/static static
COPY ./build/WAV WAV
COPY ./build/key.key .
COPY ./model/normalize.csv ../model/normalize.csv
COPY ./model/svm_tess ../model/svm_tess

EXPOSE 5000 

CMD ["python3", "app.py"]
