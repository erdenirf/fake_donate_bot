import asyncio
import logging
from config_reader import config
#from broker_rabbitmq import Broker
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.formatting import Text, Bold
import win32com.client

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value())
# Диспетчер
dp = Dispatcher()
# Очередь сообщений
# broker = Broker()
# channel = broker.channel
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Voice = speaker.GetVoices().Item(8)

# async def send_to_queue(message):
#     # Создание очереди (если не существует)
#     channel.queue_declare(queue=config.rabbitmq_topicname)
#     # Отправка сообщения
#     channel.basic_publish(
#         exchange='',
#         routing_key=config.rabbitmq_topicname,
#         body=message
#     )

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

def SpeakingTextWindows(text):
    speaker.Speak(text)

# Хэндлер на текст
@dp.message(F.text)
async def text_messages(message: types.Message, bot: Bot):
    content = Text(Bold(message.from_user.full_name), ": ", message.text)
    await bot.send_message(config.user_chat_id, **content.as_kwargs())
    SpeakingTextWindows(message.text)
    #await send_to_queue(message.text)

# Запуск процесса поллинга новых апдейтов
async def main():
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())