import env

from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from wildberries import get_product_by_url, get_product_position_by_query
from mistral import get_key_queries

TOKEN = env.get("TELEGRAM_BOT_TOKEN")

def get_help_text():
    help_text_file = open("./bot_help_text.md", encoding = "utf8")
    text = help_text_file.read()
    help_text_file.close()
    return text

dispatcher = Dispatcher()

@dispatcher.message(Command("start"))
async def start(message):
    await message.answer(get_help_text())

@dispatcher.message(Command("help"))
async def help(message):
    await message.answer(get_help_text())

@dispatcher.message(Command("get_product_rating"))
async def get_product_rating(message, command):
    url = command.args
    product = get_product_by_url(url)
    key_queries = get_key_queries(product["name"], product["description"])

    await message.answer(f"Список ключевых запросов: \n\n{"\n".join(key_queries)}")

    for query in key_queries:
        position = get_product_position_by_query(product["id"], query)

        await message.answer(f"Позиция товара по запросу \"{query}\" - {position}")

async def main():
    bot = Bot(token = TOKEN)
    await dispatcher.start_polling(bot)
