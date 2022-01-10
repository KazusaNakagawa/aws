FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
    curl \
    default-libmysqlclient-dev \
    mariadb-client \
    python3-dev \
    sudo \
    unzip \
    vim \
    wget \
    zip

# root権限意外でも扱えるようにする 共有サーバとか
WORKDIR /opt

# Anaconda3 任意のversionをinstall
ENV ANACOND_FILENAME=Anaconda3-2021.05-Linux-x86_64.sh

RUN wget https://repo.continuum.io/archive/$ANACOND_FILENAME && \
    sh $ANACOND_FILENAME -b -p /opt/anaconda3 && \
    rm -f $ANACOND_FILENAME

# aws CLI: https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/install-cliv2-linux.html
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install

ENV PATH /opt/anaconda3/bin:$PATH
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

WORKDIR /
  CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--LabApp.token=''"]
