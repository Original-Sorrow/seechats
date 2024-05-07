import datetime
import os


class dirs_:

    async def create_dirs(self, chat_id, chat_type, file_type=None):
        current_file_floader = None
        current_date = await self.get_current_date()
        current_floader = f"./saved/{chat_type}s"
        await self.create(floader=f"{current_floader}")
        current_floader += f"/{chat_type}_{chat_id}"
        await self.create(floader=f"{current_floader}")
        current_floader += f"/{current_date[2]}-{current_date[1]}"
        await self.create(floader=current_floader)
        current_floader += f"/{current_date[0]}"
        current_chat_floader = current_floader
        await self.create(floader=current_floader)
        current_floader += f"/files"
        await self.create(floader=current_floader)
        if file_type is not None:
            current_floader += f"/{file_type}s"
            await self.create(floader=current_floader)
            current_file_floader = current_floader
        return current_chat_floader, current_file_floader


    async def get_current_date(self):
        current_datetime = datetime.datetime.now()
        current_year = current_datetime.year
        current_month = current_datetime.month
        current_day = current_datetime.day
        return current_day, current_month, current_year

    async def create(self, floader: str):
        if os.path.exists(floader):
            return
        os.mkdir(floader)


dirs = dirs_()
