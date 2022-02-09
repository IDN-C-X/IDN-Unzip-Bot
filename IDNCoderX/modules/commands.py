# Copyright (c) 2021 Itz-fork
# Edited IDN-C-X

import os
import asyncio
import shutil
import psutil

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from .bot_data import Buttons, Messages
from IDNCoderX.helpers.database import (
    check_user,
    del_user,
    count_users,
    get_users_list,
    # Banned Users db
    add_banned_user,
    del_banned_user,
    count_banned_users,
    get_upload_mode
    )
from IDNCoderX.helpers.unzip_help import humanbytes
from config import Config


# Regex for http/https urls
https_url_regex = ("((http|https)://)(www.)?" + 
                "[a-zA-Z0-9@:%._\\+~#?&//=]" +
                "{2,256}\\.[a-z]" +
                "{2,6}\\b([-a-zA-Z0-9@:%" +
                "._\\+~#?&//=]*)")

# Function to check user status (is banned or not)
@Client.on_message(filters.private)
async def _(client: Client, message: Message):
    await check_user(message)


@Client.on_message(filters.private & filters.command("start"))
async def start_bot(client: Client, message: Message):
    await message.reply_text(text=Messages.START_TEXT.format(message.from_user.mention), reply_markup=Buttons.START_BUTTON, disable_web_page_preview=True)

@Client.on_message(filters.private & filters.command("clean"))
async def clean_ma_files(client: Client, message: Message):
    await message.reply_text(text=Messages.CLEAN_TXT, reply_markup=Buttons.CLN_BTNS)
    message.from_user.mention

@Client.on_message(filters.incoming & filters.private & filters.regex(https_url_regex) | filters.document)
async def extract_dis_archive(client: Client, message: Message):
    unzip_msg = await message.reply("`Processing ⚙️...`", reply_to_message_id=message.message_id)
    user_id = message.from_user.id
    download_path = f"{Config.DOWNLOAD_LOCATION}/{user_id}"
    if os.path.isdir(download_path):
        return await unzip_msg.edit("`Already one process is going on, Don't spam you idiot 😑!` \n\nWanna Clear You Files from my server? Then just send **/clean** command!")
    await unzip_msg.edit("**What do you want?**", reply_markup=Buttons.CHOOSE_E_BTN)

# Database Commands
@Client.on_message(filters.private & filters.command("stats") & filters.user(Config.BOT_OWNER))
async def send_stats(client: Client, message: Message):
    stats_msg = await message.reply("`Processing ⚙️...`")
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await count_users()
    total_banned_users = await count_banned_users()
    await stats_msg.edit(f"""
**💫 Current Bot Stats 💫**

**👥 Users:** 
 ↳**Users in Database:** `{total_users}`
 ↳**Total Banned Users:** `{total_banned_users}`
 
**💾 Disk Usage,**
 ↳**Total Disk Space:** `{total}`
 ↳**Used:** `{used}({disk_usage}%)`
 ↳**Free:** `{free}`
 
**🎛 Hardware Usage,**
 ↳**CPU Usage:** `{cpu_usage}%`
 ↳**RAM Usage:** `{ram_usage}%`"""
    )

async def _do_broadcast(message, user):
    try:
        await message.copy(chat_id=int(user))
        return 200
    except FloodWait as e:
        asyncio.sleep(e.x)
        return _do_broadcast(message, user)
    except Exception:
        await del_user(user)


@Client.on_message(filters.private & filters.command("broadcast") & filters.user(Config.BOT_OWNER))
async def broadcast_dis(client: Client, message: Message):
    bc_msg = await message.reply("`Processing ⚙️...`")
    r_msg = message.reply_to_message
    if not r_msg:
        return await bc_msg.edit("`Reply to a message to broadcast!`")
    users_list = await get_users_list()
    # trying to broadcast
    await bc_msg.edit("`Broadcasting has started, This may take while 🥱!`")
    success_no = 0
    failed_no = 0
    for user in users_list:
        b_cast = await _do_broadcast(message=r_msg, user=user["user_id"])
        if b_cast == 200:
            success_no += 1
        else:
            failed_no += 1
    total_users = await count_users()
    await bc_msg.edit(f"""
**Broadcast Completed ✅!**
**Total Users:** `{total_users}`
**Successful Responses:** `{success_no}`
**Failed Responses:** `{failed_no}`
    """)

@Client.on_message(filters.private & filters.command("ban") & filters.user(Config.BOT_OWNER))
async def ban_user(client: Client, message: Message):
    ban_msg = await message.reply("`Processing ⚙️...`")
    try:
        user_id = message.text.split(None, 1)[1]
    except:
        return await ban_msg.edit("`Give a user id to ban!`")
    await add_banned_user(user_id)
    await ban_msg.edit(f"**Successfully Banned That User ✅** \n\n**User ID:** `{user_id}`")

@Client.on_message(filters.private & filters.command("unban") & filters.user(Config.BOT_OWNER))
async def unban_user(client: Client, message: Message):
    unban_msg = await message.reply("`Processing ⚙️...`")
    try:
        user_id = message.text.split(None, 1)[1]
    except:
        return await unban_msg.edit("`Give a user id to unban!`")
    await del_banned_user(user_id)
    await unban_msg.edit(f"**Successfully Unbanned That User ✅** \n\n**User ID:** `{user_id}`")
    
    
# Database Commands
@Client.on_message(filters.private & filters.command(["mode", "setmode"]))
async def set_up_mode_for_user(_, message: Message):
    upload_mode = await get_upload_mode(message.from_user.id)
    await message.reply(Messages.SELECT_UPLOAD_MODE_TXT.format(upload_mode), reply_markup=Buttons.SET_UPLOAD_MODE_BUTTONS)
