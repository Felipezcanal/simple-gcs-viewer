FROM python:3.10


WORKDIR /app
RUN apt-get update

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

CMD ["python3", "main.py"]




