FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV TZ="Europe/Madrid"

COPY . .

CMD ["app.py"]
ENTRYPOINT ["python3"]
