FROM python:3.7.4

RUN mkdir /app
WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]