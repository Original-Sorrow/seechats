import datetime
from pyrogram.types import Message
import os


async def save_message_text(message: Message, chat_dir, file_info=None):
    current_datetime = datetime.datetime.now()
    text = f"[Смс от: {message.from_user.first_name} ({message.from_user.id}) смс в чате: {message.chat.id} отправлено в {current_datetime.strftime('%d-%m-%Y_%H:%M:%S')}]"
    if message.text is not None:
        text += f">>>{message.text}<<<"
    if file_info is not None:
        text += f"//////В СМС ПРИСУТСВЕТ ФАЙЛ, ОН ЗАПИСАН В {file_info}//////"
    if message.caption is not None:
        text += f">>>{message.caption}<<<"
    file = f"{chat_dir}/messages.txt"
    await write(text=text, file=file)


async def write(text, file):
    # print(f"Я запишу текст:\n\n{text}\n\nВ файл:\n\n{file}")
    with open(file=file,mode="a",encoding="utf-8") as file:
        file.write(text.replace("\n",""))
        file.write("\n")
    return
