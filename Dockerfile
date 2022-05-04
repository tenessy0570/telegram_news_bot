FROM python:latest

COPY . .

RUN pip install -r requirements.txt


# tg bot token
ENV BOT_TOKEN=5352126769:AAEt5Vta3_OYOHuzAJFPrBogXG4P7NjDufc

# From https://newsapi.org/
ENV NEWSAPI_APIKEY=44264e76d9444b84bf120888933db7f0

RUN python db_initialize.py

CMD ["python", "main.py"]