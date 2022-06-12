FROM python:latest

COPY actions_logging actions_logging
COPY bot bot
COPY db db
COPY news news
COPY typing_utils typing_utils
COPY db_initialize.py db_initialize.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/app"


# tg bot token
ENV BOT_TOKEN=

# From https://newsapi.org/
ENV NEWSAPI_APIKEY=

RUN python db_initialize.py


CMD ["python", "./bot/main.py"]