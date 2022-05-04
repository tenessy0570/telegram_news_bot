FROM python:latest

COPY . .

RUN pip install -r requirements.txt


# tg bot token
ENV BOT_TOKEN=

# From https://newsapi.org/
ENV NEWSAPI_APIKEY=

RUN python db_initialize.py

CMD ["python", "main.py"]