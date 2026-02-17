FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN pip install gunicorn


ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 4 --threads 8  app:app