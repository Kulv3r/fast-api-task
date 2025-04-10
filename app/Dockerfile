FROM python:3.9

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ADD . /code/
WORKDIR /code
ENV PYTHONPATH=/code

EXPOSE 8000
