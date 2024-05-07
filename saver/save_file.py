import config
import os
import json
from io import BytesIO
from pyrogram.types import Message, User
from misc import app
from saver.folders import dirs


class _file:
    def __init__(self, message: Message, chat_id: int, chat_type: str):
        self.__message: Message = message
        self.__user: User = message.from_user
        self.__file: tuple[str, BytesIO] = None
        self.__chat_id: int = chat_id
        self.__chat_type: str = chat_type
        self.__file_path = None

    async def save(self):
        await self.create_files_dir()
        try:
            msg: Message = await self.copy_file()
            self.__file = await self.download(message=msg)
            try:
                await msg.edit_caption(
                    caption=f"Файл от {self.__chat_type} <b>{self.__user.first_name}</b>\n"
                            f"(<code>{self.__user.id}</code>)\n"
                            f"[<code>{self.__file_path[1]}/{self.__file[0]}</code>]"
                )
            except:
                await msg.reply(
                    text=f"Файл от {self.__chat_type} <b>{self.__user.first_name}</b>\n"
                         f"(<code>{self.__user.id}</code>)\n"
                         f"[<code>{self.__file_path[1]}/{self.__file[0]}</code>]"
                )
        except:
            self.__file = await self.download(message=self.__message)
            await self.send_downloaded_file()
        finally:
            await self.seve_file_locally()
            return f"{self.__file_path[1]}/{self.__file[0]}"

    async def copy_file(self):
        return await self.__message.copy(chat_id=config.logchat_id)

    async def send_downloaded_file(self):
        await app.send_document(
            chat_id=config.logchat_id,
            document=self.__file[1],
            file_name=self.__file[0],
            caption=f"Файл от {self.__chat_type} <b>{self.__user.first_name}</b>\n"
                    f"(<code>{self.__user.id}</code>)\n"
                    f"[<code>{self.__file_path[1]}/{self.__file[0]}</code>]"
        )
        return

    async def download(self, message: Message):
        file = await app.download_media(message, in_memory=True)
        file_info = await self.get_file_info(message=message)
        file_extension = await self.get_file_extension(file_name=file.name)
        file_name = f"{file_info[0]}.{file_extension}"
        self.__file_path = await dirs.create_dirs(
            chat_type=self.__chat_type,
            chat_id=self.__chat_id,
            file_type=file_info[1]
        )
        file_bytes = BytesIO(bytes(file.getbuffer()))
        return file_name, file_bytes

    async def seve_file_locally(self):
        await self.create_files_dir()
        with open(f"{self.__file_path[1]}/{self.__file[0]}", "wb") as f:
            f.write(self.__file[1].getvalue())

    async def get_file_info(self, message: Message):
        js = json.loads(str(message))
        return js[str(message.media.name).lower()]["file_id"], str(message.media.name).lower()

    async def get_file_extension(self, file_name: str):
        text = file_name.split(".")
        return text[len(text) - 1]

    async def create_files_dir(self):
        try:
            os.mkdir(self.__file_path)
        except:
            pass

