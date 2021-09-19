FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
	sudo \
	wget \
	vim

# root権限意外でも扱えるようにする 共有サーバとか
WORKDIR /opt

# 任意のversionをinstall
RUN wget https://repo.continuum.io/archive/Anaconda3-2021.05-Linux-x86_64.sh && \
	sh Anaconda3-2021.05-Linux-x86_64.sh -b -p /opt/anaconda3 && \
	# インストール後必要ないから削除
	rm -f Anaconda3-2021.05-Linux-x86_64.sh

ENV PATH /opt/anaconda3/bin:$PATH
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

WORKDIR /
  CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--LabApp.token=''"]
