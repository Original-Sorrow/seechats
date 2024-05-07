import config
from pyrogram import Client


app = Client(name=config.session, api_id=config.api_id, api_hash=config.api_hash)
