from pyrogram.types import Message

from saver.folders import dirs
from saver.save_file import _file
import os

from saver.save_message_text import save_message_text


async def save_message(message: Message, chat_type: str):
    chat_dir = await dirs.create_dirs(chat_type=chat_type, chat_id=message.chat.id)
    file_info = None
    if message.document is not None or message.media is not None:
        file = _file(message=message, chat_id=message.chat.id, chat_type=chat_type)
        file_info = await file.save()
    await save_message_text(message=message, file_info=file_info, chat_dir=chat_dir[0])
