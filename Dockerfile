FROM apache/airflow:3.0.1-python3.11

USER root
RUN apt update
RUN apt install gcc build-essential make cmake libleveldb-dev neovim net-tools gosu iputils-ping openssh-sftp-server openssh-server -y

USER airflow

COPY requirements.txt requirements.txt
RUN pip install -U pip httpcore setuptools wheel future
RUN pip install -r requirements.txt

RUN airflow db migrate
