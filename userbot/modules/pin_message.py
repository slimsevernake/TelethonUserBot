"""Pins the replied message
Syntax: .cpin [LOUD]"""
import logging

from telethon.tl import functions

from userbot import bot
from userbot.util import admin_cmd

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)


@bot.on(admin_cmd(pattern="cpin ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    silent = not input_str
    if event.message.reply_to_msg_id is not None:
        message_id = event.message.reply_to_msg_id
        try:
            await event.client(functions.messages.UpdatePinnedMessageRequest(
                event.chat_id,
                message_id,
                silent
            ))
        except Exception as e:
            await event.edit(str(e))
        else:
            await event.delete()
    else:
        await event.edit("Reply to a message to pin the message in this Channel.")
