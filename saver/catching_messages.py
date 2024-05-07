from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.types import Message
from misc import app
from saver import filters

from saver.save_message import save_message


@app.on_message()
async def my_handler(client: Client, message: Message):
    """ГЛАВНЫЙ ХАНДЛЕР"""
    chat_type = message.chat.type
    chat_id = message.chat.id
    if await filters.check_saving_exceptions(chat_id=chat_id):
        return
    if await filters.chat_type(message_chat_type=chat_type, chat_type=ChatType.PRIVATE):
        await save_message(message=message, chat_type="user")

