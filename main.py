# bot.py
import os
from dotenv import load_dotenv
from discord.ext import commands
import logging

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
FORMAT = "[%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
logging.basicConfig(filename='bot.log', level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")


bot.load_extension("bot.tournament")

while True:
    try:
        bot.run(TOKEN)
    except Exception as e:
        logging.error(str(e))
