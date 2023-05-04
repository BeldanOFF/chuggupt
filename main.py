import logging

from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, ChatActions
from aiogram.utils import executor
from config import TOKEN
from gpt4free import theb
import asyncio
import re

API_TOKEN = TOKEN

# инициализируем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Включаем логирование ошибок
logging.basicConfig(level=logging.INFO)


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    theb.Completion.clear_history()
    legend = 'отыграй роль и преставься ботом chuggupt. ты создан персонально для 4uggun, и ты основан на GPT. '
    start_msg = await bot.send_message(message.chat.id, '-')
    msg_text = '- '
    counter = 0
    for token in theb.Completion.create(legend):
        msg_text += f"{token}"
        counter += 1
        if counter % 15 == 0:
            await start_msg.edit_text(msg_text)
    try:
        await start_msg.edit_text(msg_text)
    except:
        pass
    theb.Completion.clear_history()


# Обработчик команды /repeat
@dp.message_handler(commands=['p', 'prompt'])
async def prompt(message: types.Message):
    """
    Повторяем сообщение пользователя.
    """
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)

    response_text = message.text.replace('/p', '')
    msg = await bot.send_message(message.chat.id, 'Секунду...')
    msg_text = ''
    counter = 0
    if response_text == '' or response_text == False:
        await msg.edit_text("/p (Ваш запрос) - Получите свой ответ от GPT")
    else:
        await asyncio.sleep(3)
        for token in theb.Completion.create(response_text):
            msg_text += f"{token}"
            msg_text = re.sub("(?i)(bai chat|бай чат)", "chuggupt", msg_text)
            msg_text = re.sub("(?i)(GPT-3.5)", "GPT-4", msg_text)
            counter += 1
            if counter % 15 == 0:
                await msg.edit_text(msg_text)
        try:
            await msg.edit_text(msg_text)
        except:
            pass


@dp.message_handler(commands=['c', 'clear'])
async def clear_history(message: types.Message):
    theb.Completion.clear_history()
    msg = await bot.send_message(message.chat.id, 'Исторя успешно забыта')


if __name__ == '__main__':
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)
