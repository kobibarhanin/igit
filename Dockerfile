FROM python:3.7

# general installations
RUN apt-get update && apt-get -y install \
    sudo \
    vim \
    wget \
    locales \
    curl \
    unzip

RUN sudo locale-gen en_US.UTF-8

# python installations
RUN sudo apt -y install python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install pipenv

WORKDIR /home/igit
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --dev

COPY . .
RUN pipenv install --skip-lock -e .

WORKDIR /home
RUN git clone https://github.com/kobibarhanin/igit_test.git
WORKDIR /home/igit_test

RUN git checkout state_a && \
    git config --global user.name "abc" && \
    git config --global user.email "abc@example.com"

ENV test_dir=/home/igit_test
ENV source_dir=/home/igit/igit

CMD /root/.local/share/virtualenvs/igit-jeZuJjfX/bin/python3.7 -m pytest -v -s -q  ../igit/igit/tests
