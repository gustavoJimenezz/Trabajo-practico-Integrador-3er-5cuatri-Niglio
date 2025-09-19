FROM python:3.13-slim

WORKDIR /app

COPY ./app ./app
COPY main.py .
COPY requirements.txt .
COPY .env .
COPY init_db.py .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
