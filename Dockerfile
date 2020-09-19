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

WORKDIR /home/gitsy
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install

COPY . .
RUN pipenv install --skip-lock -e .

WORKDIR /home
RUN git clone https://github.com/kobibarhanin/gitsy_stage.git
WORKDIR /home/gitsy_stage

RUN git checkout state_a && \
    git config --global user.name "abc" && \
    git config --global user.email "abc@example.com"

CMD /root/.local/share/virtualenvs/gitsy-382rVgWt/bin/python3.7 -m pytest -v -s --source_dir /home/gitsy --test_dir /home/gitsy_stage  ../gitsy/tests
