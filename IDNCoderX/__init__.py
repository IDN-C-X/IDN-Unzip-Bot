# Copyright (c) 2021 Itz-fork
# Edited IDN-C-X

from pyrogram import Client
from pyromod import listen

from config import Config

plugins = dict(root="IDNCoderX/modules")
IDNClient = Client(
        "UnzipperBot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        plugins=plugins
    )
