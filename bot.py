import asyncio
import logging
from config_reader import config
from broker_rabbitmq import Broker
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.formatting import Text, Bold

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value())
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

# Хэндлер на текст
@dp.message(F.text)
async def text_messages(message: types.Message, bot: Bot):
    content = Text(message.text, " ", Bold(message.from_user.first_name))
    await bot.send_message(config.user_chat_id, **content.as_kwargs())

# Запуск процесса поллинга новых апдейтов
async def main():
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())