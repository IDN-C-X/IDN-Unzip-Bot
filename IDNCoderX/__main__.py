# Copyright (c) 2021 Itz-fork
# Edited IDN-C-X

import os

from pyrogram import idle
from . import IDNClient
from .helpers.unzip_help import check_logs
from config import Config

if __name__ == "__main__" :
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    IDNClient.start()
    print("Checking Log Channel ...")
    check_logs()
    print("Bot is active Now! Join @IDNCoderX")
    idle()
