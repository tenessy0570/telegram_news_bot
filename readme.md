### 1. [Installation](#installation)
+ [Using docker](#using-docker)
### 2. [About bot](#about-bot)
+ [Commands](#commands)
### 3. [Database schema](#database-schema)

# Installation
## Using docker

```shell
mkdir tg_bot
cd tg_bot
git clone https://github.com/tenessy0570/telegram_news_bot.git
cd telegram_news_bot
```
Open Dockerfile and add your:<br>
1. Telegram bot token
2. NewsApi api-key

after you did it:
```shell
docker build -t tg_news .
docker run -d --rm tg_news
```

## About bot
This is a simple asynchronous bot to retrieve 
news using newsapi based on news source you
chose. SQLite is being used here as a database.

### Commands:
```shell
/start 
# Initialize bot to use it. Without initial /start you can't use another functions!

/help 
# Get info about bot and commands

/get_resources
# Get list of resources. You can choose on of them to retrieve news from.

/set_resource <name> 
# Set resource as your preferable.

/update_n <number>
# Set user's N value (1 <= N <= 10).
# Amount of retrieved news will be based on this number
# Default value is 5

/get_news
# Get news based on user's N number and preferred resource.
# Can't be used if user didn't set his preferable resource.
```

## Database schema
[click](https://github.com/tenessy0570/telegram_news_bot/blob/main/db/schema.pdf)