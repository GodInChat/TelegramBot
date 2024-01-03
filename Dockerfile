# Based on https://hub.docker.com/r/robd003/python3.10

FROM robd003/python3.10:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py ./

CMD [ "python", "./bot.py" ]
