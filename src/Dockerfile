FROM ubuntu:latest

WORKDIR /app

RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

COPY ./app /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8501/tcp

CMD  ["streamlit", "run", "app.py"]

