FROM python:3.11.9-slim-buster
WORKDIR /app
COPY . /app
RUN apt-get update
RUN apt-get update && pip install -r requirements.txt
CMD ["python", "app.py"]