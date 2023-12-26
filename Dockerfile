FROM python:3.9.2-slim

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["sh", "-c", "uvicorn superboite_api.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
