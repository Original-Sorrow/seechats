from pyrogram.enums import ChatType
from config import saving_exceptions


async def chat_type(message_chat_type: ChatType, chat_type: ChatType):
    return message_chat_type == chat_type


async def check_saving_exceptions(chat_id):
    if chat_id in saving_exceptions:
        return True
    return False


