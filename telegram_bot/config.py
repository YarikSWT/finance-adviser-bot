import os

ENV = os.environ.get("ENV", "DEV")
MONGO_URI = os.getenv("MONGO_URI",'mongodb+srv://root:root@cluster0.ro0oy.mongodb.net/test')
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "1381540699:AAE_06_WD5TQ39Ab5TwtPJRcOM8Wdb9lk-g")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS", "https://finance-adviser-bot.herokuapp.com")
RUNNING_ADDRESS = os.getenv("RUNNING_ADDRESS", "0.0.0.0")
PORT = int(os.environ.get('PORT', '8443'))
# mongo_DB = 'LifeBot'