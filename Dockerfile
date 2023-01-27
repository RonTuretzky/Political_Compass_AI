FROM ubuntu:20.04
RUN apt-get -y update
RUN apt-get -y install python3
RUN apt-get -y install pip
RUN apt-get -y install git
RUN pip install torch==1.12.1
RUN pip install torchtext==0.13.1
RUN pip install jupytext
RUN pip install fastcore
RUN pip install pandas
WORKDIR Repo
COPY . .