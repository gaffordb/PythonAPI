FROM python:3.8

COPY . /PythonAPI/

WORKDIR /PythonAPI/

RUN pip install -r requirements.txt -e .

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -



WORKDIR /PythonAPI/Scenic

RUN $HOME/.poetry/bin/poetry config virtualenvs.create false
RUN $HOME/.poetry/bin/poetry install

WORKDIR /PythonAPI/