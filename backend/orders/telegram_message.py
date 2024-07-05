from telegram import Bot
from telegram.error import TelegramError
from asgiref.sync import async_to_sync

BOT_TOKEN = '6540201432:AAHgduvHpaBb7NOn1oR8Ph3-PPmuDHmFL-k'

async def send_telegram_message_async(chat_ids, text):
    try:
        bot = Bot(token=BOT_TOKEN)
        for chat_id in chat_ids:
            await bot.send_message(chat_id=chat_id, text=text)
        return True
    except TelegramError as e:
        print(f"Ошибка Telegram: {e}")
        return False

send_telegram_message_sync = async_to_sync(send_telegram_message_async)
