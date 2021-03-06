"""IX.IO pastebin like site
Syntax: .paste"""
import logging
import os
from datetime import datetime

import requests

from sample_config import Config
from userbot import bot
from userbot.util import admin_cmd

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)


def progress(current, total):
    logger.info("Downloaded {} of {}\nCompleted {}".format(
        current, total, (current / total) * 100))


@bot.on(admin_cmd(pattern="npaste ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.paste <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = "".join(m.decode("UTF-8") for m in m_list)
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    if downloaded_file_name.endswith(".py"):
        # else:
        #     message = "SYNTAX: `.paste <long text to include>`"
        py_file = ""
        py_file += ".py"
        data = message
        key = requests.post('https://nekobin.com/api/documents',
                            json={"content": data}).json().get('result').get('key')
        url = f'https://nekobin.com/{key}{py_file}'
    else:
        data = message
        key = requests.post('https://nekobin.com/api/documents',
                            json={"content": data}).json().get('result').get('key')
        url = f'https://nekobin.com/{key}'

    reply_text = f'Nekofied to *Nekobin* : {url}'
    await event.edit(reply_text)

# data = "tets sgdfgklj kdgjld"

# key = requests.post('https://nekobin.com/api/documents', json={"content": data}).json().get('result').get('key')

# url = f'https://nekobin.com/{key}'

# reply_text = f'Nekofied to *Nekobin* : {url}'
