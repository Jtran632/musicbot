FROM python:3.10.4-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install requests
RUN pip3 install BeautifulSoup4
COPY . .

RUN apt-get update && apt-get install -y ffmpeg

CMD ["python3", "bot.py"]