import os

ENV = os.environ.get("ENV", "DEV")
MONGO_URI = os.getenv("MONGO_URI",'mongodb+srv://root:root@cluster0.ro0oy.mongodb.net/test')
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "1381540699:AAHw1Y8vTocoBHhlwcDhBXeFU8KI_kSquEc")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS", "https://finance-adviser.leapper.com") #https://finance-adviser-bot.herokuapp.com
RUNNING_ADDRESS = os.getenv("RUNNING_ADDRESS", "0.0.0.0")
PORT = int(os.environ.get('PORT', '8443')) #8443
API_URL = os.getenv("API_URL", "http://api:8000/api") #http://localhost:8000/api
# mongo_DB = 'LifeBot'
